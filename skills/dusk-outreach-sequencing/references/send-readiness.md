# Send readiness and sequence state

This is a checklist for the operator and any integration—not a universal statement of marketing law. Requirements vary by jurisdiction, channel and relationship. If the user cannot establish them, stop at an illustrative draft and advise checking applicable rules with a qualified professional.

## Before labelling a draft ready for human review

- Sender and business identity are accurate; contact channel and reply path work.
- The intended recipients and basis for contacting them are permitted under the user's applicable requirements; no scraped address is presumed contactable just because it is public.
- All claims, offers, testimonials and deadlines are genuine and authorised. A likely industry pain is phrased as a possibility, not alleged as a fact about this company.
- Required identification and an effective way to opt out are present where applicable. An unsubscribe request or clear refusal is reflected in the source of truth before any further eligibility check.
- The user's prior-contact, CRM and suppression records were checked. If inaccessible, disclose that verification is outstanding.
- No hidden automatic follow-up: approved cadence, local sending window, sender domain, volume and owner are explicit before scheduling.

`READY FOR HUMAN REVIEW` means the draft is reviewable and prerequisites appear documented. It does not mean legal approval, delivery approval or a guarantee of inbox delivery. `REVIEW REQUIRED — DO NOT SEND` is the default when a material prerequisite is missing. `SKIP` is used for known refusals, opt-outs, irrelevant prospects and already-contacted recipients where the user did not request a reply.

## State model for an implementation

Track events per **campaign + recipient + touch**, not just a free-text lead stage:

| State/event | Consequence |
|---|---|
| `draft` | Editable; no sending authority. |
| `approved` | Exact content and recipient approved under a named campaign. |
| `eligible` | Prior touch has a confirmed send timestamp; elapsed gap and local send window pass; no reply, refusal, bounce or suppression. |
| `claimed` | One worker holds a durable, unique claim. Recheck eligibility at claim and immediately before provider call. |
| `accepted_by_provider` | Save provider identifier and timestamp atomically where feasible; do not claim delivered to inbox. |
| `failed_before_acceptance` | Retry only if provider definitively did not accept, with bounded backoff and human-visible error. |
| `outcome_unknown` | Timeout/crash with uncertain acceptance: quarantine and reconcile with provider; never blind-retry. |
| `replied`, `refused`, `opted_out`, `bounced` | Suppress remaining touches immediately. |

Use a database uniqueness constraint for `(campaign_id, recipient_id, touch)` and an idempotency key if the provider supports it. A successful API call followed by a database failure is still an ambiguous-send problem. Keep an audit trail of the approved content version, eligibility decision, provider response and suppression events. Build and test this separately for the user's actual stack; this skill ships no sender code.
