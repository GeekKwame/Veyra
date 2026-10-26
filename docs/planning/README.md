# Veyra planning package

Status: **Proposed — awaiting product-owner review. Implementation is not authorized.**

Repository discovery and source checks: 2026-10-23 against commit `13623bd`. Planning package completed 2026-10-25, incorporating the owner's clarifications. The master product brief supplied by the product owner is the requirements source. Existing code is evidence of prior work, not approval of the proposed scope or architecture. This package adds planning documents only.

## A. Executive product summary

**Veyra — Learn. Build. Become.** helps people turn a career goal into a manageable sequence of learning, practice, projects, assessment, and evidence. It serves beginners, career changers, and experienced learners who need practical direction and cannot depend on expensive training. Its central outcome is demonstrated capability, with the evidence and its limitations visible to the learner.

The product owner clarified that the initial audience is **people interested in tech**, learning from free YouTube materials and documentation through a designated roadmap with an AI feature. **Pathways will be selected based on available expert reviewers.** Recommend up to two complete tech pathways, a curated free resource library, deterministic roadmaps, basic knowledge checks, and one rubric-based project per pathway. Web development foundations and data analysis foundations are candidates, not approved selections. These are foundation pathways, not promises of full professional readiness. Retain a small non-tech curriculum fixture in architecture acceptance tests to demonstrate future breadth without expanding the public pilot.

Keep the existing Django/React investment where it fits. Repair correctness and privacy problems before extending it. Recommend Django REST Framework, a supported Django LTS, PostgreSQL, and a supported Next.js release; use Django Admin for content operations. A scheduled management command is sufficient for initial verification jobs. Redis, Celery deployment, vector search, file uploads, and a broad AI platform need not be launch prerequisites.

The clarified MVP includes a **bounded AI learning assistant**. The owner also confirmed **zero operating spend and acceptance of prototype limits**. Recommend a local prototype on existing hardware, with local-model feasibility evaluated before substantial implementation. No paid API, cloud bill, hardware purchase, or public availability guarantee is assumed. Existing electricity, connectivity, and device use still consume resources; zero spend here means no new service or hardware expenditure. AI should explain the learner's current task using authorized context and reviewed sources. It must not award mastery, invent resources, or control learner records. Saved roadmaps and progress remain available during AI outages or quota exhaustion.

## Reading and deliverable map

| Document | Contents | Brief deliverables |
|---|---|---|
| [Discovery](discovery.md) | Repository state, evidence, risks, validation limits | Phase A |
| This document | Summary, requirements, personas, scope, UX, open decisions | A–D, K, P |
| [Architecture](architecture.md) | System boundaries, technology comparisons, entities, lifecycle, AI | E–G, I |
| [API contracts](api-contracts.md) | Workflow contracts, schemas, authorization, errors | H |
| [Delivery and operations](delivery.md) | Security/privacy, tests, operations, phased delivery, backlog, documentation | J, L–O |
| [Proposed ADRs](decisions.md) | Decision records, alternatives, consequences, approval | Q |

## B. Requirements and assumptions

### Confirmed requirements

| ID | Requirement | Verification reference |
|---|---|---|
| R1 | Planning and explicit approval precede implementation; preserve existing work. | Planning-only diff; approval record before P0 |
| R2 | Career content is data-driven and reusable across professions. | AC2, AC11 |
| R3 | Core learning resources are free, with restrictions clearly disclosed. | AC3, AC7 |
| R4 | Learning, practice, projects, assessment, and evidence form one connected journey. | AC1, AC4 |
| R5 | Consumption and knowledge-check scores do not automatically establish practical competence. | AC4, AC5 |
| R6 | Roadmaps respect prerequisites and preserve completed work through adjustments. | AC2, AC6 |
| R7 | Private learner records stay private; ownership is enforced by the server. | AC8, AC9 |
| R8 | Saved learning workflows survive AI outages and exhausted quotas. | AC10 |
| R9 | Resources require human review and ongoing verification; HTTP success proves only reachability. | AC3, AC7 |
| R10 | Experience supports mobile, limited bandwidth, keyboard and assistive technology. | AC12 |
| R11 | No fabricated integrations, job guarantees, accreditation claims, or unexplained readiness percentages. | AC4, AC10, AC15 |
| R12 | Tests, backups, deployment, observability, cost controls, and accurate documentation are launch requirements. | AC13–AC15 |
| R13 | Initial audience is tech learners, with free YouTube/documentation resources, designated roadmaps, and an AI feature; reviewers determine launch pathways. | AC1, AC3, AC10; owner clarification during planning |
| R14 | Free learner access and zero operating spend, accepting prototype limits. | Local prototype default; no paid services, credits that auto-convert, or hardware purchases |

Acceptance scenario IDs are defined in [delivery.md](delivery.md).

### Provisional assumptions

These assumptions permit planning; they are not approved product policy.

| Assumption | Consequence if changed |
|---|---|
| English-language, adults-only, invitation-based pilot; launch jurisdiction unresolved. | Minors, localization, and additional markets require revisiting consent, content, support, and legal review. Do not infer the market from a developer's location. |
| Supervised local prototype: 1–5 pilot testers, sequential AI requests, no public uptime promise. | A remotely hosted or larger pilot requires a new cost, security, deployment, and capacity decision. |
| One product engineer plus part-time subject reviewers; actual capacity unknown. | Effort estimates are relative only. Human review and curriculum creation may be the critical path. |
| Existing hardware/connectivity are available without new purchases; local model feasibility remains unproven. | If a useful model cannot run within available resources, return for a narrower AI scope or approved free-provider/privacy alternative; never silently introduce billing. |
| One active roadmap per learner, with past roadmaps retained. | Multiple simultaneous goals require new dashboard and scheduling policies. |
| Up to two reviewer-backed tech pathways, 6–8 skills each, approximately 20–40 hours each. | Final pathway choice and estimates require reviewers and authored tasks; these numbers are scope bounds, not completion promises. |
| No existing production data has been established. | If real data exists, inventory, backup, compatibility, migration rehearsal, and maintenance communications become mandatory before changes. Never reset on this assumption. |

### Proposed requirements needing approval

Use reviewed curriculum releases, reusable skills, and explicit evidence levels. Require one practical project with 3–5 rubric criteria per pathway, at least one practice activity per skill, and a knowledge check where educationally appropriate. Accept text and external artifact links initially; record external link privacy limits. Review projects manually in the prototype; label self-reported work separately while review is pending. Provide account export/deletion, resource reporting, and a review queue. Use explicitly local test accounts and console email in the local prototype; real email verification/recovery is an external-launch gate, never pretend console output delivered a message.

Define completion as completion of explicit pathway requirements. Display knowledge results and reviewed practical evidence separately. Use “demonstrated against this rubric” instead of an unqualified “mastered.” Do not display the existing `readiness_score` as a meaningful career outcome.

### Out of scope for MVP

Broad career matching, public portfolios, readiness scoring, credentials, native mobile apps, social/community features, institutional tenancy, employer screening, payments, advertising, subscriptions, gamification/streaks, reminders beyond transactional email, code execution, file ingestion, image/audio AI, autonomous agents, web-browsing mentors, vector databases, and automated subjective project grading. Do not add routes or buttons for these until they work.

## C. Personas and journeys

| Persona | Need and constraint | Proposed journey and success |
|---|---|---|
| Beginner | Clear first action; limited time and unfamiliar vocabulary. | Browse a pathway without an account → see sample task and resource conditions → register → choose hours → review plan → learn → practice → knowledge check → create project → receive rubric feedback. Success: can explain and demonstrate one skill, not just mark a video watched. |
| Career changer | Recognize transferable experience without overstating it. | Compare two pathways → see typical activities and prerequisites → describe existing experience optionally → attempt relevant checks or submit prior evidence → accept a plan showing credited and remaining work → build a new artifact. Success: understands why each remaining step matters. |
| Experienced learner | Avoid unnecessary beginner lessons. | Choose pathway → opt into challenge assessment/prior work review → receive evidence-based credit for eligible requirements → keep practical requirements not yet demonstrated → start next gap. Pending evidence does not block access to reading; required practical gates remain visible. |
| Returning learner | Resume with limited attention or interrupted connectivity. | Dashboard shows last saved task and next action → resume → submit once despite retry → adjust weekly time → review changed dates. Completed work remains intact. |
| Curator/reviewer/admin | Maintain trustworthy content with limited staffing. | Draft content → validate graph and completeness → review free-access evidence → publish release → triage broken links → replace resource through reviewed revision → review assigned projects → audit decisions. Support access is explicit and logged. |

Discovery remains a distinct capability. MVP exploration is a catalog with meaningful comparisons and sample activities; it does not purport to predict career fit. V1 can add an explainable questionnaire using reviewed career attributes and qualitative reasons. Users can always reject suggestions or choose another pathway.

## D. MVP scope and later phases

| Feature | Problem / value | Classification and complexity | Dependencies / risks | Acceptance |
|---|---|---|---|---|
| Account and short profile | Saves learning across sessions. | Essential / M | Session security; local test accounts initially, real email recovery before external launch. | Register and resume; server ignores attempts to set role; console mail visibly labeled in local mode. |
| Reviewer-backed tech pathways and public exploration | Gives trustworthy starting choices for tech learners. | Essential / L content, S interface | Expert reviewers and resource rights; thin or misleading curricula. | Each pathway passes completeness checklist; a non-tech acceptance fixture uses the same engine. |
| Roadmap proposal, acceptance, pacing | Converts goal and weekly availability into next actions. | Essential / L | Versioned templates, graph validation; concurrent edits and erased history. | Explain prerequisites; reject impossible schedules; preserve evidence on changes. |
| Prior-knowledge challenge | Respects experienced learners. | Essential in narrow form / M | Reviewed checks and practical rubric; false credit. | Knowledge credit skips learning only where policy allows; practical credit needs appropriate evidence. |
| Resource library and reporting | Reduces search cost and reveals access limitations. | Essential / M | Curation and verification; paywall drift. | Every required step has a usable free route; failed links can be reported. |
| Practice and knowledge checks | Enables active recall and useful feedback. | Essential / M | Objectives, question versions; answer leakage. | Server grades pinned questions; repeated attempts retain history; no automatic practical mastery. |
| Project, review, evidence | Demonstrates applied skills. | Essential / L | Reviewer capacity, rubric, private artifacts; bottleneck. | Submit, review, revise, retain prior versions; objective-linked evidence with provenance. |
| Dashboard and settings | Shows next action and control over data/time. | Essential / M | Progress projection, export/deletion; misleading metrics. | Separates completed tasks, knowledge checks, and reviewed evidence. |
| Admin, publish review, audit | Makes content trustworthy and maintainable. | Essential / M | Permission groups, releases; accidental disclosure. | Drafts absent publicly; publication and review changes attributable. |
| Background link checks | Detects degradation without expensive manual monitoring. | Essential / M | Safe fetcher and scheduled command; SSRF/rate limiting. | Append observations; flag uncertainty; never automatically certify “free.” |
| Contextual AI learning assistant | Helps explain difficult steps in the selected roadmap. | Essential per clarification, launch-gated / M | Local inference evaluation on existing hardware; zero new expenditure. | Authorized context, no invented links, graceful unavailable state. Failure of model feasibility requires a review of scope, not a paid fallback. |
| Broad discovery and adaptive planning | Helps uncertain users and complex schedules. | Deferrable / L | Validated content attributes and behavioral evidence. | V1 only after pilot establishes need; no arbitrary match percentage. |

S/M/L represent relative engineering effort; content work is separately called out.

| Stage | Scope and rationale |
|---|---|
| MVP | Complete reviewer-backed tech pathways, conservative personalization, bounded AI assistant, private evidence, human review, usable admin, safe operations. Validates whether learners can produce and improve artifacts. |
| V1 | More pathways only with reviewers; attribute-based discovery; accessible file uploads after safe storage/scanning; opt-in reminders; richer assessments; explicit content migration previews. Each addresses observed pilot friction. |
| V2 | More adaptive planning, multi-goal scheduling, assisted project feedback with human oversight, optional portfolio publishing, localization. Require evidence of demand and operational capacity. |
| Future | Institutions, communities, mobile apps, interviews, employment integrations, sustainability options. Separate product and privacy decisions; no implementation commitment. |

### Pilot outcome measures

Use a small server-side event vocabulary with pseudonymous user IDs and no answer/message text. Count unique learners, deduplicate events, and document exclusions for staff and test accounts.

- Onboarding conversion: users accepting a roadmap / users starting onboarding within seven days.
- Activation: accepted-roadmap users completing one practice task within seven days / all accepted-roadmap users with a full seven-day observation window.
- Demonstration: learners with one reviewed practical requirement met / accepted-roadmap learners with a full four-week observation window.
- Improvement: resubmissions improving at least one rubric criterion / reviewed resubmissions; report sample size and reviewer agreement.
- Return use: activated learners completing a learning action in the following week / activated learners eligible for that observation window.
- Resource failure rate: failed scheduled observations / all completed scheduled observations; report access restrictions separately from confirmed broken links.
- AI usefulness: helpful ratings / rated mentor replies, alongside response rate, failures, and cost per useful reply. No claim that unrated replies were helpful.

For an initial five-person supervised cohort, propose a learning target of three participants completing a project and two revising successfully from feedback; interview dropouts as well as completers. If fewer people participate, report individual outcomes rather than percentages suggesting statistical confidence. These are study goals, not market-success thresholds. Compare pathways separately where both are available. Do not optimize for time spent or video counts.

## K. UX structure

Public navigation: **Explore pathways · How it works · Sign in**. Signed-in navigation: **My learning · Explore · My evidence · Settings**. Put the AI assistant inside the current task; learners can choose when to use it. Administration uses a separate permissioned interface. Avoid a dense dashboard and developer-facing language such as “DAG” in learner flows. “Public” describes published, unauthenticated content; it does not imply that the local prototype is internet-hosted.

Onboarding asks for a pathway and weekly time first. Experience and challenge options are skippable. Show a sample task before sign-up and the proposed plan before acceptance. Display estimates as ranges with assumptions; if a target date is infeasible, explain the gap and offer a narrower goal or more time. A paused roadmap has no invented finish date.

Dashboard: goal and next task first; last saved state; next milestone; distinct activity and evidence summaries; a visible way to change availability. Empty states lead to selecting a pathway. A provider outage affects only the mentor panel.

Roadmap: accessible ordered list grouped into milestones, prerequisite explanations, estimated effort, and reasons for credit or remaining work. A graph is optional decoration, never the only navigation. Review schedule changes as a small before/after comparison.

Learning workspace: objective → resource and access restrictions → practice instructions → reflection/completion action → appropriate check. External resources open explicitly; track user-reported completion rather than claiming to know whether external material was consumed. Show pending, saved, and retry states. Never discard unsent text because a fetch failed.

Project workspace: brief, deliverables, criterion descriptions, examples where licensed, submission privacy explanation, versioned submission, review status, and actionable feedback. Reviewers can request revision. No timer on ordinary practice; assessment timing is only introduced when it measures an actual objective and accommodations exist.

Settings: available time, timezone, email/account security, AI data controls if enabled, export, and deletion with clear confirmation. Portfolio visibility is private in MVP. An external document's provider controls its own sharing; Veyra must not describe a public external URL as private storage.

Admin: queues for draft validation, publication, changed/broken resources, learner reports, and assigned project reviews. Preview the exact published learner view. Show diffs, author, reviewer, publication time, and affected releases. A small pilot may use one person in multiple roles, with separate review actions and recorded accountability.

Visual proposal: deep navy foundation, blue action color, restrained teal progress accents, readable system fonts initially, generous spacing, semantic forms, persistent focus indicators, and reduced motion. No image/logo assets were found; use the Veyra name until a wordmark is approved. Final palette requires contrast testing in context. Target [WCAG 2.2 AA](https://www.w3.org/TR/WCAG22/) with manual keyboard and screen-reader checks; an automated scanner alone is insufficient.

## P. Open decisions and approval boundary

### Needed before implementation

| Decision | Recommended default | Why it matters |
|---|---|---|
| Pilot audience, age, launch market | Tech audience confirmed; provisionally English, adults, invitation pilot; confirm jurisdiction before external launch. | Determines privacy review, content relevance, accessibility research, and support. |
| Pathways and reviewers | Reviewer-led selection confirmed; shortlist web development/data analysis only if reviewers are available. | Reviewer capacity and useful projects matter more than breadth. Existing tracks remain preserved until approved replacement/archive policy. |
| Product and stack scope | Review proposed MVP and ADRs 001–011; retain Django/Next.js with supported versions. Approval may cover P0 alone. | Prevents rebuilding a broad incomplete prototype or silently finalizing stack choices. |
| Existing data and deployments | Confirm whether any real learners or production environment exist. | Cannot safely plan destructive schema replacement from repository evidence alone. |
| Operating budget and AI deployment | Zero operating spend and prototype limits confirmed; approve local-only deployment and a local-model feasibility phase. | No paid API, hosting, hardware, or automatic fallback; a useful AI model must pass evaluation on available hardware. |
| Team capacity and review workflow | Small reviewable phases; owner reviews each phase; branch/PR workflow, no autonomous merges. | Controls delivery scope and estimates. |

### Needed before external pilot

Approve a genuinely sustainable zero-spend hosting arrangement or explicitly revise the budget; privacy notice, retention and subprocessors; adult eligibility policy; review turnaround/capacity; resource rights and regional availability; real email delivery; deployment authority and incident owner. A local prototype does not satisfy public availability or disaster recovery guarantees. No contract, purchase, deployment, or external publication is authorized by this document.

### Can remain provisional

Precise colors and logo, search ranking, additional pathways, AI model winner, and reminder cadence. Model selection follows evaluation, not brand preference. Deferred features remain unapproved.

Review can approve selected ADRs and a single phase rather than the entire backlog. **Planning completion is not implementation authorization.** The next action is the product owner's review and explicit approval of the relevant decisions and implementation phase.
