# Skills

Public skill packages by Jake Marchin-Vincent. Each released skill has a `SKILL.md`, supporting files and its own license. Private development candidates are not published here.

| Skill | Status | What it does |
| --- | --- | --- |
| [Australian Business Finder](skills/aus-business-finder-mv/SKILL.md) | Public beta | Finds Australian business candidates with opened source pages. [How to use it and what testing found](docs/aus-business-finder/README.md). Not an independent business verification service. |
| [Outreach Sequencing](skills/dusk-outreach-sequencing/SKILL.md) | Public beta | Turns a user's offer and prospect evidence into reviewable outbound email drafts. No email provider or CRM required; never sends on installation. |

## Install in Hermes

```sh
hermes skills install JakeMarchin-Vincent/skills/aus-business-finder-mv
hermes skills install JakeMarchin-Vincent/skills/skills/dusk-outreach-sequencing
```

Review a skill before installing it. A direct install is not an official Hermes catalog listing or endorsement. Start a fresh Hermes session after installing.

## Outreach Sequencing

Provide your sender identity, truthful offer, desired recipients and what you know about them. For example: “Draft a first-touch email and optional follow-up for my appointment software. I am Morgan at CedarDesk; here is my offer and prospect brief. Do not send anything.” The skill works from pasted facts; web research is optional when authorised and available. Unknown permission or compliance requirements result in an illustrative **REVIEW REQUIRED — DO NOT SEND** draft.

This is an agent **draft-and-review workflow**, not an autonomous lead database or sending system. It does not require an EMVY account, particular CRM, Convex, Resend, a specific industry or a fixed three-touch cadence. Developers planning live automation should read the [implementation contract](skills/dusk-outreach-sequencing/references/implementation-contract.md) and build a tested sender for their own stack. The [MIT notice](skills/dusk-outreach-sequencing/references/LICENSE.md) applies to this package.

The former nested path `skills/outreach/dusk-outreach-sequencing` contained an unsafe sender example and is replaced by the flat Hermes-discoverable path above. Existing direct installs should be updated to the new identifier; do not keep running the older sender example.

## Australian Business Finder

Its [MIT notice](skills/aus-business-finder-mv/references/LICENSE.md) covers that package. The [0.4.0 development evaluation](docs/aus-business-finder/EVALUATION-0.4.0.md) and [earlier eight-case evaluation](docs/aus-business-finder/EVALUATION.md) report both sourced candidates and misses. This is a source-linked discovery aid, not a verified directory or a demonstrated improvement over ordinary research.

## Legacy operations document

The EMVY-specific outreach operations document has been removed from the current tree. It was not a portable skill and should be maintained only in an approved private location. **Removing a file from the current branch does not erase its earlier public Git history.** Assess any prior operational disclosure separately.

## Verification

Test the published revision in a clean Hermes installation; local package checks and a synthetic agent trial do not establish performance across models, hosts, jurisdictions or real campaigns. No bundled skill in this repository grants permission to send outreach or change external records.
