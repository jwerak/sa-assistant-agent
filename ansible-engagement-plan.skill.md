# Skill: ansible-engagement-plan

## Objective
Plan an Ansible Automation Platform engagement (demo, workshop, PoC, discovery) for a specific customer. Combines account context from the Obsidian vault with available demos from the `product-demos` repository to produce a structured engagement plan with a tailored demo agenda, prerequisites checklist, and follow-up actions.

## Repo Location
`/home/jveverka/git/product-demos/`

## Inputs
- **Company** (required): Canonical account or partner name (see CLAUDE.md).
- **Engagement type** (required): One of `demo`, `workshop`, `discovery`, `poc`, `qbr`.
- **Focus areas** (optional): Specific topics the customer is interested in (e.g. "RHEL patching and compliance", "hybrid cloud with AWS", "network automation").
- **Duration** (optional): Available time for the engagement (e.g. "2 hours", "half day", "full day").
- **Audience** (optional): Who will attend — sysadmins, management, security team, developers.
- **AAP version** (optional): If known, which AAP version the customer has or will use (2.5/2.6/2.7). Defaults to 2.7.

## Workflow Steps

### 1. Resolve Vault Path & Read Account Context
Read `SA_KNOWLEDGE_PATH` from `.env`. Then gather context:

1. **Account Blueprint:** Read `$SA_KNOWLEDGE_PATH/SA_Knowledge/Accounts/<Company>.md` for:
   - Tech stack and infrastructure landscape
   - Active projects and initiatives
   - Key stakeholders and their roles
   - Previous engagement history
   - Pain points and strategic priorities

2. **Recent Meetings:** Search `$SA_KNOWLEDGE_PATH/SA_Knowledge/Meetings/` for recent meeting notes with `company: "[[<Company>]]"` to understand current context and momentum.

3. **Open Tasks:** Check `$SA_KNOWLEDGE_PATH/SA_Knowledge/Tasks/` for open action items related to this account.

If no vault data exists for this company, proceed with the user-provided focus areas only, and note that account context was unavailable.

### 2. Map Customer Context to Demo Categories

Use this mapping to identify relevant demo categories:

| Customer Signal | Demo Categories | Key Demos |
|---|---|---|
| RHEL fleet, Linux operations | `linux/` | Patching, Compliance (STIG/CIS/HIPAA), System Roles, Insights |
| Windows Server, AD environment | `windows/` | AD Setup, IIS, Chocolatey, DISA STIG, PowerShell |
| AWS/cloud workloads | `cloud/` | Cloud Stack Deploy, EC2 lifecycle, Patching Workflow |
| Network infrastructure, firewalls | `network/` | Containerlab, Palo Alto, DISA STIG, Backup/Restore |
| Kubernetes, containers | `openshift/` | CNV, EDA, Dev Spaces |
| Satellite, content management | `satellite/` | Patch Dev Workflow, Content Views, Compliance |
| Security, compliance, audit | `linux/`, `windows/`, `network/` | Multi-profile Compliance, DISA STIG (all platforms), OpenSCAP |
| Event-driven automation | `openshift/`, `infrastructure/` | EDA Install, Config Drift Remediation |
| Cloud-native infrastructure | `infrastructure/` | ROSA, HashiCorp Vault, OPA |

### 3. Select and Sequence Demos

Based on the mapping, select demos that:
1. **Match customer priorities** — address their stated interests and pain points
2. **Tell a story** — sequence demos to build from simple to complex, showing a logical progression
3. **Fit the time budget** — estimate ~10-15 min per standalone demo, ~20-30 min per workflow demo
4. **Match the audience** — technical depth for sysadmins, business value for management

**Sequencing principles:**
- Start with a **high-impact, low-complexity demo** to build confidence (e.g. Patching, Troubleshoot)
- Progress to **domain-specific demos** matching their focus areas
- End with a **workflow demo** that shows end-to-end automation (e.g. Compliance Workflow, Cloud Patching Workflow)
- For workshops, include hands-on time between demos

### 4. Identify Prerequisites

For each selected demo, check `setup.yml` and document:

- **AAP Resources:** Credentials, inventories, projects needed
- **External Access:** AWS keys, Satellite instance, network lab, OpenShift cluster
- **Environment:** demo.redhat.com vs. customer's own AAP instance
- **Execution Environment:** Which EE image is needed (apd-ee-25/26/27)
- **Pre-setup:** Whether `setup_demo.yml` needs to run first

### 5. Build the Engagement Plan

Output a structured plan:

```markdown
## Ansible Engagement Plan: <Company>

### Engagement Overview
- **Type:** <demo/workshop/discovery/poc/qbr>
- **Company:** [[<Company>]]
- **Duration:** <estimated or provided>
- **Target Audience:** <roles>
- **AAP Version:** <version>
- **Environment:** demo.redhat.com / customer AAP

### Account Context Summary
<2-3 sentences on relevant account background, current initiatives, why this engagement matters>

### Demo Agenda

| # | Time | Demo | Category | Purpose |
|---|---|---|---|---|
| 1 | 00:00-00:15 | <Demo Name> | linux | <Why this demo for this customer> |
| 2 | 00:15-00:30 | ... | ... | ... |

### Talking Points
<Per-demo bullet points connecting the demo capability to the customer's specific situation>

### Prerequisites Checklist
- [ ] AAP environment provisioned (demo.redhat.com / customer)
- [ ] EE image: `apd-ee-<version>`
- [ ] Product demos installed: `ansible-navigator run install-apd.yml`
- [ ] <Specific credentials/access needed>
- [ ] Demo categories set up: `setup_demo.yml -e demo=<category>`

### Follow-up Actions
<Suggested next steps: PoC proposal, architecture workshop, trial activation, etc.>

### Demo Freshness Check
<Flag any selected demos that are aging or stale — run git log check>
```

### 6. Optionally Create Vault Artifacts
If the user approves, create:
- A **meeting prep note** in `Meetings/` with the engagement plan as body (using `prep` type)
- **Task notes** in `Tasks/` for any prerequisites that need action before the engagement

### 7. Suggest Follow-up Skills
At the end, recommend:
- After the engagement: run `process-notes` to capture outcomes
- If new contacts were identified: run `manage-contact`
- If action items emerged: create tasks in the vault
- If the engagement revealed new customer needs: suggest updating the Account Blueprint

## Rules
- **Always** read the actual repo files for demo details — never rely on cached/memorized info.
- **Always** verify demo freshness for selected demos before recommending them.
- **Never** recommend a demo without checking that its prerequisites are realistic for the customer's environment.
- **Engagement plan language:** The plan structure and demo names stay in English. Talking points and context summary follow vault language convention (Czech by default).
- When no Account Blueprint exists, create a minimal one after the engagement if significant account info was gathered.
- For `discovery` type engagements, emphasize breadth — show demos across multiple categories. For `poc` type, go deep on 2-3 demos with hands-on time.
- **demo.redhat.com** is the preferred environment for demos unless the customer specifically wants to see their own AAP. Always mention this option.
