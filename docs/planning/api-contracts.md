# H. Proposed API contracts

Status: design for review, **not implemented API documentation**. Existing routes differ; migrate the frontend and backend together after approval. Retain the `/api/v1` prefix and public career slugs. Proposed contracts describe workflows and public DTOs, not unrestricted model CRUD.

## Common contract

- JSON over HTTP on loopback locally, HTTPS before any remote deployment. UUID strings identify private objects; public careers also have stable slugs. RFC 3339 UTC timestamps; dates use `YYYY-MM-DD`. Estimates use explicit units and ranges. Nullable fields mean unknown, never fabricated zero.
- Session cookie is HttpOnly, SameSite=Lax and Secure outside loopback development. All unsafe requests, including unauthenticated login/registration, require CSRF validation. Explicitly protect these views rather than relying on session authentication to check anonymous requests. No credentials or tokens in URLs or localStorage.
- Authenticated user comes from the server session. No endpoint accepts `user_id`, owner, role, calculated score, proficiency, verification result, or reviewer identity as learner-controlled input. Reject unknown writable fields.
- Public reads return only published content DTOs; draft metadata and answer keys are never nested into public results. Private responses set `Cache-Control: private, no-store`. Public catalog ETags are scoped to published revisions, with invalidation on withdrawal.
- Collections use `{items: [...], next_cursor: string|null}` with `limit` default 20, maximum 50; opaque stable cursor over `(created_at,id)` or documented catalog sort. Invalid cursors/filters return 400. No unbounded nested curriculum/history collections.
- Mutations with duplicate side effects require `Idempotency-Key` (UUID). Scope keys by actor and operation; store a keyed request digest and safe result atomically, never raw credential-bearing bodies. Anonymous registration keys are separately scoped and must not disclose another request's account result. Same key/body replays the result, different body returns 409. Retain records at least 24 hours; permanent single-finalization constraints still protect attempts/submissions after key expiry. An interrupted AI job returns its existing request ID instead of submitting another generation.
- Mutable documents return integer `version` plus strong ETag. Updates require `If-Match`; missing gives 428, stale gives 412 with current version. No optimistic update may overwrite earned evidence. Concurrent acceptance/finalization also uses transactional locking and uniqueness constraints.
- Consistent statuses: 400 malformed/invalid request, 401 no valid session, 403 denied action/CSRF, 404 absent or another user's private object, 409 invalid workflow state, 412 stale version, 413 oversized payload, 422 well-formed but infeasible roadmap constraints, 428 missing concurrency precondition, 429 rate/quota limit with Retry-After, 503 unavailable dependency. Configure auth error handling explicitly to honor this contract.
- Initial abuse limits: anonymous catalog 60/min/IP, account login 5 failed attempts/15 min per account plus 30/15 min/IP, registration/recovery 5/hour/IP, learner writes 30/min/user, checks 10 finalized attempts/hour/user, resource reports 10/day/user, AI one pending request/user and ten/day. These are adjustable prototype policies, not upstream provider limits. Avoid permanent account lockout; handle shared-network users fairly. Use shared DB counters atomically in local multi-process mode; no process-local counter as a security boundary.

Error example:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Check the highlighted fields.",
    "fields": {"hours_per_week": ["Enter a value from 0 to 40."]},
    "request_id": "req_example"
  }
}
```

The proposed 40-hour ceiling keeps estimates within the pilot's intended use; zero pauses a schedule. Validate integers and timezone names; do not coerce malformed values silently. Error messages never include secrets, SQL, stack traces or account-existence details.

## Authentication and profile

| Method and route | Access / request | Response / effects and special behavior |
|---|---|---|
| `GET /auth/csrf` | Anonymous; no body. | 200 CSRF token bootstrap; no learner identity. Rate-limited. |
| `POST /auth/register` | Anonymous + CSRF; `{email, display_name, password}`. Normalize email, validate password through framework validators, cap field sizes. | Local mode: 201 `{user, account_mode:"local_test", email_verified:false}` with session. External mode must use generic verification flow to avoid enumeration and cannot claim sent mail without delivery configuration. Role is server assigned. Idempotency required. |
| `POST /auth/login` | Anonymous + CSRF; `{email,password}`. | 200 `{user}` and rotated session; generic 401 for all invalid credentials. No token in body. Rate controls above. |
| `POST /auth/logout` | Session + CSRF; empty body. | 204; invalidate session server-side. Safe repeat yields logged-out state. |
| `GET /auth/me` | Session. | 200 safe user/profile DTO; 401 if expired. Never turn an unrelated 503 into “signed out.” |
| `PATCH /profile` | Owner; `{display_name?, timezone?, hours_per_week?, preferences?}` with If-Match. | 200 safe profile/version; does not silently rewrite roadmap schedule. Return `schedule_change_available` when appropriate. No writable role or verification flag. |
| `POST /auth/password-reset-requests` | External-launch contract: anonymous + CSRF, `{email}`. | Generic 202 for any address. Single-use expiring token through approved email sender. In local mode, clearly identify console/test delivery and never expose another user's token in an API response. |
| `POST /auth/password-resets` | Single-use token + CSRF; `{token,new_password}`. | 204; validate password, consume token, revoke existing sessions. 400 generic invalid/expired token. |

Email change and verified-email activation contracts are completed with the real email delivery design before external launch. For a purely local supervised prototype, use test accounts without pretending to verify email ownership. Staff permissions are managed through audited admin actions, not the profile endpoint.

## Catalog, resources and discovery boundary

| Method and route | Access / schema | Response / validation / effects |
|---|---|---|
| `GET /careers?category=&limit=&cursor=` | Public; documented filters only. | 200 collection of `{id,slug,title,summary,category,scope,current_release_id,estimated_hours:{min,max}}`. No private draft or market-demand claim. |
| `GET /careers/{slug}` | Public, published current release. | 200 path scope, typical tasks, prerequisites, reviewer/publication metadata and milestone summary; 404 if not published. Large activities fetched separately. |
| `GET /careers/{slug}/activities?limit=&cursor=` | Public, published content. | 200 objective/task summaries and resource IDs. Answer keys and reviewer-private notes omitted. |
| `GET /resources?skill_id=&access=&language=&limit=&cursor=` | Public, published resource revisions. | 200 collection of resource cards. Enum filters validated; access and health shown separately. |
| `GET /resources/{id}` | Public if published. | 200 `{id,revision,title,url,provider,type,language,access,health,attribution}`; `access` includes classification, required login, certificate cost and known regions; health includes check type/date/status. |
| `POST /resources/{id}/reports` | Session; `{reason:"broken|paywall|accessibility|quality|other",note?}`; note max 1,000 characters. | 201 `{id,status:"open"}`; triage queue entry, no automatic content withdrawal. Idempotency/deduplication and report rate limit. |

No public discovery-scoring endpoint in MVP. Existing `/careers/discovery/evaluate/` should be retired with the affected UI after approval; do not keep arbitrary percentages as a hidden compatibility feature. V1 proposal: `POST /discovery/suggestions` over reviewed career attributes, separate from roadmap creation, returning explanations/limitations without success probabilities.

Resource example:

```json
{
  "id": "00000000-0000-4000-8000-000000000010",
  "revision": 2,
  "title": "Example official documentation",
  "url": "https://example.org/tutorial",
  "provider": "Example provider",
  "access": {
    "classification": "free",
    "login_required": false,
    "certificate_cost": "not_applicable",
    "region_notes": null,
    "reviewed_at": "2026-10-20T10:00:00Z"
  },
  "health": {
    "status": "reachable",
    "method": "http_check",
    "checked_at": "2026-10-23T09:00:00Z"
  }
}
```

All IDs and example.org URLs here are illustrative contract fixtures, not claimed real learning resources.

## Roadmap workflows

| Method and route | Request / permissions | Response / invariants |
|---|---|---|
| `POST /roadmaps/proposals` | Owner; `{career_id,hours_per_week,target_date?,timezone}`; Idempotency-Key. Only published, complete release. | 201 proposed roadmap DTO, pinned release, credit decisions and reasons, effort range, prerequisite groups. Persist as `UserRoadmap.status=proposed`, expiring after 24h; no active plan deactivated yet. Infeasible target date: 422 with constraints/options. |
| `GET /roadmaps/{id}` | Owner; another user's ID returns 404. | 200 `{id,status,release_id,version,schedule,summary,next_step}`. Steps/history paginated separately. Expired proposals return their expired status; cannot accept. |
| `POST /roadmaps/{id}/accept` | Owner of unexpired proposal; empty body, Idempotency-Key and If-Match. | 200 accepted plan. Atomically archive/deactivate former active roadmap and activate this one, retaining all history. Revalidate publication/eligibility; withdrawn release or changed proposal returns 409/412. |
| `GET /roadmaps/active` | Owner. | 200 active plan DTO, or 404 `no_active_roadmap`; UI offers explicit next action. |
| `GET /roadmaps/{id}/steps?limit=&cursor=` | Owner. | 200 ordered collection with objective, activity, availability, reason, estimated effort and content revision. |
| `POST /roadmaps/{id}/schedule-preview` | Owner; `{hours_per_week,target_date?}`. | 200 proposed date/effort diff and existing version, or 422 infeasible target. No learning-state mutation; only privacy-safe usage logs. |
| `PATCH /roadmaps/{id}/schedule` | Owner; same schedule body, If-Match. | 200 updated schedule/version; preserve completed steps, attempts, reviews and source releases. Zero hours pauses; no automatic curriculum migration. |
| `POST /roadmaps/{id}/steps/{step_id}/activity-records` | Owner; `{action:"start|complete|undo_completion",reflection?}`, Idempotency-Key. | 201 record and updated activity summary. Only learner-completable activity types; 409 on unmet gate or attempt to manually award assessment/project evidence. Reversal recorded rather than deleting history. |

Proposal example, showing meaningful reasons instead of an AI-generated unvalidated plan:

```json
{
  "id": "00000000-0000-4000-8000-000000000020",
  "status": "proposed",
  "release_id": "00000000-0000-4000-8000-000000000021",
  "version": 1,
  "schedule": {"hours_per_week": 5, "remaining_hours": {"min": 20, "max": 30}},
  "credit_decisions": [{"objective_key": "tables.read", "credit": "knowledge_check", "reason": "Passed the current equivalent knowledge check; project evidence is still required."}],
  "next_step": {"activity_key": "tables.practice", "reason": "Apply the knowledge demonstrated in your challenge."},
  "warnings": ["Estimates exclude waiting for project review."]
}
```

## Assessments, projects and evidence

| Method and route | Request / permissions | Response / effects |
|---|---|---|
| `POST /assessments/{id}/attempts` | Owner; `{roadmap_id,purpose:"practice|challenge"}`, Idempotency-Key. Check release, objective membership, allowed challenge policy and attempt limits. | 201 `{id,assessment_version,status:"in_progress",questions,version}`; learner-safe question DTOs only. Server pins question set. Prior-knowledge challenge eligibility is explicit, not a generic bypass. |
| `POST /assessment-attempts/{id}/submit` | Owner of open attempt; `{answers:[{question_id,selected_option_ids}]}`, Idempotency-Key and If-Match. | 200 finalized result, objective-level knowledge evidence and permitted explanations. Validate unique question IDs, belonging, option membership and required answers. No client score. Atomic grade/evidence/unlock; no automatic practical mastery. |
| `GET /assessment-attempts/{id}` | Owner. | 200 immutable finalized result or in-progress safe DTO. Protected answers only disclosed according to formative feedback policy after finalization. |
| `GET /projects/{id}` | Public only for a published project version. | 200 brief, objectives, deliverables, permitted submission types and rubric. No other learner submissions or private reviewer notes. |
| `POST /projects/{id}/submissions` | Owner; `{roadmap_id,text?,artifact_url?,reflection?,self_review?}`, Idempotency-Key. Require at least one accepted artifact type; cap text at 20,000 chars and URLs at 2,048. | 201 draft submission with version. HTTPS URL validation only; backend does not fetch. No forced public sharing; user sees external privacy reminder. |
| `PATCH /submissions/{id}` | Owner of draft; safe artifact fields and If-Match. | 200 draft/version; edits prohibited after final submission. |
| `POST /submissions/{id}/submit` | Owner of valid draft; empty body, Idempotency-Key and If-Match. | 200 `{status:"submitted",review_state:"pending"}`; preserve artifact version, enqueue human review, no promised automatic grade. |
| `POST /submissions/{id}/revisions` | Owner; new draft artifact fields, Idempotency-Key. | 201 new revision linked to preceding submission; never overwrite reviewed evidence. |
| `GET /submissions?limit=&cursor=` and `GET /submissions/{id}` | Owner; assigned reviewer uses admin route. | Paginated owner-only history / detail with finalized feedback. Another learner receives 404. |
| `GET /evidence?skill_id=&limit=&cursor=` | Owner. | Collection with skill/objective, source, provenance, policy/version, achieved level, date, revocation/supersession if any. No employability guarantee. |

MVP assessments are formative. Full feedback after an attempt helps learning but allows memorization; subsequent attempts remain labeled and cannot independently prove practical competence. Formal secure testing would be a separate product. Unrecognized/duplicate answers produce field errors rather than silently ignoring tampering.

## AI learning assistant

| Method and route | Request / permissions | Response / behavior |
|---|---|---|
| `POST /mentor/requests` | Owner; `{roadmap_id,step_id,message,conversation_id?}`; Idempotency-Key. Confirm all context belongs to owner and the pinned roadmap. | 202 `{request_id,status:"queued",status_url}`; at most one pending/user and one running globally. Reject unknown cross-owner conversation with 404. 429 busy/quota, 503 unavailable runtime, no simulated response. |
| `GET /mentor/requests/{id}` | Owner only. | 200 queued/running/completed/failed/cancelled state; completed includes `{answer,source_ids,next_activity_id?,uncertainty?,model_version}`. Failure includes safe reason/retry guidance, never success-shaped fabricated content. Poll with bounded backoff. |
| `POST /mentor/requests/{id}/cancel` | Owner; empty body. | 200 cancellation state. Worker observes cancel flag, stops/releases lease; late results are discarded. Safe repeat. |
| `GET /mentor/conversations/{id}/messages?limit=&cursor=` | Owner. | Paginated retained messages; no complete conversation in generic logs. |
| `DELETE /mentor/conversations/{id}` | Owner + CSRF. | 202 deletion status; cancels queued requests, removes live transcript by documented deadline. |

No provider keys are accepted from the browser. The local adapter uses only configured local endpoints. The server maps allowed source IDs to known URLs before display. The AI cannot create new authoritative resource records or advance progress.

## Data rights and administration

| Method and route | Request / permissions | Response / side effects |
|---|---|---|
| `POST /account/exports` | Owner with recent reauthentication; empty body, Idempotency-Key; one/day. | 202 `{request_id,status}`; background job produces owner-only JSON export, download expires in 24h. Includes profile, learning records, submissions, feedback and retained AI messages; excludes credentials, staff-private logs and answer banks. |
| `GET /account/exports/{id}` / `GET /account/exports/{id}/download` | Owner and recent session. | 200 state / attachment when ready, private no-store; 409 if pending, 410 if expired. No public download token in URL. |
| `POST /account/deletion-requests` | Owner with recent reauthentication; `{confirm:true}`, Idempotency-Key. | 202 receipt, revoke sessions, immediately disable account; worker removes live data under retention policy. Idempotent tombstone protects against duplicate jobs. Explain backup expiry before confirmation. |
| `POST /admin/curriculum-releases/{id}/validate` | Curator; If-Match. | 200 completeness, prerequisite, rights/free-route errors. No publication. |
| `POST /admin/curriculum-releases/{id}/publish` | Publisher permission; `{review_note}`, If-Match and Idempotency-Key. | 200 immutable release/current pointer; enforce successful fresh validation and recorded review; audit within transaction. |
| `POST /admin/resources/{id}/verification-requests` | Curator; `{reason}`; bounded per-resource rate. | 202 queued job. Server uses reviewed resource URL, never a URL from request body. |
| `POST /admin/submissions/{id}/reviews` | Assigned reviewer; `{criterion_results:[{criterion_id,level,feedback}],decision,summary}` and Idempotency-Key. | 201 finalized review plus policy-derived evidence; validate pinned rubric; preserve attribution and prior decisions. Review correction creates a superseding review. |

These administration contracts may initially be Django Admin forms invoking the same services, rather than a separately implemented admin JSON API. Do not build both without need. Role checks, audit, validation and transactions are identical regardless of interface.

## Compatibility and completion before coding each workflow

During implementation, derive OpenAPI from reviewed DTOs, generate/check TS types, and add contract tests for actual server responses. Replace the present paginated-list mismatch first. Inventory real clients before removing existing routes. If external clients exist, use explicit deprecation and migration; otherwise update the local frontend atomically with the backend. Make breaking changes v2 only when v1 has real consumers; avoid maintaining duplicate APIs for a prototype without evidence of those consumers.

Complete exact schema enum names, maximum sizes, example responses and error cases for each implemented phase before writing handlers. This document is representative contract design, not a claim that all endpoints should be generated at once.
