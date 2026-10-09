# Skills

Public skill packages by Jake Marchin-Vincent. Each released skill lives in its own directory with a `SKILL.md` and any supporting files. Private development candidates are not published here.

| Skill | Status | What it does |
| --- | --- | --- |
| [Australian Business Finder](skills/aus-business-finder-mv/SKILL.md) | Public beta | Finds Australian business candidates with opened source pages. [How to use it and what testing found](docs/aus-business-finder/README.md). Not an independent business verification service. |
| [dusk-outreach-sequencing](skills/outreach/dusk-outreach-sequencing/SKILL.md) | Existing public material; review pending | Generalised email-outreach sequence pattern. |
| [emvy-outreach-templates](skills/outreach/emvy-outreach-templates/SKILL.md) | Existing public material; review pending | Older EMVY-specific outreach instructions; the label “internal” did not restrict access to this public repository. Do not rely on it as a current operations runbook. |

## Install Australian Business Finder in Hermes

```bash
hermes skills install JakeMarchin-Vincent/skills/aus-business-finder-mv
```

Its [MIT notice](skills/aus-business-finder-mv/references/LICENSE.md) covers that package; it does not license the other material in this repository. The [evaluation](docs/aus-business-finder/EVALUATION.md) reports limitations and negative results alongside successful examples. Installation is not evidence that its answers outperform ordinary research.

The two legacy outreach files remain at their existing paths to avoid silently breaking links. They are not in the default flat `skills/<slug>/SKILL.md` layout used by Hermes tap discovery; do not assume a tap lists them. This repository is still undergoing consolidation.
