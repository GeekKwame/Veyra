# Repository discovery

Status: planning evidence, 2026-10-23. Scope: tracked source/configuration, Git state, dependency manifests, tests, and supplied brief. No application changes, migrations, dependency installations, service launches, or external writes were performed.

## Observed state

- Existing partial implementation, not an empty project. Branch `main` tracks `origin/main`; initial working tree was clean. Latest observed commit: `13623bd` (requirements update). Remote synchronization was not checked by fetching.
- Django modules: accounts, careers, roadmaps, assessments, projects, mentor; initial migrations exist for five data-owning modules. Django Admin registrations and career fixtures exist.
- Frontend: Next.js App Router, React, TypeScript, global styles/design tokens; home, careers/list/detail, discovery, register, login, dashboard pages. No project, assessment, evidence, settings, or learning-task pages found.
- Requirements constrain Django to `>=5.1,<5.2`; other backend dependencies largely have lower bounds only. Celery, Redis, HTTPX, Pydantic, pytest, and Flask-oriented `flasgger` are listed; no use of `flasgger` was found in inspected application code.
- `package-lock.json` resolves Next.js 15.5.27, React 19.3.0, TypeScript 5.9.3. The README describes broader major versions. Frontend has build/dev/start/lint scripts, no frontend tests or lint configuration found.
- Compose defines PostgreSQL 16 with pgvector and Redis 7, with local credentials and host-published ports. No app container builds, CI workflow, deployment manifest, background verification task, or runbook was found. Settings default to SQLite, debug enabled, and a development secret.
- No applicable `AGENTS.md` was found in the repository or inspected ancestor locations. No supplied raster/vector logo assets were found in the frontend. Existing CSS is not evidence of an accessibility audit.
- No project-local virtual environment or frontend `node_modules` exists. System Python cannot import Django, pytest, pytest-django, or dotenv. Database contents, hosting, deployed versions, provider accounts, and production users were not established.

## Findings and proposed handling

These are source-level findings unless explicitly described as executed checks. Severity is planning priority, not a completed penetration-test rating. Preserve the existing files; implement corrections only after approval.

| Priority | Evidence | Finding / consequence | Proposed treatment |
|---|---|---|---|
| P0 | `backend/apps/accounts/serializers.py`, `views.py` | `UserSerializer` exposes writable `role` through the current-user update view. It does not itself set `is_staff`, so this is not evidence of full Django-admin takeover; it does allow unauthorized role-label mutation. | Separate safe profile input DTO; enforce role changes only through privileged audited workflow. Test learner PATCH attempts. |
| P0 | `backend/apps/roadmaps/models.py` | Initialization counts `downstream_links` instead of a skill's `prerequisite_links`; unlocking traverses `prerequisite_links` from the completed skill instead of its downstream dependents. For A → B this can lock A and expose B. | Regression tests with real DB relationships; transactional service with correct required-edge semantics. |
| P0 | `frontend/src/lib/api.ts`, `backend/veyra_core/settings.py`, `frontend/src/app/careers/page.tsx` | List API uses DRF pagination; client expects `CareerListItem[]` and page invokes `.map()`. Likely runtime failure with the configured paginated response. Existing API test merely checks response length. | Explicit collection contract and a test spanning actual serializer response and UI consumption. |
| P0 | `backend/apps/mentor/services.py` | Always emits a canned response. Presence of any configured provider key changes `is_simulated` to false without any provider call. | Mark unavailable honestly; gate real integration behind evaluation. Never imply that key presence establishes a successful call. |
| P0 | `backend/apps/assessments/views.py` | Passing any current quiz calls `mark_mastered`; no practical evidence requirement, eligibility gate, or pinned question version. | Separate knowledge from practical demonstration; server-authorized evidence policy and immutable attempts. |
| P0 | `backend/apps/careers/serializers.py`, project/assessment views | Nested topic resources are unfiltered by publication status; project detail includes all projects; assessment detail ignores career publication/eligibility. | Public querysets and nested serializers must enforce published releases; private content requires ownership/eligibility checks. |
| P0 | `backend/requirements.txt` | Django 5.1 line is unsupported under the current upstream support table. | Propose supported Django 5.2 LTS with a tested upgrade and locked dependencies. See [Django support](https://www.djangoproject.com/download/). |
| P1 | `backend/apps/roadmaps/views.py`, models | Enrollment deactivates other roadmaps before later operations, without a transaction; can enroll an unpublished career; no DB guarantee of one active roadmap. | Atomic enrollment, published-release check, owner lock and partial unique constraint. |
| P1 | `backend/apps/careers/models.py` | Cycle validation lives in `clean()`, with no save override/service enforcing it; fixture creation bypasses this validation. README claim of validation “on database save” is not established by the code. | Validate and lock complete draft graph at publication; DB self-edge/uniqueness constraints; test competing updates. |
| P1 | `backend/apps/careers/models.py` | Skills belong to a single career through competency; prerequisites forbid cross-career relations. Resources attach to one topic, use default-true free flag, and mix publication and verification in one status. | Shared skills with path mappings; resource access classification and separate review/health records. |
| P1 | `backend/apps/careers/views.py` | Discovery uses profession/category string checks and arbitrary numeric match scores; reads interests/environment without using them; unsafe casts can reject malformed input as server errors. | MVP catalog selection; later content-driven explanatory discovery with validated inputs. |
| P1 | `backend/apps/accounts/views.py`, serializers, frontend API client | Login reveals whether an account exists; browser persists bearer tokens in localStorage; registration does not invoke configured Django password validators. Profile is read-only as nested data. | Secure same-origin sessions, generic auth errors, password validation, controlled profile contract, recovery and verification. |
| P1 | `backend/veyra_core/settings.py` | AllowAny default, BasicAuthentication enabled, no throttle policies, permissive development defaults. Individual private views do set IsAuthenticated. | Deny by default, explicit public routes, shared limits, production fail-fast settings, session/CSRF design. |
| P1 | Models across careers/projects/assessments/roadmaps | Mutable live curriculum and cascading deletes can invalidate or erase learning history; attempts/submissions lack content revision pins. | Preserve identities, immutable published versions, protected references, tested data migration. |
| P1 | `frontend/src/app/page.tsx`, `layout.tsx` | Static career claims, title-derived slugs differing from fixtures, and `/how-it-works` navigation with no matching page. | Source catalog links from real API slugs; build or remove unavailable destinations after approval; factual copy audit. |
| P1 | README, Compose, settings, API client | README backend port 8000 differs from frontend fallback 8001; README overstates verification/mentoring maturity and test coverage. | Single documented development configuration and truthful status; keep current README unchanged during planning. |
| P2 | Pacing and DAG engines | Pacing floors fractional days, treats zero time as one hour, uses server date; graph set iteration does not guarantee stable independent-step order. | Explicit pause semantics, rounded-up bounds, learner timezone, stable tie-break ordering. |
| P2 | Career serializers | Per-career counts/sums and nested graph/resource retrieval may cause repeated DB queries. | Query-count baselines and prefetch/aggregation before load tuning. |

Existing seed content covers developer, medical coding, bookkeeping/accounting, and electrical foundations. A separate script creates a small curriculum and one resource per track, directly marked published without verification history. It does not establish complete pathways or reviewed resources. Regulated and hazardous subject matter requires qualified, jurisdiction-aware review before publication; a safe cross-profession pilot can use other pathways. Existing seeds should not be silently deleted or represented as vetted content.

## Validation actually performed

- Python's standard-library parser successfully parsed **62 Python files**; this is syntax validation only.
- Ran dependency-free smoke assertions directly against the existing algorithm modules: linear A → B → C ordering, milestone tiers, detection of a three-node cycle, and 40 hours at 10 hours/week yielding 2026-10-29 from 2026-10-01. These checks passed.
- Found **12 pytest test functions** covering basic auth, careers/discovery, enrollment/recalibration, DAG, and pacing. Did **not** execute pytest: its dependencies are absent. No assessment, project, mentor, ownership-negative, browser, or resource-verification tests were found.
- Did **not** run frontend build, lint, typecheck, browser tests, PostgreSQL integration tests, dependency vulnerability scans, migrations, fixtures, or deployed checks. No claim is made that the application currently works end to end or is secure.

Next.js' official support page currently lists 15.x as maintenance and 16.x as active LTS, while its policy also describes a two-year maintenance period after initial release. Given the inspection date and that boundary, recheck the latest support/security guidance during P0; recommend validating an upgrade to active LTS rather than relying on the existing major. [Next.js support policy](https://nextjs.org/support-policy)

## Preserve and evolve

Retain the domain modules, UUID identities, basic Django Admin setup, API prefix, React styles/components that pass review, and useful algorithm tests. Do not reset Git, squash historical migrations, load fixtures into unknown databases, or rewrite working modules merely to match the proposal. First implementation phase must inventory any real data, establish reproducible checks, and turn the high-priority source findings into observable regression cases.
