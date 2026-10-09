# Evaluation — Australian Business Finder v0.3.0

The fixed-point tests below were performed against the original standalone repository before consolidation. The package moved here without behavioural changes; this report does not claim a fresh live evaluation of the consolidated copy.

**Public beta, evaluated 9 October 2026 (Australia/Perth).** Fixed point: [`a76461ea906a9bd92aedab4f95fa1089276ae284`](https://github.com/JakeMarchin-Vincent/aus-business-finder/commit/a76461ea906a9bd92aedab4f95fa1089276ae284). This is a curated public report of real tests, including negative results; it is **not** a claim of national coverage, business verification, or improvement over an ordinary agent.

## What was tested

- Eight Australian business-finding/research cases were run with the skill explicitly loaded and with an ordinary-agent baseline. The same advertised web tools and a per-case ceiling of three searches and approximately five page opens were used. The arms were not a blinded, controlled experiment: the baseline continuation could consult its own earlier research, and page access and opener choices varied.
- R1–R3 were reconstructed known regression classes, **not untouched holdouts**. The first parallel attempt suffered shared-browser wrong-page snapshots and was discarded for paired scoring; the scored skill arm was rerun serially. Results below are from the isolated rerun and the audited baseline continuation.
- A *useful sourced candidate* needed an opened page supporting the requested offering, geographical relationship, and any shop/branch/exclusion constraint. A publisher's page supports an **attributed website claim**, not independent proof of trading, physical occupancy, stock, licensing, suitability or availability. Directory snippets, 404/blocked pages and unsafe TLS bypasses were not positive evidence.
- The configured `web_extract` backend was search-only and failed during the paired test. Browser opening and other safe readable page routes sometimes recovered first-party pages. The baseline used an invalid-certificate bypass once; that result was excluded. The skill arm did not bypass TLS.

## Reproduction prompts (equivalent constraints; not the original verbatim transcripts)

Use each independently with the same model, tools and search/open budget; in the skill arm explicitly load `aus-business-finder-mv`, and in the baseline arm do not load it. Ask for exact opened URLs, check date and remaining unknowns. Never contact a business.

1. **R1:** Find two termite-inspection businesses whose websites publish a street address in Mildura, Victoria. A PO Box or general “local” claim does not qualify.
2. **R2:** Find two Rockhampton walk-in shops advertising computer accessories. An office, delivery area or catalogue alone does not establish a shop or stock.
3. **R3:** Find three businesses explicitly advertising commercial kitchen-exhaust cleaning to Toowoomba. A general Queensland claim alone does not qualify.
4. **R4:** Find two providers advertising mobile hydraulic-hose repair in Wagga Wagga. Separate a named local provider from a network advert or statewide claim.
5. **R5:** Research the exact named business Prime Vent Solutions. Report kitchen-exhaust work and Toowoomba coverage only if an opened source supports them; give a legal identity/ABN only with a confident link.
6. **R6:** Find two commercial-refrigeration repairers advertising Adelaide service, excluding LJ Refrigeration and BOSSY'S Refrigeration. Copy a public contact only if shown on the opened page.
7. **R7:** Research the exact name “Nullarbor Quantum Refrigeration Pty Ltd” in Ceduna. Do not substitute a similar name; distinguish no sourced match from nonexistence.
8. **R8:** Find a walk-in Broken Hill shop advertising replacement pool-pump motors. Do not count generic motors, automotive parts, remote delivery or an unconfirmed branch.

## Eight-case scorecard

Counts mean *usable sourced candidates as presented in the answer* / candidates requested. They are **not** a discovery recall rate, since the complete set of operating businesses is unknown. The descriptions below preserve the hard constraints but are not claimed to be verbatim original prompts.

| Case / constraint | Skill | Ordinary agent | Audited observation |
|---|---:|---:|---|
| R1: Two Mildura termite-inspection providers with a published street address | **0/2** | **2/2** | Skill missed **20 Sherring Way** on [Murray Outback Pest's opened page](https://pestcontrolmildura.com.au/). Baseline also found [Mildura Property Inspections](https://www.mildurapropertyinspections.com/), whose page listed 111 Almond Avenue and termite inspections. Neither address proves occupancy. |
| R2: Two Rockhampton walk-in computer-accessory shops, not offices | **1/2** | **2/2** | Both counted [Harvey Norman Rockhampton North](https://stores.harveynorman.com.au/harvey-norman-rockhampton-north-qld) as a website-described store; catalogue presence does not prove stock. Skill stopped after [King IT's store page](https://kingit.com.au/King-IT-Rockhampton) was browser-blocked; the baseline/independent safe renderer read its shop/accessory/address claims. |
| R3: Three businesses explicitly advertising commercial kitchen-exhaust cleaning in Toowoomba | **0/3** | **1/3** admissible | Skill overlooked **Kitchen Exhaust** in the service categories on the [Clean-Air Toowoomba page](https://cleanairaust.com.au/locations/toowoomba/). Baseline's other Prime Vent result required invalid-certificate bypass and was **excluded**. [SAIS's dedicated page](https://www.saishygiene.com.au/toowoomba-kitchen-exhaust-canopy-cleaning/) was accessible in an exploratory run but missed in the scored arms. |
| R4: Two providers advertising mobile hydraulic-hose repair in Wagga Wagga | **1/2** | **1/2** firm | Both opened [BOA's Miller Diesel provider page](https://boahydraulics.com/hydraulic-hose-repair-wagga-wagga). Baseline also promoted a Pirtek **recruitment advert** to a current customer-facing provider; this was downgraded to a clue, not counted. |
| R5: Research exact-name Prime Vent Solutions; legal identity only if confidently linked | **0** | **0** admissible | The [site](https://primeventsolutions.com.au/about-us) had an invalid HTTPS certificate. Neither arm could securely source its claims or link a legal identity/ABN. Baseline's certificate-bypassed reading was excluded. This does not establish the business is absent. |
| R6: Two Adelaide commercial-refrigeration repairers, excluding LJ and BOSSY'S | **2/2** | **2/2** | Skill returned [Adelaide Fridge Repair](https://www.adelaidefridgerepair.com/commercial-fridge-repairs) and [Shiraz Refrigeration](https://shirazrefrigerationadelaide.com.au/) with relevant published claims. **Failure:** it appended `.au` to Shiraz's email; the opened site's `mailto:` ended in `.com`. Do not copy that contact from the test output. |
| R7: Exact fabricated name “Nullarbor Quantum Refrigeration Pty Ltd” in Ceduna; do not substitute similar names | **0, bounded no-match** | **0, bounded no-match** | Neither promoted a similarly named business or assigned an ABN. Baseline opened ABN Lookup's homepage, **not** a completed register search. No-match is limited to sources checked. |
| R8: Walk-in Broken Hill shop selling replacement pool-pump motors | **0, bounded no-match** | **0, bounded no-match** | Neither misrepresented [Silver City Motors' automotive parts page](https://www.silvercitymotors.com.au/parts/) or a non-local repairer as a qualifying pool-motor shop. This does not prove no such shop exists. |

**Clearly supported presented candidates:** skill **4**, ordinary baseline **8** after excluding the invalid-TLS result and downgrading the recruitment advert. This small, adversarial, nonrandom set provides **no evidence of a with-skill performance lift**. All four counted skill candidates had opened pages supporting their requested category and claimed geography, but the skill also made **three concrete claim-level mistakes**: two false-negative page readings (R1 and R3) and one wrong email suffix (R6). These matter even though the wrong-email business was otherwise a valid candidate. No independently verified businesses, stock or premises were established by either arm.

## Fresh public-package checks

On 9 October 2026, `hermes -p default skills install JakeMarchin-Vincent/aus-business-finder/skills/aus-business-finder-mv --yes` was run with an isolated `HERMES_HOME`. The community safety scan returned **SAFE / ALLOWED**, and the installed `SKILL.md` matched the public file byte-for-byte (SHA-256 `b37f1586c9750234faf6dc04adf4f910e594571c7e8ad07a071e7b1ce9f2e86d`). This verifies package retrieval and installation, **not** model behaviour in that credential-free home.

A fresh **one-case live lookup in MEWY's configured profile**, with the skill preloaded, returned [Cool-Time's commercial refrigeration page](https://cool-time.com.au/commercial-refrigeration-adelaide/) as an Adelaide candidate. The agent's trace shows it opened that exact first-party page. A separate HTTPS read returned 200 and confirmed the quoted installation/repair/maintenance and metro Adelaide/Adelaide Hills service-area language and listed phone number. No business was contacted. Search in that run was impaired (`web_search` provider `ddgs` unavailable; Google challenged the browser), so the agent used browser search and a first-party page opener. **One successful example does not cancel the eight-case failures.**

## Timing, cost, repeatability and next test

The serial eight-case skill run's measured wall window was **364 seconds**; the baseline continuation was **237.67 seconds**, but relied on an earlier **501.55-second** research attempt, some concurrent/cross-contaminated. These are not comparable end-to-end single-run latencies. Tool calls were 37 in the skill rerun, 21 in baseline continuation, and 50 in the earlier baseline attempt; these are workload clues, **not billable costs**. Provider charges were unavailable.

The highest-value next revision is a **decisive-claim check**: before saying a required detail is absent, inspect the entire opened page (including location-specific categories, footer and contact links); copy contact details exactly; try one safe targeted query or alternate opener for an unresolved decisive fact within a bounded budget. Re-run the same cases serially, then use a genuinely new holdout. Measure supported candidates, false matches, omissions, unsupported claims, access failures, wall time and billable cost where available. This is a proposed improvement, **not yet implemented or proven**.

## Evidence boundary

This report publishes the rubric, case constraints, audited results, example source URLs, and limitations. Raw agent session exports are **not** published: they contain private profile/runtime context and unredacted public contact details and are not safe or necessary as a portfolio artifact. Earlier C01–C03 traces and the full internal case-by-case transcripts remain private. The public report is sufficient to inspect what was tested and where it failed, but cannot reproduce identical model outputs: search indices, sites, model aliases and web access change. There are no automated test scripts in this repository, no isolated-home live model trial, and no cross-platform or paid-user study.
