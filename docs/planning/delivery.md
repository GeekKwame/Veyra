# Security, quality, operations, and delivery plan

Status: proposed for review. No phase is authorized by the existence of this plan. The budget constraint is zero new operating expenditure; the immediate target is a supervised local prototype, not an always-on public service.

## J. Security and privacy

### Trust boundaries and permissions

The browser, submitted text/URLs, model responses and external resources are untrusted. Django is the authority for identity, ownership, publication, workflow state, grading and evidence. PostgreSQL, the local model runtime, verification jobs and backup storage are private services. The model has no privileged tools and no direct database access.

| Actor | Allowed | Explicitly excluded |
|---|---|---|
| Visitor | Read published curriculum/resources. | Drafts, answer keys, learner records, admin. |
| Learner | Own profile, roadmaps, attempts, submissions, evidence, AI conversations, data-rights requests. | Role changes, setting scores/verification, another learner's identifiers, public evidence sharing in MVP. |
| Curator | Draft/edit content, validate drafts, triage resource reports. | Learner transcripts/submissions merely by being a curator, security/role changes. |
| Publisher | Approve reviewed content release; archive or replace resources. | Alter historical evidence or bypass content checks. |
| Assigned reviewer | Read assigned submission and rubric; issue attributable feedback/review. | Browse unrelated learner records or private AI history. |
| Administrator | Manage staff permissions and specific support/security actions. | Unlogged support access; treating a role label as an authorization check. |
| Scheduler/AI worker | Execute bounded leased jobs with minimum required DB/network permissions. | Arbitrary shell commands, arbitrary URLs or cloud fallback, user/admin impersonation. |

Use Django groups/permissions as the authority; a UI role string is descriptive only. Deny private routes by default and explicitly grant public access. Scope querysets before object lookup; check relationships as well as IDs. Curators and reviewers can be the same human in a small prototype, but assigned permissions and recorded actions remain distinct. Add staff MFA before remote administrative access, or prohibit remote admin until an appropriate zero-spend method is configured.

### Threat and mitigation register

| Threat | Controls in proposed MVP | Evidence required |
|---|---|---|
| Cross-user reads/writes (IDOR) | Owner-scoped queries for every private resource and nested relationship; avoid trusting payload owners; private cache control. | Two-account negative tests for GET/PATCH/list/export/submission/AI request and guessed IDs. |
| Role escalation / mass assignment | Separate read/write DTOs, explicit allowed fields, role changes restricted to audited admin service. | Learner cannot PATCH role, grade, reviewer, verification or timestamps. |
| Session theft, credential abuse, enumeration | HttpOnly session; CSRF on all unsafe routes including login; generic auth errors; password validators; throttles; session rotation/revocation. | CSRF requests fail, login response does not distinguish known emails, logout/reset revokes sessions. |
| XSS and malicious external links | React escaping; sanitized restricted Markdown; no raw HTML; HTTPS-link validation; `noopener` and referrer policy; CSP before remote use. | Malicious text/Markdown/URL fixtures render inert, with no script execution or token disclosure. |
| SQL injection | ORM/parameterized queries and constrained filter/sort fields. | Fuzz malformed identifiers/filters; no SQL strings composed from user data. |
| SSRF from resource checks | Reviewed provider allowlist, destination validation at connection time and on redirects, private-network egress blocked, size/time limits; no submission fetching. | DNS rebinding/private IPv4/IPv6/redirect/metadata tests; no requests to forbidden targets. |
| Prompt injection / context contamination | Untrusted data separated from instructions, relational authorization before retrieval, minimal context, no model tools, strict allowed source IDs and output validation. | Cross-user, hostile resource, “ignore instructions,” fabricated-source and assessment-answer evaluation cases. |
| Incorrect or unsafe learning claims | Reviewer-approved objectives and rubrics; factual source labels; no job/accreditation guarantee; knowledge separated from practical evidence. | Content checklist and expert review; critical unsafe output blocks model release. |
| Race conditions and lost history | Transactions, row locks, version preconditions, unique active roadmap, immutable submitted/published versions, idempotency. | Concurrent acceptance/grading/publication, retries and migration history tests on PostgreSQL. |
| Resource or compute exhaustion | Input length limits, pagination, DB/HTTP timeouts, bounded queues, one inference worker, per-user quotas, cancel/lease recovery. | Queue saturation and slow-model tests; core learning remains responsive. |
| Dependency/configuration exposure | Supported pinned versions, checked lockfiles, secret scanning, debug/secret fail-fast outside local mode, least-privilege DB user. | Reproducible install, vulnerability review, configuration checks; no secrets in Git. |
| Sensitive logging/backups | Redaction, minimal identifiers, limited access/retention, encrypted backups and explicit deletion handling. | Inspect logs/export/backup access; restore/deletion drill. |
| Malicious files | No uploads or execution in MVP. | File endpoints absent; external links not auto-downloaded. |

For later uploads: private object storage, authenticated short-lived access, MIME/magic-byte checks, size limits, quarantine and malware scanning, no executable rendering, content-disposition attachment, and deletion lifecycle. These requirements do not justify building upload infrastructure now.

Session cookies and CSRF solve different problems; SameSite alone is insufficient. The plan follows the separation described in [OWASP CSRF guidance](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html). Exact CSP and proxy/header settings must be tested against the chosen deployment, not copied blindly from development defaults.

### Data minimization and retention proposal

Collect display name, email/test identifier, password hash, timezone, availability, selected goals, learning actions and submitted evidence. Optional experience/accessibility preferences have a stated purpose and can be omitted or deleted. Do not collect exact date of birth, health information, national IDs, financial records, employer secrets or real customer datasets for learning exercises. Use public/synthetic datasets and remind learners to redact private material.

No private submissions are sent to external models or used for training under the local-only design. Model runtime must be configured with cloud disabled; local model weights and license are reviewed. A future cloud adapter requires an explicit privacy/subprocessor decision before any private transfer. Marketing analytics and session replay are excluded.

All periods below are **proposed product policy**, not claims of compliance with a jurisdiction's law:

| Data | Purpose / proposed retention | Deletion and access |
|---|---|---|
| Profile, roadmaps, attempts, submissions, reviews, evidence | Provide learning history for active account. | Owner access; assigned reviewer minimum access. Delete live personal records within 7 days of confirmed deletion; immediately revoke sessions and hide account. |
| AI conversations/messages | Short contextual continuity, default 7 days. | Owner can delete earlier; purge message content. Do not retain in routine logs. |
| AI/job usage metadata | Diagnose local failures and enforce limits; 30 days. | Pseudonymous request/model/token/latency/status data; no prompt bodies. |
| Application logs | Operational diagnosis; 7 days with local rotation. | Operator only; mask email, credentials, private URLs, answers and query-string secrets. |
| Security/audit events | Accountability; 90 days. | Staff-restricted; minimal actor reference; delete/anonymize personal identifiers when no justified retention applies. Publication authorship may require distinct agreed attribution. |
| Resource verification records | Trend/triage; 90 days of observations, latest human review retained with current resource revision. | Staff details; public status only. No downloaded provider bodies retained by default. |
| Data export | User-controlled portability; expires after 24h. | Authenticated owner-only download; encrypted temporary storage if written to disk. Delete after expiry. |
| Encrypted backups | Recovery; rolling 30 days maximum. | No general access. Deleted records can persist until expiry; restore procedure reapplies deletion records before serving traffic. |
| Proposed roadmaps / idempotency records | Review/retry support; at least 24h. | Expired proposals cannot activate; idempotency contains response metadata, not passwords. |

Account deletion: recent reauthentication and confirmation → disable account/revoke sessions → cancel pending AI/jobs → remove live private records and exports → scrub permitted log references → preserve only minimal justified deletion/audit record → expire backups. A restore must replay the deletion ledger before access resumes. Do not claim deletion of user-owned documents hosted at third-party providers; explain that boundary.

Export includes the user's profile, roadmap versions, activity history, attempts/results, submissions, feedback, evidence and retained conversations in documented JSON. Omit credentials, unreleased question banks, unrelated records and staff-private incident notes. Test exports for completeness and isolation.

Before real remote users: identify operating entity, target countries, age policy, data controller/processor roles, legal basis/notice, deletion/export handling, provider contracts and transfer rules. Obtain jurisdiction-specific review then; neither local deployment nor this checklist establishes legal compliance. Adults-only/English are provisional scope assumptions pending owner review.

## L. Testing and quality assurance

### Testing layers

| Layer | Coverage / why it matters | Proposed tooling and execution |
|---|---|---|
| Unit | Stable DAG order, required vs optional edges, time ranges, pause behavior, evidence policy, schema validation. | Existing pytest approach after dependencies are approved; fixed clock and data-driven fixtures. |
| PostgreSQL integration | Transactions, constraints, ownership, publication, concurrent attempts/enrollment, migration backfill and deletion. | pytest-django on disposable PostgreSQL; do not rely on SQLite to validate concurrency. |
| API contract | DTO shapes, pagination, auth/CSRF/errors, source restrictions, revision pins and idempotency. | DRF client + OpenAPI contract validation; generated TS typecheck as part of the same change. |
| UI components | Forms, busy/error/empty states, keyboard controls, retry preservation. | React Testing Library with an approved lightweight test runner; test behavior, not internal state variables. |
| End to end | Full learn/practice/project/review flow in both selected pathways, return session and schedule adjustment. | Playwright against real local API/DB with synthetic accounts; deterministic AI stub only in explicitly labeled automated tests. |
| Accessibility | Keyboard, focus, labels, error association, zoom/reflow, contrast and screen-reader flow. | Automated axe checks plus manual keyboard/screen-reader review at 320px and 200% zoom. |
| Security | Ownership-negative matrix, CSRF, mass assignment, SSRF, XSS and dependency/configuration checks. | Regression fixtures plus manual threat review; report scanner findings, not “secure because tests pass.” |
| Performance | Core route latency, SQL counts, bounded payloads, simultaneous local reads and one AI generation. | Repeatable local load script; record hardware/conditions; measure before tuning. |
| AI evaluation | Teaching quality, source fidelity, prompt injection, uncertainty, model failure and cancellation. | Fixed 40-case minimum suite and human rubric; no private production data by default. |
| Resource verification | Redirects, 429/403, transient timeout, changed domain, missing pricing, human-review lifecycle. | Controlled HTTP/DNS fixtures; don't hammer real providers in CI. Manual source checks remain required. |

Dependency/test-tool installation happens only after implementation approval. No new tests were added or application suites run in the planning phase; actual discovery checks are recorded separately.

### Acceptance scenarios

| ID | Observable acceptance scenario |
|---|---|
| AC1 | Beginner chooses an approved tech pathway, reviews/accepts a plan, opens a genuinely free resource, completes practice, submits a project and reads feedback. Every selected pilot pathway supports this entire loop. |
| AC2 | A → B → C prerequisites start with A available; B unlocks only after its configured required evidence; optional edges do not block. Stable ordering and cycle rejection hold at publication. |
| AC3 | Required resources have human-reviewed permitted free access, provenance, check date and visible restrictions. Trial/unknown/paid-only material cannot be the sole required route. HTTP 200 never automatically sets free/reviewed. |
| AC4 | Marking a resource complete changes activity completion only. Passing a quiz creates knowledge evidence. Only appropriate rubric-reviewed practical work creates practical demonstration. No readiness percentage is fabricated. |
| AC5 | Experienced learner challenges an objective, gains only supported credit, and avoids redundant eligible learning while preserving unmet practical requirements. Repeated quiz attempts never erase earlier attempts. |
| AC6 | Changing hours or pausing preserves completed steps, scores, submissions and pinned releases. Duplicate acceptance or stale schedule edits cannot produce two active roadmaps or lost updates. |
| AC7 | A failed/paid/restricted resource is flagged, reported and reviewed; a replacement is attributable. Existing roadmap progress and original history survive the change. |
| AC8 | User A cannot read, list, change, export or use AI context from user B's profile, roadmap, attempt, submission, evidence or conversation, even by guessing UUIDs or nesting another user's IDs. |
| AC9 | Safe profile fields are editable; roles/grades/reviewer identity are not. Missing CSRF fails; logout invalidates session; anonymous login errors do not reveal account existence. |
| AC10 | Real local model produces evaluated task-contextual assistance. Busy, cancelled, invalid-output, unavailable and quota-exhausted states are truthful. No cloud call occurs in local-only mode; saved learning remains usable. |
| AC11 | A curator adds an internal non-tech lesson-planning fixture using the same objectives, resource, project and assessment services with no profession-specific branches. Public catalog stays tech-focused. |
| AC12 | Core journey works by keyboard/screen reader, at narrow widths and zoom, with clear focus/errors. Text instructions remain usable without playing video; no autoplay or required heavy graphics. |
| AC13 | Migration rehearsal preserves counts/relationships; published content changes do not rewrite past attempts. Backup restore reproduces a known checkpoint and reapplies deletion records before access. |
| AC14 | Owner export is complete and private; confirmed deletion disables access immediately and meets documented live/backup retention. Pending jobs cannot recreate deleted user data. |
| AC15 | All displayed features/links are real, no fake model success or unsupported verification claims, production-only gates are explicit, logs redact sensitive data, and zero-spend mode cannot call paid services. |

### Proposed non-functional targets

For the local prototype, measure core API p95 below 500ms under five simulated users, excluding external resources/model inference; error rate below 1% for valid requests during that bounded run. Prefer public page usable content within 3 seconds on a measured throttled connection, with no initial video payload. Report failures and device conditions rather than generalizing to internet-scale performance. A heavy local model may invalidate these targets; test the combined workload in P0/P5.

AI target is median reply within 30s and p95 within 90s, one generation at a time, subject to model quality. No public availability SLO. Save success means committed server state, not a frontend animation. All write retries must be safe. A prototype only passes if its essential learning loop works even when optional assistance is temporarily unavailable.

## M. DevOps and observability

### Environments and delivery workflow

Local development → disposable automated test environment → local release-candidate environment → supervised prototype. A future staging → production path remains documented as a gate, not deployed infrastructure. Separate DB names, secrets, test users and ports; do not copy private learner data to tests. Only one resource-heavy environment/model need run at a time to stay within available RAM.

Propose short-lived branches and reviewable changes with one logical outcome. Preserve user work. Commit/PR/merge rules require owner approval; do not auto-merge. No repository commits are made in the planning phase. Use the same reproducible local verification commands as a later CI workflow. Hosted CI is only enabled after checking that its quota/settings cannot introduce charges; local checks remain the zero-spend baseline.

Before each phase is considered complete: type/lint checks appropriate to changed code, focused behavioral tests, contract checks, source/dependency review, documentation updates, and a concise acceptance report. Before prototype release: full critical regression suite, browser journey, accessibility review, model evaluation, content sign-off, migration/restore rehearsal. Do not repeat expensive suites without a change or new risk justifying it.

Lock Python/Node dependencies and supported runtimes; record model digest/license separately. Use documented example variables, never credentials or local absolute paths. Production settings must fail on debug, default secrets, untrusted hosts, unintended SQLite, unsafe proxies, or cloud endpoints in zero-spend mode. Local mode is explicit, not inferred because a key is missing.

### Database changes and rollback

Use additive migrations first, then backfill and validate, then switch readers/writers, then separately remove legacy fields. Run migrations once per deployment, with a backup, lock/maintenance plan and compatibility check. Test both a fresh database and migration from representative existing state. Never use initial-migration edits as a shortcut for unknown real data.

Pin a release artifact/commit and its migration version. Application rollback is safe only while schema compatibility is preserved. For destructive/data-transforming failure, prefer a forward correction or restoration into a fresh DB rather than an untested reverse migration. Record downtime/data-loss implications and involve the owner before destructive recovery. The plan itself does not authorize deleting or restoring over a live database.

### Local process and job operations

Use documented start/stop commands or a small process supervisor after approval; bind DB/AI to loopback. Expose only the application origin locally. Health checks distinguish process liveness from readiness of PostgreSQL; AI readiness is separate so it cannot make saved roadmaps unavailable. Worker state uses leases, heartbeat and bounded retries; stale runs return to a recoverable state without duplicating finalized work.

Resource checks run in bounded scheduled batches; catch up due work after the computer restarts. AI uses a single bounded worker for interactive requests. Deletion/export/cleanup jobs can run in scheduled commands with durable state. If existing job code cannot meet the needed guarantees simply, revisit a lightweight queue before implementing a bespoke general job framework.

### Backup and recovery

Proposed local backup: encrypted PostgreSQL dump every day with writes and before migrations, retain up to 30 days, check completion/checksum, and perform a restore into an empty test DB before the first real-user session and after material schema changes. Include app configuration instructions, model digest/prompt versions and deletion ledger; do not copy plaintext secrets into documentation.

Target recoverability is the last successful daily snapshot (up to 24h of activity loss while operating), and a four-hour restore target on working existing hardware. These are unproven targets until drilled. A backup on the same disk does **not** survive device loss. If no existing independent storage is available at zero cost, explicitly limit the prototype to disposable/test data or accept documented loss risk; do not advertise durable production storage. No paid backup subscription is assumed.

Restore procedure: isolate new DB → verify backup → restore → apply deletion ledger and current access restrictions → run reconciliation/critical smoke checks → switch application connection → observe → retain old state until authorized cleanup. Document who can decrypt, where recovery instructions are held, and how to revoke access.

### Operational signals and incident handling

Use structured JSON logs with event, timestamp, severity, request/job ID, route template, duration, safe user reference, status and error code. Exclude passwords, tokens, full URLs with secrets, prompts, answers and artifact contents. Keep logs local and rotated initially. No paid telemetry service or large metrics stack is required.

| Signal | Trigger / response |
|---|---|
| API latency/errors | Investigate sustained failure or p95 target breach during supervised use; inspect correlation IDs and SQL timing. |
| DB health/storage/backups | Alert locally if backup fails, DB unavailable, or disk space threatens operation; stop nonessential model/verification work first. |
| Resource checks | Show overdue checks and material access changes in curator queue; distinguish provider blocking from genuine removal. |
| AI queue/latency/failure | Queue depth, runtime availability, invalid-output count, peak memory, timeouts and cancellation failures; disable new generations on repeated failures. |
| Zero-spend policy | Startup configuration check plus tests rejecting external model endpoints; any unexpected cloud attempt is a release blocker. |
| Security | Repeated auth/authorization failures, staff changes, suspicious source destinations; avoid logging credential values. |
| Content/review health | Outstanding publications, unreviewed projects, aged reports and reviewer turnaround; cap new enrollment if review capacity is exceeded. |

Local alerts can be a status page/admin queue/console indicator during supervised sessions. They are not 24/7 monitoring. Before public launch name an incident owner and arrange a sustainable notification channel.

Incident runbooks: disable mentor independently; pause verifier/provider; temporarily withdraw a resource with history retained; contain suspected account access and revoke sessions; restore a database; reconcile stuck jobs; investigate cost-policy violation. Capture what happened, affected data and recovery, then add a regression test where appropriate. Security/privacy incident notification requirements must be established for the actual market before external launch.

## N. Implementation sequence

Relative effort: S = contained change; M = several coordinated workflows; L = substantial domain/UI work. These are not dates. Reviewer/content effort is additional. Each phase ends with a reviewable result, executed checks, known limitations and updated docs. Approval can cover one phase at a time.

| Phase | Objective and deliverables | Likely modules/files | Dependencies | Tests / acceptance gate | Risks / effort |
|---|---|---|---|---|---|
| P0 — establish feasibility | Confirm real-data/deployment status; reproduce baseline with approved dependency installation; preserve data; evaluate a local model/license on representative tech explanations; record actual memory/latency/quality and zero cloud calls. Create minimal regression cases for priority defects. | Requirements/lockfiles, test configuration, `docs/evaluations/`, isolated local model evaluation script; no broad feature implementation. | Explicit planning/phase approval; existing hardware; provisional sample content. | Existing suites executed with honest failures; local model evaluation evidence; fresh DB only. If useful AI cannot fit, stop dependent AI commitment for owner decision. | CPU/RAM/model quality, dependency drift; M |
| P1 — safe foundation | Supported dependencies; secure account/profile/session contract; fix catalog contract, role mutation, graph direction, enrollment transaction and misleading mentor success; establish local settings and check commands. | `backend/veyra_core`, accounts, careers/roadmaps regressions, mentor availability boundary; frontend API/auth; examples/README. | P0, auth/stack ADRs. | AC2/AC8/AC9/AC15 focused tests; frontend can consume actual catalog response. No fake integration remaining. | Compatibility with unknown data/clients; M |
| P2 — trustworthy curriculum | Shared skills and path mappings; immutable releases; resources/access/history; reviewed publication/admin; first reviewer-backed tech content and internal non-tech fixture; migration mappings. | careers/curriculum, resource verification module/commands, admin, migrations, fixtures/content docs. | P1, actual reviewer commitments, domain approval. | AC3/AC7/AC11/AC13; draft leak, graph, pricing/SSRF cases; content coverage checklist signed. | Content rights/reviewer time; L (content is separate) |
| P3 — designated roadmap journey | Short onboarding, proposal/acceptance, next step, scheduling/pausing, activity tracking, honest dashboard and responsive navigation. | roadmaps services/API, frontend onboarding/dashboard/task views, reusable UI primitives. | P2, approved contracts. | AC1 through practice portion; AC2/AC6/AC12, duplicate/stale update tests. Completed activity history preserved. | Scheduling complexity and frontend state; L |
| P4 — practical evidence | Formative checks and prior-knowledge challenge; project drafts/submission/revisions; assigned human review; evidence projection and UI. | assessments, projects/evidence, admin, frontend learning/project/evidence views. | P2–P3, authored questions/rubrics and reviewer capacity. | Full AC1/AC4/AC5/AC8 and history/concurrency cases; no quiz-only practical mastery. | Review workload, ambiguous rubrics; L |
| P5 — real bounded AI assistant | Local-only adapter, context authorization, bounded request queue/worker, validated sources/output, visible busy/cancel/error states; task-integrated panel. | mentor services/DTOs/request records/worker, frontend mentor panel, evaluation cases. | P0 feasibility passed, P3 context, P4 evidence policy where used. | AC10 and injection/isolation/source tests; measured local performance; no cloud access or hidden paid fallback. | Local model quality and memory contention; M–L |
| P6 — prototype acceptance | Export/deletion/retention; backup/restore; remaining observability and runbooks; full linked journey, accessibility and content review; local release instructions. | accounts/privacy jobs, operations commands, browser tests, docs/runbooks, all changed workflows. | P1–P5. | AC1–AC15; restore/deletion drill; zero-spend configuration; reviewer sign-off. Only then invite supervised testers. | Test-data privacy, durable storage limits; M |
| Later external-launch gate | Assess hosting, email, TLS, region/privacy, monitoring, availability and remote AI feasibility under still-approved budget. | Deployment/operations/configuration and policy docs. | Separate owner decision after local results. | Real external end-to-end and recovery tests; no paid service assumed. | Free-tier instability and hidden cost; not part of authorized prototype scope |

If only one expert reviewer/pathway is available, deliver one complete public tech pathway and keep cross-profession extensibility acceptance in fixtures; do not invent a second reviewer or publish unchecked content. Add the second pathway when it meets the same acceptance bar. This is a proposed reduction from the original breadth, consistent with the owner's reviewer-led launch direction.

## O. Engineering backlog

Priority: P0 = blocks safety/feasibility or core journey; P1 = required for complete prototype; P2 = deferred improvement. Entries are proposed tasks, not created external tickets. Dependencies reference backlog IDs or phases.

| Epic / feature | Tasks and priority | Dependencies | Done when |
|---|---|---|---|
| E01 Feasibility / reproducibility | B01 P0: inventory real data, approved environments, install/lock versions, execute baseline. | Approval | Actual check results and constraints documented; no existing data overwritten. |
| E01 Local AI viability | B02 P0: shortlist licensed small models; download only after approval; evaluate memory/quality/latency with cloud disabled. | B01 | Reproducible evaluation supports a useful local option or records a concrete decision blocker. |
| E02 Identity / authorization | B03 P0: safe profile DTO, permissions, session+CSRF, generic auth errors, registration validation. | B01 | AC8/AC9 pass; role labels cannot grant privileges. |
| E02 Correctness repairs | B04 P0: fix list pagination/client mismatch, edge directions, enrollment atomicity, fake mentor success and unsafe public querysets. | B01 | Regression cases fail before fix and pass after; existing data preserved. |
| E03 Curriculum / versions | B05 P0: shared skill mapping, immutable releases, objective/evidence policies, graph validation and migration mapping. | B04 | AC2/AC11/AC13; legacy data meaning preserved and labeled. |
| E03 Content production | B06 P0: select reviewer-backed tech pathway(s); write objectives/tasks/projects/rubrics; review source rights/free access. | Reviewer identification, B05 | Every published objective has a learn/practice/evidence route; reviewer and review date recorded. |
| E03 Publishing | B07 P1: curator/publisher admin, validation report, preview/diff, publish/archive audit. | B05–B06 | Drafts inaccessible publicly; release publication validated and immutable. |
| E04 Resources | B08 P0: access taxonomy, revision/health split, public resource DTOs and reports. | B05 | AC3/AC7; paid certification/trial/login distinctions visible. |
| E04 Verification | B09 P1: safe fetcher, redirect/DNS controls, bounded scheduled jobs and curator triage. | B08 | Simulated provider failures handled safely; no automatic quality/free certification. |
| E05 Roadmaps | B10 P0: deterministic proposal/acceptance, credit rules, one-active constraint, schedule preview/patch/pause. | B05–B08 | AC2/AC6; stale/duplicate requests safe. |
| E05 Learner UI | B11 P1: onboarding, dashboard, task list, resources, progress states, meaningful errors/empty states. | B03, B10 | Beginner resumes and completes practice on mobile/keyboard with saved state. |
| E06 Knowledge checks | B12 P1: versioned questions, attempt lifecycle, server scoring, prior-knowledge policy and feedback. | B05, B10 | AC4/AC5; answer IDs validated; results do not grant practical competence. |
| E06 Projects / reviews | B13 P1: generic artifact submissions, revisions, review permissions/rubric validation, feedback interface. | B06, B11 | Full create/review/revise loop; owner/assigned reviewer access only. |
| E06 Evidence | B14 P1: provenance records, policy projection, history UI and revoked/superseded annotations. | B12–B13 | Source/version visible; no unexplained mastery/readiness score. |
| E07 AI integration | B15 P1: local adapter, relational context, request leases/worker, source validation, quotas, cancel and UI. | B02, B10–B11 | AC10 passes with actual local model; invalid/absent output never appears successful. |
| E07 AI quality | B16 P1: 40+ evaluation cases, expert scoring, regression report and model/prompt pinning. | B06, B15 | Meets agreed evaluation gate on existing device; limitations explicit. |
| E08 Privacy | B17 P1: export, deletion ledger, transcript/log retention, reauthentication, cleanup jobs. | B03, B12–B15 | AC14 including pending jobs and restore re-deletion. |
| E08 Operations | B18 P1: health checks, job/backups status, structured redacted logs, restore script/runbook. | B05, B09, B15 | AC13/AC15; recoverability measured; same-disk limitation disclosed. |
| E09 Quality / release | B19 P1: full browser flow, accessibility/performance checks, zero-spend enforcement, documentation accuracy. | B11–B18 | All critical ACs verified with observed results; supervised test instructions complete. |
| E10 Later capabilities | B20 P2: discovery questionnaire, reminders, uploads, extra pathways, public hosting feasibility. | Pilot feedback, explicit scope decision | Separate brief, budget/privacy approval and acceptance criteria before implementation. |

Content backlog per selected pathway: role scope → 6–8 draft skills → observable objectives → prerequisite graph → reviewed resource/fallback links → practice activities → eligible knowledge checks → project brief and 3–5 anchored rubric criteria → free/accessibility review → learner walkthrough → publication sign-off. Track reviewer time as a real dependency even when voluntary; zero operating spend does not establish free expert labor.

## Documentation plan

Keep this proposal labeled proposed. After each approved implementation phase, update real behavior rather than claiming future features exist.

| Artifact | Owner / delivery point | Required content |
|---|---|---|
| Root README | Engineer / P1 onward | Actual status, prerequisites, working ports/start commands, tested versions, known limits; distinguish local prototype from hosted product. |
| Product requirements / journeys | Owner + engineer / approval and scope changes | Confirmed scope, personas, acceptance, exclusions, decisions. |
| Architecture/ADRs/domain/database | Engineer / P2 changes | Actual entity relationships, transactions, indexes, revision policy and selected alternatives. |
| API docs / generated types | Engineer / each API phase | Actual schemas, auth/errors, examples, versioning and compatibility. |
| AI architecture/evaluation report | Engineer + reviewer / P0 and P5 | Runtime/model/license, prompt versions, context/privacy controls, measured results and failure behavior. |
| Security/privacy model | Engineer + owner / P1–P6 | Access matrix, threat model, retention, data rights and external-launch legal gaps. |
| Local development/configuration | Engineer / P1 | Reproducible setup, placeholder environment examples, local-only defaults, no absolute workstation paths. |
| Test/contribution guides | Engineer / P1 onward | Commands, fixture policies, meaningful test boundaries, branch/review rules after approval. |
| Migration/deployment guides | Engineer / P2–P6 | Fresh vs existing DB paths, compatibility, local release procedure; external deployment remains explicitly unimplemented. |
| Backup/recovery and runbooks | Operator / P6 | Tested restore, key/access handling, job recovery, AI shutdown, resource incident, deletion replay. |

The final phase report must state what changed, checks actually run, failures/limitations and the next reviewable step. Passing a small suite does not establish production readiness. After the planning package is presented, stop for explicit implementation approval as required by the product brief.
