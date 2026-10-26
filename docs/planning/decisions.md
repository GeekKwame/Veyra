# Q. Proposed Architecture Decision Records

Status of every ADR below: **Proposed — not accepted**. The owner's tech focus, reviewer-led selection, requested AI feature, and zero-operating-spend/prototype constraint are confirmed requirements. The specific engineering choices below still need review. Record approver, date and scope when accepted; do not infer acceptance from a request to continue planning.

The [technology matrix](architecture.md) includes cost, operational complexity, lock-in and confidence for each major technology. These records state the decision context and consequences. No ADR authorizes implementation or expenditure by itself.

## ADR-001 — Preserve a modular monolith

**Context:** Existing Django modules and Next.js frontend implement part of the intended domain; correctness and privacy gaps are more urgent than service decomposition.

**Recommendation:** Retain Django/DRF as the single domain/API authority, PostgreSQL as the relational store, and Next.js/TypeScript for presentation. Upgrade to supported, tested, locked versions after approval. Keep business services inside coherent modules; no microservices or second backend in Next.js.

**Alternatives:** FastAPI plus assembled auth/admin, a TypeScript backend rewrite, server-rendered Django UI, or microservices. These may fit other teams but introduce replacement work or operations with no established benefit here.

**Consequences:** Reuses investment and supports transactions/admin. Two language runtimes remain; local memory must be measured. Costs are local hardware use, not service fees. Conventional API/SQL exports reduce hosting lock-in; ORM/frontend framework coupling remains. Confidence high; approval required before dependency or architecture changes.

## ADR-002 — Tech-first, reviewer-led content on a generic model

**Context:** Original vision spans professions; owner clarified tech learners first and expert availability determines pathways.

**Recommendation:** Launch up to two reviewer-backed tech foundation pathways, starting with one if necessary. Reuse skills/objectives/resources/projects through mappings. Validate extensibility with an internal non-tech fixture, not additional public launch scope. Catalog selection first; broad career matching later.

**Alternatives:** Publish all four existing seeds, hard-code tech logic, or attempt a large career catalog. Existing seeds lack demonstrated review/completeness and include jurisdiction-sensitive subjects.

**Consequences:** Content quality and review capacity bound launch. Small catalog and no predictive fit scores. Shared skills require migration from career-owned skills but avoid future duplication. Volunteer review is not assumed available. Confidence high on scope, medium on pathway selection pending named reviewers; approval required.

## ADR-003 — Published releases and evidence provenance

**Context:** Mutable content and cascades can invalidate learner history. Current quiz results are treated as mastery.

**Recommendation:** Immutable typed curriculum/assessment/project/resource revisions; learner records pin versions; consumption, knowledge and practical evidence remain distinct. Transactions and protected references preserve history. Shared stable skill identities allow controlled transfer of credit.

**Alternatives:** Live references only, full-database event sourcing, generic untyped content blobs, or one aggregate readiness score. Live references lose historical meaning; full event sourcing and generic blobs add complexity beyond need.

**Consequences:** More revision/mapping records and explicit migrations, but reproducible feedback and trustworthy updates. Derived summaries can be rebuilt. Legacy mastery is labeled as legacy evidence without inventing practical review. Confidence high; approval required before schema/migration implementation.

## ADR-004 — Deterministic roadmaps and conservative credit

**Context:** Ordering, scheduling and completion must remain correct under AI failure and concurrent edits.

**Recommendation:** Validate required DAG, use stable ordering, explicit evidence gates, reviewed duration ranges and pause semantics. Learners review proposals and schedule diffs. Challenge checks waive only appropriate learning requirements; practical credit requires corresponding evidence.

**Alternatives:** Fully LLM-generated roadmaps, one rigid sequence, or an advanced adaptive constraint solver. The first is difficult to validate; the last is unnecessary for initial pathways.

**Consequences:** Explainable and cheap planning, less generative novelty. Alternative routes must be authored initially. No silent wholesale replacement of plans. Confidence high; approval required for behavior/contract changes.

## ADR-005 — Same-origin sessions and explicit permissions

**Context:** The current browser keeps tokens in localStorage; role is writable through current-user serialization.

**Recommendation:** Django server sessions, HttpOnly cookies, explicit CSRF validation including login, one browser origin, safe profile DTOs and permission groups. Private data is scoped on every query and nested relationship.

**Alternatives:** Keep persistent browser bearer tokens, use JWT refresh workflows, or outsource identity. These add token handling or service dependencies not justified for a local browser prototype.

**Consequences:** Simpler revocation and browser security; proxy/cookie configuration must be tested. Mobile/third-party auth is deferred. No external identity fee; session DB maintenance required. Confidence high; approval required.

## ADR-006 — Human-reviewed free resources and cautious automation

**Context:** A default-true boolean and successful HTTP status do not establish legal/free/usable learning access.

**Recommendation:** Separate publication, access classification and health. Link to original YouTube/documentation sources, retain permitted metadata, use reviewed provider destinations and safe scheduled checks. Human reviewers certify suitability/free-route coverage; reports and observations trigger triage.

**Alternatives:** Unrestricted crawling, automatic AI approval, or manual-only verification. Crawling adds risk and expense; manual-only checking can miss changes.

**Consequences:** Ongoing curation work, honest uncertainty and dated observations. No video/transcript redistribution by default. Limited background network activity and no paid scraping. Confidence high; approval required for workflow and network-job implementation.

## ADR-007 — Bounded jobs without Redis/Celery deployment

**Context:** Celery/Redis are configured but the inspected repository has no implemented verifier jobs. Zero-spend local deployment has limited resources.

**Recommendation:** Scheduled commands for maintenance/verification and one bounded DB-backed AI request worker with leases. Share application service functions and idempotency. Keep dispatch replaceable and avoid building a general queue framework.

**Alternatives:** Celery+Redis, inline long-running HTTP requests, or a cloud job service. Celery becomes reasonable if workload complexity grows; inline inference harms responsiveness and cancellation; cloud services add terms/cost risk.

**Consequences:** Fewer processes and no broker, but lease/cancellation/recovery behavior must be tested. Revisit before multi-worker scaling or complicated job chains. Confidence medium-high for prototype; approval required before removing existing dependencies/configuration.

## ADR-008 — Local AI first under a hard zero-spend constraint

**Context:** Owner requires an AI feature and no operating bills. Available hardware has limited free RAM; no local model has been tested.

**Recommendation:** Evaluate a licensed small quantized instruction model with local-only Ollama on existing hardware in P0. Select/pin only after quality, safety, memory and latency checks. Model scope is contextual explanation/hints; no tools, browsing, grading authority or cloud fallback. One generation at a time, explicit queues/quotas/timeouts.

**Alternatives:** Paid hosted APIs (incompatible with current budget), free hosted tiers (privacy/availability/quota conditions need explicit review), or no AI (contradicts clarified scope unless owner changes it). llama.cpp is a local-runtime alternative if justified by measured resource savings.

**Consequences:** No API subscription, but installation/download, model licensing, local computation and device uptime remain requirements. Quality/performance confidence low until measured. If feasibility fails, report it and revisit scope; never substitute canned replies or quietly spend money. Approval required before installing/downloading/running models. Exact model decision remains open.

## ADR-009 — Local prototype before external hosting

**Context:** Zero operating spend and prototype limits are accepted; no hosting/region/email/backup service is approved.

**Recommendation:** Loopback-only supervised prototype with test accounts, local DB and model, explicit console email, encrypted backups on existing storage. No paid providers, card-backed trials, hardware purchases or public tunnels by default. Keep remote/public launch as a separate gate with privacy, TLS, email, availability and durable storage decisions.

**Alternatives:** Assemble free cloud tiers, paid managed PaaS, self-managed VPS, or static frontend alone. Free tiers cannot be assumed permanent; paid infrastructure violates the budget; a static frontend cannot supply the full backend/AI experience.

**Consequences:** Not an always-available website for remote learners. Requires the owner's computer during sessions, with limited concurrency and recovery. Portable processes/SQL ease a later move. Confidence high for a prototype, not established for public operation. Approval required for this delivery mode and any subsequent publication.

## ADR-010 — Generic project evidence without uploads or execution

**Context:** Projects should demonstrate skills across careers while protecting private work and avoiding unnecessary storage/security infrastructure.

**Recommendation:** Versioned text/external-link submissions, explicit rubric criteria, assigned human review and evidence provenance. No automatic fetching, executing, or publicly sharing submissions. Show external-provider privacy limits. Defer object storage and automated project grading.

**Alternatives:** Require code repositories, universal AI grading, or immediate file uploads. These exclude non-code work or create unvalidated assessment/security burdens.

**Consequences:** Reviewer capacity and external link durability limit the prototype. No storage fee or execution sandbox needed. Later artifacts can adopt private object storage without changing the evidence contract. Confidence high; approval required.

## ADR-011 — REST contracts and modest frontend state

**Context:** The existing client/server pagination mismatch illustrates the risk of unreviewed interfaces; the UI is incomplete.

**Recommendation:** REST `/api/v1` workflow DTOs, consistent errors/pagination/idempotency/concurrency, contract tests and checked generated TS types. Local form state and server persistence; shared UI primitives only as repetition warrants them. Django Admin consumes backend publication/review services.

**Alternatives:** GraphQL, broad client global-state frameworks, duplicate admin JSON/UI implementations. None addresses a demonstrated prototype need.

**Consequences:** Some contract/type-generation tooling and disciplined review; limited framework-specific coupling. No extra service bill. Confidence high; approval required before API migration.

## Approval record template

Record accepted/rejected/deferred ADR IDs, approved phase(s), approver/date, exceptions and rationale, and any constraints on dependencies/downloads, real data or external access. Approval to implement P0 can remain limited to reproducibility and local-model evaluation; it does not authorize P1–P6 or external launch. A request to continue writing the plan is not that approval.
