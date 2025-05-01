# TAGS.md

LangAgentMail – Tag History and Milestone Tracking

This file records all Git tags used in the project, with context, version scope, and linkage to roadmap or deferred items.

---

## 🔖 v0.0.9 — Infrastructure Milestone

**Git Tag:** `v0.0.9`  
**Status:** Active  
**Committed:** [YYYY-MM-DD] (update with actual date)

### Summary

- DNS: RFC-compliant with SPF, DKIM, DMARC
- Mail routing via YunoHost SMTP relay
- DNS Master-Slave sync live (IPv4/IPv6)
- PGP key configured for `aiagent@cook-il.us`
- Roundcube-based signature confirmation
- Webmin and SSH remote access hardened
- GitHub commits secured via SSH + GPG
- CONTRIBUTING.md published with philosophy and access model

### Related Roadmap Milestone

- `v0.0.9 — Infrastructure Milestone (Current)` in `ROADMAP.md`

### Deferred Under This Tag

- `langagent/pgp/roadmap/deferred-v1`  
  ➤ Signing of echo replies deferred (see `ROADMAP.md`)

---

## 🛠 Next Planned Tag: v0.1.0 — Command-aware Responses

Will mark the introduction of:
- Command parsing (`/help`, `/status`)
- Log-aware routing and AI reply formatting
