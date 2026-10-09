---
name: aus-business-finder-mv
description: Find Australian businesses with source links.
version: 0.3.0
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

1. **Discover:** Search type + location and relevant synonyms with `web_search`; an accessible directory or industry association may supply clues. Search rank and directory snippets do not establish business facts. If searches repeatedly fail or challenge access, try at most two other permitted routes, then stop and say what could not be checked.
2. **Open:** Open the business's own relevant service/product, location and contact pages. Cite only URLs actually opened and checked; never invent a contact-page URL or cite a 404 as support. If a page is blocked, do not bypass it; report the gap where it limits the answer. If relying on a parent company's service page for a local brand, also open and link a page connecting the two.
3. **Describe, don't certify:** Say “the website lists an address at …” or “the website advertises service to …”, not “physically based/operating there” unless the claim is explicitly qualified as the website's statement. A branch office, catalogue or stock statement is not proof of a walk-in retail shop. Separate a published shop/store claim from independently confirmed operation; the latter is not provided by this skill.
4. **Filter:** Apply exclusions and requested category, remove clear duplicates by website/name/address, and leave similarly named but distinct businesses separate. Stop at the requested number of usable sourced candidates; do not pad the list with unsupported search results. For exact-name no-match, say no matching sourced candidate was found **in the sources checked**, not that the business does not exist.
5. **Respect access:** Maps can be an optional small-lookup discovery clue when accessible and permitted, but never bulk-extract Maps results, copy Maps-only contacts/ratings into a database or bypass consent/challenge walls. ABN Lookup may help resolve a confidently matched legal identity, but is not a source of website, contact or service area. Do not seek private individuals or guess personal details.

## Result

For each **sourced candidate**, give **business name | what its opened page says about the requested offering | published address or advertised service area (label which) | exact opened source URL(s) | public business contact if shown | checked date | what remains unconfirmed**. Prefer short lists. State how many candidates have opened first-party pages, not how many businesses have been independently verified. If a page or alternative candidate was blocked and that limits the count, say so. Label a directory-only clue as unconfirmed and separate it from the sourced list. Never output a `verified` status or an independently confirmed physical-shop claim.

## Pitfalls

- A public page can be stale or mistaken. Its text is evidence of a published claim, not proof of current trading, occupancy, licensing, suitability, stock or availability.
- A blocked directory, failed extraction or empty search is not proof a business is absent. Continue with permitted sources when feasible and preserve the gap.
- Public business contact details are for lookup, not permission for marketing. Never send enquiries, make bookings or contact businesses as part of finding them.

[MIT license and copyright notice](references/LICENSE.md).

## Check before replying

Confirm each cited URL was actually opened, supports the **attributed website claim**, and is not a missing page. Check exclusions, duplicates, actual number of sourced candidates and the difference between address and service-area claims. Report unknowns plainly; no external actions.
