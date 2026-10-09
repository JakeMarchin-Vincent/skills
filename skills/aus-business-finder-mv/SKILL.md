---
name: aus-business-finder-mv
description: Find Australian businesses with source links.
version: 0.4.0
author: Dusk, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Australia, business-discovery, research]
    requires_toolsets: [web]
---

# AUS Business Finder-MV

Find Australian business **candidates** by type and location, then show the public pages behind them. This first public version is a sourced discovery aid, **not an independent verification service or a complete directory**. Never label a business, physical premises, offering, contact or service area `verified`; an agent reading a website cannot independently establish those facts.

## When to Use

Use for Australian service-provider, supplier, shop, venue, partner and named-business lookups. This is ordinary research, not prospect qualification or outreach. If the user explicitly wants sales qualification, use the separate lead workflow after discovery; do not pitch or send anything as part of this skill.

## Prerequisites

Use `web_search` and an available page opener (`web_extract` or `browser_navigate`). If both openers fail, search snippets alone cannot support a sourced candidate; explain the limitation. No directory account or ABN API key is required. Source access varies by site and session.

## Quick start

“Find three commercial refrigeration repair businesses advertising service to Adelaide. Show the exact business pages you opened, distinguish an address from a service-area claim, and tell me what remains unconfirmed. Do not contact anyone.”

## Inputs and scope

- Use the requested business type, Australian place, purpose, count and exclusions. Accept a suburb, region, state or Australia-wide request. Ask for type or location only when genuinely missing; default to a short list.
- For a named business, report the best matching public pages rather than substituting a similar name. Do not infer quality, price, stock, availability or customer satisfaction.

## Find and check sources

1. **Discover broadly, then check precisely:** Search business type + place and relevant synonyms with `web_search`; do not require every requested attribute (such as a street address) in the initial search query, since that can hide real candidates. Open plausible businesses' own pages to test those attributes. An accessible directory or industry association may supply clues, never proof. If searches are empty or challenged, try one different safe discovery route or broader query before concluding sources are insufficient; stop after at most two alternative routes. Search rank and directory snippets do not establish business facts.
2. **Open and read:** Open the business's own relevant service/product, location and contact pages. Read the full relevant page, including service categories, footer and contact links, before declaring a decisive detail absent. Cite only URLs actually opened and checked; never invent a contact-page URL or cite a 404 as support. If a page is blocked, do not bypass it; report the gap where it limits the answer. If relying on a parent company's service page for a local brand, also open and link a page connecting the two.
3. **Check the decisive claim:** For every candidate, check that opened page(s) connect the **same business** to the requested **offering** and **place**; one fact alone never fills in the others. Follow [the decisive-claim check](references/claim-checking.md), including its bounded recovery when a fact appears absent or a page is blocked. If still unresolved, leave the business an unconfirmed clue rather than reject it as nonexistent or count it as sourced.
4. **Describe, don't certify:** Say “the website lists an address at …” or “the website advertises service to …”, not “physically based/operating there” unless the claim is explicitly qualified as the website's statement. A branch office, catalogue or stock statement is not proof of a walk-in retail shop. Separate a published shop/store claim from independently confirmed operation; the latter is not provided by this skill.
5. **Filter:** Apply exclusions and requested category, remove clear duplicates by website/name/address, and leave similarly named but distinct businesses separate. Stop at the requested number of usable sourced candidates; do not pad the list with unsupported search results. For exact-name no-match, say no matching sourced candidate was found **in the sources checked**, not that the business does not exist.
6. **Respect access:** Maps can be an optional small-lookup discovery clue when accessible and permitted, but never bulk-extract Maps results, copy Maps-only contacts/ratings into a database or bypass consent/challenge walls. ABN Lookup may help resolve a confidently matched legal identity, but is not a source of website, contact or service area. Do not seek private individuals or guess personal details.

## Result

For each **sourced candidate**, give **business name | what its opened page says about the requested offering | published address copied from an opened page or advertised service area (label which) | exact opened source URL(s) connecting those claims | public business contact copied exactly if shown | checked date | what remains unconfirmed**. Cite the specific opened page for each material detail; if an address, workshop or branch fact came from another page, cite that page too or omit the detail. If a page snapshot is abbreviated, check the full opened page before repeating an address; otherwise omit it. Prefer short lists. State how many candidates have opened first-party pages, not how many businesses have been independently verified. If a page or alternative candidate was blocked and that limits the count, say so. Label a directory-only clue as unconfirmed and separate it from the sourced list. Never output a `verified` status or an independently confirmed physical-shop claim.

## Pitfalls

- A public page can be stale or mistaken. Its text is evidence of a published claim, not proof of current trading, occupancy, licensing, suitability, stock or availability.
- A blocked directory, failed extraction or empty search is not proof a business is absent. Continue with permitted sources when feasible and preserve the gap.
- Public business contact details are for lookup, not permission for marketing. Never send enquiries, make bookings or contact businesses as part of finding them.

[MIT license and copyright notice](references/LICENSE.md).

## Check before replying

Confirm each cited URL was actually opened, supports the **same business × offering × place** claim and is not a missing page. Before treating a decisive fact as absent, inspect the whole relevant page and make the one bounded safe recovery attempt described in the reference. Check exclusions, duplicates, actual number of sourced candidates and the difference between address and service-area claims. Verify any public contact character-for-character against the opened source, or omit it. Report unknowns plainly; no external actions.
