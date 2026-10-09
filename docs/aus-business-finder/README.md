# Australian Business Finder

**Public beta:** source and installation are available. This is a sourced-candidates Finder, not independent business verification. Version 0.4.0 adds a decisive-claim check and bounded source recovery; see its [development evaluation](EVALUATION-0.4.0.md), including misses and limitations. The [0.3.0 evaluation](EVALUATION.md) remains available as the historical baseline.

A small agent skill that finds **Australian business candidates** by type and place and links to the businesses' own public pages. It tells you what each site says about its services, address or service area. It **does not independently verify** that a business trades, occupies an address, has stock or is available. It never contacts a business or builds a database.

## Try asking

> Find three businesses advertising commercial refrigeration repair around Adelaide. Show the business pages you opened, distinguish an office address from a claimed service area, and tell me what remains unconfirmed. Do not contact anyone.

You can ask about service providers, suppliers, shops, venues or a named business, and add exclusions. The Finder returns only candidates with relevant opened pages; it may return fewer than requested rather than pad a list from search snippets.

## Example from a local test

For an Adelaide refrigeration-repair request, the skill returned LJ Refrigeration & Air-Conditioning, BOSSY’S Refrigeration and Adgemis Refrigeration. Their opened pages [LJ](https://ljrefrig.com.au/commercial-fridge-repair-adelaide/), [BOSSY’S](https://www.bossys.au/commercial-refrigeration-service-repairs/) and [Adgemis](https://adgemisrefrigeration.com.au/services/commercial-refrigeration-adelaide/) advertised relevant repair work and an Adelaide service area on 8 October 2026. An independent review checked what those pages actually stated. This is **not** confirmation of current availability, service quality or every Adelaide provider.

## Install

Install it in Hermes:

```bash
hermes skills install JakeMarchin-Vincent/skills/aus-business-finder-mv
```

The original standalone 0.3.0 package installed in a clean, isolated Hermes home on 8 October 2026. The 0.4.0 candidate bundle in this consolidated repo was separately installed from a pinned commit into an isolated home on 9 October: its safety scan allowed it and the installed skill, claim-checking reference and MIT notice matched the commit byte-for-byte. MEWY also exercised the installed candidate in live, bounded lookups; see the [0.4.0 evaluation](EVALUATION-0.4.0.md) for results and limits. A live model run *inside that credential-free isolated home* has not been performed. Hermes needs web search and at least one working page opener (`web_extract` or `browser_navigate`); source access varies by session. The skill has no account, API-key or business-database dependency of its own.

For predictable use, **invoke the installed skill explicitly** in a new Hermes session: `/aus-business-finder-mv Find two ...` or `hermes -s aus-business-finder-mv chat -q 'Find two ...'`. Natural selection of this skill was inconsistent in development tests; a business-finding answer alone does not show that the skill loaded.

## Reading the results

- **Sourced candidate:** an opened business page says something relevant. Read the link yourself before relying on the detail.
- **Address vs service area:** “the site lists an address in X” and “the site advertises service to X” are different statements. Neither confirms current occupancy or operation.
- **Unconfirmed clue:** a directory/search result that could not be checked on the business's own page. It is separate from the sourced list.
- **No matching sourced candidate in the sources checked:** not evidence the business does not exist.

Search rankings are not recommendations, ratings, stock checks, price checks or availability checks. Public contact details are for lookup, not permission for outreach. The skill never sends enquiries or makes bookings.

## Evidence, authorship and limits

See [the 0.4.0 development evaluation](EVALUATION-0.4.0.md), [the earlier eight-case evaluation](EVALUATION.md) and [release evidence and limitations](EVIDENCE.md). The earlier 0.3.0 skill returned **4** clearly supported candidates versus **8** for the audited ordinary-agent baseline, missed page details and copied one contact incorrectly. The 0.4.0 development cases recovered some of those missed candidates but still missed others, and were not a matched comparison against an ordinary agent. **Neither result establishes a performance improvement over a general agent.** Earlier versions sometimes overstated a shop or physical location and once cited a broken contact-page URL; that is why this version reports website claims as **candidates**, not independently verified businesses. Its value is a short, inspectable starting point, not a certification service.

Dusk authored the Australian discovery workflow with Hermes Agent assistance. Hermes supplies the runtime and web tools; a hosted model makes the research decisions. ABN Lookup can help with a confidently matched legal identity but does not provide a complete sector/contact/service-area feed. Google Maps is not a bulk-data source. Public publishing and portfolio wording remain subject to founder review.
