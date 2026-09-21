# Skill: ansible-demo-lookup

## Objective
Search the `product-demos` repository for available Ansible Automation Platform demos by category, keyword, or customer context. Return structured information about matching demos, their requirements, and freshness status. Proactively flag stale demos or suggest repo/skill updates.

## Repo Location
`/home/jveverka/git/product-demos/`

## Inputs
- **Query** (required): Free-text search — a keyword (e.g. "patching", "compliance", "STIG"), a category (e.g. "linux", "cloud", "network"), or a customer-relevant topic (e.g. "security hardening for RHEL fleet").
- **Category filter** (optional): Restrict to one or more categories: `linux`, `windows`, `cloud`, `network`, `openshift`, `infrastructure`, `satellite`.
- **Check freshness** (optional, default: true): Also run the freshness audit for matched demos.

## Demo Catalog Reference

The repo contains 70+ demos across 7 categories, deployed as AAP Configuration-as-Code via `infra.aap_configuration.dispatch`. Each category has its own `setup.yml` defining AAP resources.

### Categories at a Glance

| Category | Demos | Key Topics |
|---|---|---|
| `linux/` | 17 jobs, 1 workflow | Patching, compliance (CIS/HIPAA/STIG/PCI-DSS), Insights, system roles, Podman, Cockpit, sudo mgmt |
| `windows/` | 13 jobs, 1 workflow | Active Directory, IIS, Chocolatey, PowerShell, DISA STIG, patching/rollback, DSC |
| `cloud/` | 10 jobs, 3 workflows | AWS VPC/EC2 lifecycle, multi-OS provisioning, snapshot/restore, enterprise patching workflow |
| `network/` | 11 jobs, 3 workflows | Cisco NX-OS/IOS-XE, Palo Alto PAN-OS, containerlab, DISA STIG, backup/restore |
| `openshift/` | 6 jobs, 2 workflows | OpenShift Virtualization (CNV), EDA, Dev Spaces, GitLab |
| `infrastructure/` | 7+ jobs, 2 workflows | ROSA lifecycle, Config Drift + EDA remediation, HashiCorp Vault, OPA, Automation Orchestrator |
| `satellite/` | 4 jobs, 1 workflow | Content view publish/promote, satellite registration, compliance scan, patching workflow |

## Workflow Steps

### 1. Pull Latest (if online)
```bash
cd /home/jveverka/git/product-demos && git pull --ff-only 2>/dev/null || true
```
Fail silently if offline — work with local copy.

### 2. Search for Matching Demos
Based on the query, search across:
- Category README files: `/home/jveverka/git/product-demos/<category>/README.md`
- Setup definitions: `/home/jveverka/git/product-demos/<category>/setup.yml` (contains job template names, descriptions, survey specs)
- Playbook files for deeper technical detail when needed

**Search strategy:**
1. If query matches a category name exactly → list all demos in that category
2. If query is a keyword → grep across all README.md and setup.yml files
3. If query is a customer topic → map it to relevant categories/keywords (e.g. "security" → compliance, STIG, patching; "hybrid cloud" → cloud + openshift)

### 3. Build Result Table
For each matching demo, extract:

| Field | Source |
|---|---|
| **Name** | Job template name from `setup.yml` |
| **Category** | Parent directory |
| **Description** | From README or setup.yml description |
| **Playbook** | The `.yml` file that runs |
| **Survey** | Whether the demo has interactive survey variables (from setup.yml) |
| **Prerequisites** | Required credentials, inventory, external access (AWS keys, Satellite, etc.) |
| **AAP Version** | Which EE/AAP versions are supported (2.5/2.6/2.7) |

### 4. Check Demo Freshness
For each matched demo, run:
```bash
git -C /home/jveverka/git/product-demos log --since="6 months ago" --oneline -- <category>/<playbook>
```

Flag demos as:
- **Current** — modified within 6 months
- **Aging** — last modified 6–12 months ago, review recommended
- **Stale** — no changes in 12+ months, may need validation against current product versions

Also check:
- Whether the demo's required collections exist in the latest EE (`execution_environments/requirements-27.yml`)
- Whether the README mentions deprecated features or old product versions

### 5. Suggest Updates (when applicable)
At the end of every lookup, include a `## Maintenance Suggestions` section if any of these apply:

- **Stale demos found:** "Demo X hasn't been updated in Y months. Consider testing it against current AAP/RHEL versions or checking upstream for updates."
- **New upstream demos:** Compare local repo age against remote. If local is behind, suggest `git pull`.
- **Skill catalog drift:** If the product-demos repo added new categories or demos since this skill was written, suggest updating the catalog reference in this skill file.
- **Collection version drift:** If EE requirements reference older collection versions, flag it.

### 6. Format Output
Return results as a structured report:

```markdown
## Ansible Demo Search: "<query>"

### Matching Demos

| # | Name | Category | Description | Freshness |
|---|---|---|---|---|
| 1 | ... | linux | ... | ✅ Current |

### Demo Details
<For each match, a brief section with prerequisites, survey variables, and playbook path>

### Maintenance Suggestions
<Any freshness warnings, update recommendations>
```

## Rules
- **Always** search the actual repo files — never rely solely on the catalog reference table above (it may be outdated).
- **Always** report freshness status unless explicitly told not to.
- When a customer/company name is provided as context, check the Obsidian vault (`$SA_KNOWLEDGE_PATH`) for their Account Blueprint to understand their tech stack before searching. Map their environment to relevant demo categories.
- If the repo is significantly behind upstream (10+ commits), prominently suggest pulling updates.
- Demo names and descriptions should be reported in **English** (they are already in English in the repo). Any contextual commentary for the SA can be in Czech per vault conventions.
- When suggesting demos for a customer engagement, consider the **demo.redhat.com** availability — all product-demos are pre-installed there.
