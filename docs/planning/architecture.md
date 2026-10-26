# Proposed architecture, technology, and domain design

Status: proposed. All decisions require the approval recorded in [decisions.md](decisions.md). The current delivery target is a **zero-new-spend local prototype**, following the product owner's clarification. External hosting is a later gate, not an implicit purchase.

## E. System boundaries

```text
Learner / curator browser
        |
        | One application origin (loopback locally; HTTPS before remote use)
        v
Next.js UI / thin reverse proxy
        | /api/v1/* and /admin/* routed to Django
        | no independent business rules or direct database access
        v
Django + DRF modular monolith
  accounts | curriculum | roadmaps | practice/assessments | projects/evidence
  resources/verification | mentor adapter | administration/audit
        |                      |                     |
        v                      v                     v
 PostgreSQL             Local AI runtime       Scheduled command
 content revisions      loopback/private       same application code
 private learning       no direct DB/tools     -> vetted public resource URLs
 sessions/jobs/audit     cloud disabled         -> append verification observations
        |
        v
 Encrypted backup on existing storage (restore drill)

Browser -> original YouTube/documentation sites for learning
           (links, no copied videos, no assumed transcript rights)

Future, only after approval: cloud model adapter, managed DB/hosting,
object storage for uploads, queue worker if actual workloads require one.
```

Keep one repository and one backend application with explicit modules and service functions. Existing `careers` can own curriculum initially rather than renaming every app. Existing `projects` owns project evidence initially. Add a `resources` module only when separating verification/publication responsibilities is useful. No microservices or event broker.

Backend commands such as accept_roadmap, record_activity, finalize_attempt, publish_release, and review_submission own transactions and invariants. Views validate DTOs, authorize, invoke services, and serialize responses. Query helpers apply ownership/publication filtering consistently. Model methods are not the sole enforcement point; database constraints protect race-sensitive invariants.

For the first local demonstration, run services on loopback and use test accounts. PostgreSQL and AI endpoints are never browser-accessible or publicly exposed. Use a thin local application proxy so cookies and CSRF follow the same contract as future hosting. Do not build a second API in Next.js. Remote access, tunnels, public TLS, and real accounts require a separate deployment review.

## F. Technology comparison

Each row states recommendation, fit, alternatives, trade-offs, cost, operational burden, migration risk, confidence, and approval requirement. “Free” means no software/service fee under the local design, not free electricity or unlimited hardware capacity.

| Choice | Recommendation and why it fits | Alternatives / trade-offs | Cost and operations | Migration / lock-in | Confidence / approval |
|---|---|---|---|---|---|
| Backend | Retain Django + DRF; move to latest compatible Django 5.2 LTS patch after tests. Admin, auth, ORM, transactions suit content-heavy domain. | FastAPI: good typed APIs, but admin/auth/content workflows require assembly. TypeScript/NestJS: one language but rewrites Python work. Django templates/HTMX: fewer runtimes, but replaces existing frontend investment. | Local license cost zero; one Python app. Lock runtime and transitive dependencies; remove unused packages only after usage audit. | Conventional SQL/Python; Django-specific models/admin, moderate framework coupling. | High / yes |
| Frontend | Retain TypeScript/React and evaluate Next.js active LTS upgrade. Public curriculum pages benefit from server rendering; task interactions remain client components. | Vite SPA simplifies runtime but requires changes to routing/deployment and loses current framework behavior. Server templates reduce JS but are a deliberate rewrite. | Local zero fee, Node process consumes RAM. Build for production before measuring footprint. | Keep API/domain rules external; avoid provider-specific server features. | Medium-high / yes |
| Relational store | PostgreSQL 16 at a maintained patch initially; no pgvector extension required. | SQLite useful for isolated smoke work but differs on locking/constraints; document store weak fit for relational evidence and releases. | Local zero fee; one DB process and backups. Keep development/test behavior aligned with real DB. | SQL dump/restore offers exit path; avoid unnecessary extensions. | High / yes |
| Browser auth | Django server sessions, HttpOnly cookies, CSRF token, same origin; permission groups for staff. | Existing localStorage bearer token is simpler for separate clients but exposes tokens to script compromise. External identity service adds account/terms/availability dependency. | Local zero fee; DB-backed sessions; recovery email only external-launch requirement. | Future mobile OAuth/OIDC can be added without making browser tokens permanent. | High / yes |
| Background jobs | Scheduled management commands for link checks, deletion, cleanup; DB run records/leases and bounded batches. | Celery+Redis appropriate for sustained asynchronous workloads but adds two processes now. Request-time fetching harms latency and safety. | Local OS scheduler; missed runs catch up on next start, one run per job lease. No broker bill or process required. | Keep job functions broker-independent; migrate dispatch later. | High for local scale / yes |
| AI runtime | Local-only Ollama adapter; test a small quantized instruction model against real curriculum; pin model digest and license after evaluation. | llama.cpp provides lower-level control but more integration work. Cloud APIs simplify capacity but conflict with zero spend unless a genuinely suitable free tier is explicitly approved. | No paid inference; memory/CPU constrained, one generation at a time. Runtime/model download requires implementation approval. | Narrow adapter and prompt versions reduce vendor dependence; model quality is not portable by assumption. | Medium for integration, low for quality/speed until measured / yes |
| Content/search | Django Admin with validated publication services; relational filters and PostgreSQL search only when needed. | Bespoke CMS or headless CMS improves editorial polish at substantial integration cost; vector search unjustified for a small curated library. | Local zero fee; reviewer labor is the main cost. | Use owned content exports; no proprietary content store. | High / yes |
| Artifacts | Text + validated external HTTPS links; no upload/URL unfurling in MVP. | Object storage supports reliable file retention but requires scanning, ACLs, quotas, and operational choices. | Zero storage-service fee; external URLs can disappear or expose data at source. | Submission metadata and reviews retained; future object storage behind artifact interface. | High / yes |
| Deployment | Existing computer, loopback, supervised prototype; separate dev/test data. | Free cloud tiers may sleep/expire/change and need database/AI/email solutions. Paid managed PaaS is easier for public operation but outside authorized budget. | No new subscription or hardware; no uptime SLA; existing disk backup cannot protect against whole-device loss. | Standard processes/containers and SQL exports support later move. | High for prototype, unproven for public service / yes |
| API style | REST JSON under existing `/api/v1`, explicit DTOs; OpenAPI 3.1 contract and generated TS types after approval. | GraphQL adds authorization/query-cost concerns with little MVP benefit; RPC reduces generic client portability. | No service fee; schema review and contract tests required. | HTTP contracts avoid database exposure; additive changes within v1. | High / yes |

Django's support table marks 5.1 unsupported and 5.2 LTS supported through April 2028. This makes 5.2 a conservative upgrade target, rather than a recommendation to remain on the installed range. [Django release support](https://www.djangoproject.com/download/)

Next.js recommends an active or maintenance LTS release. Check the support boundary and security advisories again during implementation, then choose a compatible pinned patch. [Next.js support policy](https://nextjs.org/support-policy)

Ollama documents local API access without API keys, local-only operation, and a switch to disable cloud features. These establish an integration option, not a guarantee that a particular model is capable or fast on the available machine. [Local API](https://docs.ollama.com/api/introduction), [local-only settings](https://docs.ollama.com/faq)

### Frontend organization

Keep `src/app` for routing/layout/loading/error boundaries. Introduce feature folders only for shared workflow logic: `features/onboarding`, `roadmaps`, `learning`, `projects`, `mentor`; reusable accessible primitives in `components`; API DTOs/client in `lib/api`. Prefer native forms plus explicit validation; avoid adding a global state library initially. Keep transient form state local, durable state on the server, shareable filters in URLs. Browser storage must not contain bearer tokens or cached private records.

Server-render public pages where helpful; private requests are user-scoped, uncached (`no-store`), and never put into shared static output. Client hydration is limited to interactive controls. Debounce search, paginate large collections, self-host or omit external fonts, load no video until the learner opens a source. Stable keys and optimistic UI only for reversible actions with rollback/error messaging; grades and accepted evidence wait for server confirmation.

### Hosting and AI cost alternatives

The proposed plan targets **US$0 in new hosting/model subscriptions**: local processes, existing hardware, no card-backed trial and no cloud fallback. Internet access is still needed for external courses and initial model/dependency downloads. No model is downloaded now. Exact model size, disk needs, license, and performance must be checked during P0. The zero-spend constraint is confirmed; this implementation approach remains proposed.

Free hosted services are not selected. A static site alone cannot run Django, PostgreSQL, and private local inference. A cloud API's promotional quota is not a permanent operating plan. If remote access becomes essential, review the complete stack and account terms together rather than advertising a free front end while hiding backend charges.

For future comparison only: Render offers web/worker/cron/database services with separately priced compute; paid PostgreSQL has PITR, and its free database does not include the same backup capabilities. Railway advertises a US$5 Hobby minimum usage and US$20 Pro minimum usage, with additional resource consumption beyond included credits. Neither price is a complete Veyra deployment quote. PaaS reduces patching work; a self-managed VPS may reduce provider fees but increases operations and recovery responsibility. All paid alternatives are out of the current budget. [Render pricing](https://render.com/pricing), [Render recovery](https://render.com/docs/postgresql-backups), [Railway pricing](https://railway.com/pricing)

### Cloud model comparison, for a later budget decision only

Prices observed 2026-10-23, standard text input/output per million tokens, excluding taxes, tools, caching and other charges. These are candidate baselines, not a commitment or a quality ranking.

| Candidate | Input / output | Structured output / privacy considerations | Decision |
|---|---|---|---|
| OpenAI GPT-6 Luna | $0.10 / $0.50 | Structured outputs available; default API data not used for training without opt-in, but abuse-monitoring retention can apply. Disable unnecessary stored application state. | Cost-focused candidate if budget changes; evaluate teaching and citation accuracy. |
| Anthropic Claude Haiku 5.5, short prompts | $0.10 / $0.50 | JSON schema output supported on this family. Standard API retention has a 30-day baseline with exceptions; verify contract/model details before private data. | Alternative evaluation candidate; do not infer quality from price or latency marketing. |
| Google Gemini 3.1 Flash-Lite, paid text tier | $0.25 / $1.50 | Pricing distinguishes free-tier data use from paid-tier data use. Free-tier text should not be treated as having paid-tier privacy terms. Exact schema compatibility remains to verify. | Free-tier private mentoring is not the recommended default; no silent provider switch. |

Sources: [OpenAI pricing](https://developers.openai.com/api/docs/pricing), [structured output](https://developers.openai.com/api/docs/guides/structured-outputs), [data controls](https://developers.openai.com/api/docs/guides/your-data); [Claude pricing](https://platform.claude.com/docs/en/about-claude/pricing), [structured output](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), [retention](https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data); [Gemini pricing/data-use distinctions](https://ai.google.dev/gemini-api/docs/pricing).

Provider availability, account limits, region, latency, and educational quality were not tested. Select by blinded evaluations with expert reviewers, measuring p50/p95 latency, validity, usefulness, failures, and actual tokens. A model advertised as inexpensive is not automatically suitable. Use an explicit adapter selection; no runtime multi-provider failover in the prototype.

Budget formula if paid inference is later approved: `calls × (input_tokens × input_price + output_tokens × output_price) / 1,000,000`. For illustration, 10,000 calls at 3,000 input and 600 output tokens with $0.10/$0.50 rates is $6 base inference, excluding other costs and retries. This is a hypothetical comparison, not an authorized spend or forecast. The zero-spend prototype instead limits compute time and concurrency.

## G. Domain and data architecture

### Relationship overview

```text
CareerPath --< PathCompetency >-- Competency --< CompetencySkill >-- Skill
CareerPath --< CurriculumRelease --< ReleaseSkill / SkillDependency
Skill --< LearningObjective --< Topic (optional grouping)
Resource --< ResourceRevision >--< ObjectiveResource >-- LearningObjective
CurriculumRelease --< Activity / ProjectVersion / AssessmentVersion
User -- Profile
User --< UserRoadmap >-- CurriculumRelease
UserRoadmap --< RoadmapStep --< ActivityRecord
User --< AssessmentAttempt >-- AssessmentVersion --< QuestionVersion
User --< ProjectSubmission >-- ProjectVersion
ProjectSubmission --< ProjectReview --< SkillEvidence >-- Skill
AssessmentAttempt --< SkillEvidence
SkillEvidence -> derived SkillProficiency (evidence type and scope preserved)
Resource --< ResourceVerification / ResourceReport
User --< AIConversation --< AIMessage; AIRequest tracks bounded execution
Publication/review/security operations -> AuditEvent
```

CareerPath combines “career” and “role” for MVP: a role-level pathway with category and scope. Split career families from roles later only if navigation requires it. Skills are globally reusable identities; pathway mapping determines context and target level. Dependencies belong to a versioned pathway release, not a permanent universal ordering. This allows shared analytical skills without asserting every profession teaches them in the same sequence.

### Entity catalog

Conventions: UUID public IDs; UTC timestamps; public catalog records are public **only when published**, excluding author-only notes and answer keys. Drafts are staff-private. Learner records are owner-private with narrowly scoped assigned-reviewer access. Published semantic content is immutable: edits create a revision; archive retires availability without deleting referenced history. Draft edits use optimistic versions. JSON is limited to validated rubric/answer/evaluation structures, not arbitrary entity references.

| Entity | Purpose and relationships | Ownership / lifecycle / mutability | Constraints and useful indexes |
|---|---|---|---|
| User, Profile | Identity, timezone, hours, optional learning preferences. | Learner-private; editable safe fields; admin-owned permissions; delete via account workflow. No inferred learning-style diagnosis. | Normalized unique email; hours within agreed bound, zero means paused; role immutable through profile API. |
| CareerPath | Public role/pathway identity, category, typical work, scope, reviewer. | Platform-owned; archive, no hard delete if referenced. Titles/descriptions captured in releases. | Unique slug; published/category index. |
| Competency, PathCompetency | Reusable capability group and ordered path mapping. | Platform-owned; draft mutable; published descriptions pinned in release. | Unique path/competency mapping; nonnegative order. |
| Skill, CompetencySkill | Reusable skill identity and mapping, independent of career. | Platform-owned; retire identities; no cascading removal of evidence. | Unique stable skill key; unique mapping pair; reverse mapping indexes. |
| LearningObjective, Topic | Observable outcomes and optional grouping under a skill. | Platform-owned; release-versioned wording; topics can remain simple ordered grouping records. | Stable objective key, skill FK, unique order where meaningful. |
| CurriculumRelease / RoadmapTemplate | Reviewed bundle of path requirements, estimates and ordered activity definitions. One concept rather than two duplicate engines. | Platform-owned; numbered immutable published release; author/reviewer/checksum; draft → validated → reviewed → published → retired. | Unique path/version; one current published pointer per path; protected references to older releases. |
| ReleaseSkill, SkillDependency | Skill targets and required/recommended edges within release. | Part of immutable release; required evidence level on each gate; optional edges only advise. | Unique release/skill and release/edge; no self-edge; both endpoints in release; DAG checked transactionally. |
| Resource, ResourceRevision | Stable source identity plus title, URL, provider, format, duration, language, access restrictions, rights and suitability metadata. | Platform-owned; published metadata revision immutable; current health separate; human-reviewed free-access status. | Normalized canonical URL lookup (review collisions), revision uniqueness, provider/status filters. |
| ObjectiveResource | Reuse one resource across multiple objectives, with priority and fallback role. | Platform-owned; pinned in curriculum release. | Unique release/objective/resource-revision; FK constraints. |
| ResourceVerification | Timestamped reachability/pricing-review observations with method, outcome, redirect chain and reviewer. | Operations-owned, staff-private; append-only, retention policy applies; latest health is derived. | Resource/time index; unique job/resource key; no fetched body stored by default. |
| ResourceReport | Learner flags breakage, paywall, quality or accessibility issue. | Reporter/staff-private; limited free text; mutable triage status, audit transitions. | Reporter/resource/open-report deduplication; status/time index. |
| Activity | Learn/practice task definition linked to objectives, estimated range, completion rule. | Platform-owned; immutable release version; compact finite type enum. | Stable activity key within release; duration nonnegative; explicit required/optional flag. |
| ProjectVersion | Brief, objectives, deliverables, rubric and submission types. | Platform-owned; immutable when published; release pins version. | Rubric schema/weights/criterion IDs validated; many-skill mapping; nonempty deliverables. |
| AssessmentVersion, QuestionVersion | Knowledge check, eligibility and scoring rules; objective mappings. | Platform-owned; immutable published versions; answer keys always restricted. | Nonempty question set; valid option IDs and thresholds 0–100; version uniqueness. |
| UserRoadmap | Owner's accepted release, schedule parameters, active/paused/archived state. | Learner-owned; schedule mutable, accepted baseline pinned; revisions retained. | Partial unique active roadmap per user; owner/status index; optimistic version. |
| RoadmapStep | Concrete requirement, ordering and earned credit on a user's roadmap. | Learner-private; references pinned content; service-controlled transitions. | Unique roadmap/activity key; content references protected; unmet gates cannot be completed by client. |
| ActivityRecord / ProgressRecord | Completion or reversal with actor, timestamp and reason. | Learner-private; append-only event history for this bounded domain, not platform-wide event sourcing. | Unique owner/idempotency key; roadmap/time index; never equates consumption to competence. |
| AssessmentAttempt | Version, eligible questions, start/finish state, answers and server grade. | Learner-private; in-progress mutable; finalized immutable; corrections create superseding decision. | Owner/version/time; atomic single finalization; valid answers only; scores 0–100. |
| ProjectSubmission | Text/link artifact and reflection against a pinned project version. | Owner-private; drafts editable; submitted revisions immutable; later attempts preserve earlier work. | Owner/project/time; unique submission revision; URL length/scheme bounds. |
| ProjectReview | Reviewer, rubric-version scores, feedback, decision, provenance. | Assigned reviewer/owner-private; finalized append-only; changes supersede and audit. | Submission/reviewer/time; criterion membership, score bounds; no auto-approval from AI. |
| SkillEvidence | Objective-linked evidence from attempt or project review; scope and provenance. | Owner-private; append-only earned/revoked decisions; retained until deletion policy. | Exactly one source FK per evidence record; unique source/objective; owner/skill index. |
| SkillProficiency | Read projection of self-report, knowledge check, practical demonstration and gaps. | Owner-private; rebuildable from evidence + policy version. | Unique owner/skill/policy; no unexplained numeric employability score. |
| AIConversation, AIMessage | Short task-scoped exchanges with context/revision provenance. | Owner-private, bounded retention; no cross-user cache; messages immutable except deletion/redaction workflow. | Owner/task/time; bounded message length and count. |
| AIRequest / JobRun | Queued/running/completed/failed status, lease, resource usage, timeout, prompt/model versions. | Owner/status visible for AI; operations metadata staff-private; no full prompts in logs. | Unique owner/request key; lease/status/time indexes; one active generation globally initially. |
| AuditEvent | Staff publication/review, permission/security and deletion actions. | Restricted operations-owned, append-only with retention; minimal identifiers. | Actor/time, target/time; no passwords, answers or transcript bodies. |
| AccountExport, DeletionRequest | Track owner-authorized data-rights workflows and deletion replay after restores. | Owner receipt/operations metadata; bounded expiry; exports removed after 24h, minimal deletion ledger retained through backup expiry. | Unique owner/request key; status/expiry indexes; no deleted content embedded in ledger. |
| IdempotencyRecord, RateLimitBucket | Protect write retries and shared abuse budgets across local processes. | Internal operations state, not public content; expire records/buckets after documented window. | Unique actor/operation/key or actor/window; atomic increment/claim; request hash protected, no raw passwords. |

Do not create Achievement, LearningSession, NotificationPreference, public portfolio, or a generic polymorphic ContentRevision table in MVP. Transactional email preferences belong to account policy; marketing/reminder preferences arrive only with the relevant feature. Typed content versions and publication audit cover current revision needs. Avoid both a stored percentage and a second authoritative progress fact: activity/evidence history is canonical; dashboard summaries are projections.

### Invariants and algorithms

1. **Publication:** all required skills have observable objectives, permitted free learning routes, practice, and appropriate evidence requirements. At least one project covers the pathway's central practical objectives. No unknown URLs or unchecked generated references become published.
2. **History:** attempts pin assessment/question versions; reviews pin rubric/project versions; roadmaps pin curriculum release. Content retirement must not cascade-delete evidence. Material curriculum changes affect new enrollments unless the learner explicitly accepts a migration preview.
3. **Planning:** validate required-edge DAG; resolve a stable topological order using explicit order then stable ID for ties; incorporate existing evidence only when objective/version equivalence policy permits it; distinguish optional advice from blocking gates. Alternate paths are authored template variants initially, not an arbitrary constraint solver.
4. **Pacing:** sum remaining mandatory activity estimates without counting the same task twice; include practice/project/review waiting time separately. Present lower/upper ranges; compute dates using learner timezone and round up. Zero hours pauses dates; impossible target date yields choices, not fabricated feasibility.
5. **Mutation:** lock user/roadmap on acceptance, use transactions for attempts/evidence/unlocks, and enforce one active roadmap at DB level. Never trust user IDs, scores, completion dates, reviewer roles, or model output sent by the client.
6. **Prior knowledge:** self-report helps choose challenge opportunities; it does not award evidence. Passing a knowledge challenge can waive matching learning tasks, while practical gates need appropriate project evidence or human-reviewed prior work. Learners may read ahead while unmet demonstration gates remain visible.
7. **Progress:** calculate activity completion as completed required activities / all required activities for the pinned release; show numerator and denominator. Show assessed knowledge and practical criteria separately. No career-readiness percentage in MVP.
8. **Graph validation:** lock draft release during validation/publication, enforce membership and self-edge checks, run cycle detection on the entire release, and disallow mutation after publication. Do not rely on `Model.clean()` being invoked by every write path.
9. **Safe updates:** resource health warnings may overlay pinned metadata immediately; replacement content requires a reviewed revision with attribution. Preserve old link/title in history and explain changes. A revoked assessment is annotated; do not erase the original attempt.

State transitions are explicit service rules. Roadmaps move proposed → active → paused/archived, with expired proposals ineligible for acceptance. Activities move available → in_progress → completed; undo adds a reversing record. Availability is derived from gates and is not a learner-writable flag. Attempts move in_progress → finalized (or abandoned), and finalized answers cannot be patched. Submissions move draft → submitted → needs_revision/accepted; revision creates a new submission version. Evidence corrections append a superseding/revoking decision. If a prerequisite's evidence is revoked, preserve completed downstream work, explain the gap, and require review before new gated demonstrations; never silently erase completed steps.

### Migration from current models, after approval only

Inventory real data and back it up. Add new identities/version tables alongside existing fields; map each existing career and skill with stable IDs; create legacy curriculum snapshots; preserve attempts/submissions against legacy versions. Existing quiz-derived `MASTERED` values become **legacy knowledge evidence**, not fabricated reviewed practical competence. Existing `is_completely_free=True` becomes “unreviewed legacy classification” until a human confirms it. Reconcile counts and references; test rollback/restore. Switch reads/writes only after validation; remove legacy columns in a later approved release. Never rewrite applied initial migrations to hide the transition.

## Resource verification and governance

Model access separately: `free`, `audit_free`, `limited_free`, `trial`, `freemium`, `partially_paywalled`, `paid`, `unknown`; separate certificate cost, login requirement, region, language, accessibility, reviewer, reviewed_at, provider update date, rights/attribution notes. A paid certificate does not make free course content paid; a free trial is not an eligible required free route. For limited/audit resources, review that the necessary objective is achievable without payment. Unknown pricing cannot satisfy required publication checks.

Lifecycle: draft → automated validation → human review → published → flagged/reviewed replacement or archived. Publication status, access classification, and observed reachability are independent fields. Curator records how free access was checked, in which region, when, and with what login conditions. AI suggestions enter draft only. For YouTube, store link/title/provider and permitted metadata; prefer captions/transcripts where available without claiming accessibility if unverified. Do not download/rehost videos or scrape captions by default.

Proposed checks: pre-publication URL validation; weekly reachability for active required resources; monthly human access review for pilot content; on-demand triage from reports. Check at most one request per provider per second, respect Retry-After, robots/provider terms where applicable, and pause a provider on repeated 429/403. An inaccessible automated check is “unverified/restricted,” not proof the source is broken. Bound attempts (three, spaced with backoff) and surface jobs that remain unresolved. The local scheduler only runs when the machine is on; catch up bounded due batches without a retry storm.

Fetcher controls: only reviewed provider hosts and HTTPS/approved HTTP; reject credentials in URLs, unsafe ports, IP literals and nonpublic IP ranges; validate every redirect (maximum three), DNS resolution and actual connection destination; block metadata/private networks including IPv6. Keep network egress restricted, TLS verification enabled, timeouts/response-size limits, and no ambient credentials/cookies. Do not fetch arbitrary submission links. These controls follow the threat described by [OWASP SSRF guidance](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html).

Store status, timings, redirect observations, errors and minimal metadata, not complete provider content. HTTP 200 is only reachability; paywall hints create a review task. Replacement preserves the user's progress and history. Admin notification is an in-app queue initially; optional email later.

## I. AI architecture

### Responsibilities and boundary

MVP modes: explain a concept, give a hint, suggest the next approved activity, and ask a formative practice question. Quizzes generated in conversation are practice only. The server handles prerequisites, scheduling, scoring, authorization, resource selection, publication and evidence decisions deterministically. The model cannot execute code, browse URLs, call admin tools, grade for credentials, change roadmaps, or read other accounts.

Request path: authenticate → authorize task/roadmap → validate and bound input → reserve one request slot → load minimal allowed context → call selected local model → validate response → map source IDs to approved URLs → persist bounded conversation/result → release slot. Return visible queued/running/error state. Use an `AIRequest` row and a single lightweight worker polling it for this local prototype; this is the one job that needs interactive background execution, separate from daily scheduled checks. Lease expiry and reconciliation handle a crashed worker. Do not introduce Celery/Redis for one concurrent generation.

Context includes current objective, relevant reviewed resource metadata or licensed short excerpts, task instructions, limited recent messages, and a concise owner-only progress summary if needed. No email, legal name, complete history, answer keys for active assessments, or private project contents unless the user explicitly chooses that coaching context. Fetch by relational IDs, not vector search. Treat all user/retrieved content as untrusted data. Keep stable instructions separate and never interpolate learner text into privileged instructions.

Adapter input: task enum, bounded messages/context, timeout, output schema, model configuration. Output: status, answer, allowed source IDs, optional next activity ID, uncertainty note, usage, model/prompt version. Prefer a simple JSON shape but independently validate it; schema conformance does not establish truth. Sanitize Markdown; no raw HTML or arbitrary links. Resolve citations from known resource IDs and reject unknown IDs. A structurally invalid/refused/empty response is an explicit unavailable/retry outcome, never a simulated success.

### Local feasibility and controls

The inspected machine reports roughly 16.7 GiB total RAM and approximately 3.8 GiB available at inspection, with a Ryzen 5 PRO 3500U CPU. Ollama is not installed; NVIDIA tooling was not present, which does not establish whether any acceleration is usable. This is capacity evidence, not a benchmark or a deployment requirement. Available memory changes, and no machine-specific path belongs in configuration.

P0 should evaluate a currently supported, appropriately licensed small quantized instruction model, initially in the approximate 1–3B parameter class, with short contexts. Do not select by parameter count alone. Record license, model digest, download size, peak RAM, time-to-first-token, total latency, refusal behavior, and teaching/citation quality. A larger model is considered only if it fits existing hardware. No new hardware purchase or paid inference is authorized.

Provisional bounds: one local inference at a time, queue at most five requests, one pending request per learner, ten replies per learner/day, 2,000 characters of user input, approximately 2,000 input and 400 output tokens, 90-second hard deadline. Test and adjust only within observed resources. Busy returns an honest busy state; quota exhaustion shows the reset time and preserves learning access. Retry transient failures at most once within the same reserved budget; no automatic retries after an ambiguous completion that could duplicate work. Cancellation and timeout must release leases and prevent unbounded background computation.

Disable cloud features and use an explicit local model allowlist. Configuration must reject cloud endpoints in zero-spend mode. No third-party analytics receives prompts. Local inference reduces external transfer, but application logs, backups, reviewer access, and model output still require privacy/security controls.

### Evaluation gate

Create at least 40 synthetic or consented, de-identified cases: both launch pathways, novice and experienced explanations, incomplete context, hint requests, deliberate misconceptions, requested invented links/certificates, prompt injection, cross-user IDs, and assessment-answer requests. Include a non-tech fixture to check generic architecture. Use expert rubric ratings for correctness, usefulness, appropriate hints, uncertainty and source support. Evaluate local model candidates on identical cases; no paid benchmark calls in this phase.

Proposed acceptance: zero cross-user disclosures/privileged actions in the adversarial suite, every rendered source mapped to supplied approved IDs, at least 90% schema-valid successful responses, and at least 80% reviewer-rated useful/correct explanations with no critical unsafe advice. Measure coverage and sample size; finite passing tests do not prove safety. Re-run on prompt/model/content-policy changes. Target median complete reply within 30 seconds and p95 within 90 seconds on the actual device; if infeasible, report results and reconsider scope with the owner. These are goals, not observed performance.

If local inference fails quality or hardware limits, pause the AI deployment decision. Options for owner review are narrower contextual hints, an explicitly approved free cloud tier with acceptable data terms and hard nonbilling limits, or a revised budget. A canned reply is not a substitute for the requested AI feature.
