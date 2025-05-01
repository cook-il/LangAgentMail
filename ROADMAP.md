## 🗺️ Roadmap

LangAgentMail follows a deliberate versioning plan tied to infrastructure, identity, and response capabilities.

### ✅ v0.0.9 — Infrastructure Milestone (Current)
- RFC-compliant DNS + mail routing (BIND, SPF, DKIM, DMARC)
- Working dual-stack IPv4/IPv6 with TCP/UDP
- SMTP relay via YunoHost with trusted domain/IPs
- PGP identity + SSH-secured GitHub deploys
- Signed commits and echo replies via `info@cook-il.us`

---

### 🛠 v0.1.x — Command-aware Responses
- Basic text normalization, stripping HTML/CSS/graphics
- Free-form command parsing (e.g. `/status`, `/help`)
- Improved reply formatting
- Manual message archival grouped by sender
- Internal logging with source timestamps

---

### 🧠 v0.2.x — LangChain Integration
- Embedding via OpenAI or self-hosted LLMs
- Query classification and memory-aware replies
- Context chaining across multi-turn instructions
- Publicly queryable conversation snapshots (optional)

---

### 🔐 v0.3.x — Audit & Access Layer
- Cryptographically verifiable message logs
- Optional GPG key pinning for inbound messages
- Role-based controls for subdomain users
- API gateway compatibility for non-email access

---

### 🎯 v1.0.0 — First Civic-Ready Release
- Full CLI/web onboarding flow
- Exportable identity + deployment package
- Localized models (optional)
- Tested compatibility with multiple subdomains and isolated agents

# langagent/pgp/roadmap/deferred-v1

## 🔁 Post-MVP Security Enhancements

### PGP Signing for Automated Replies

**Status:** Deferred  
**Component:** LangAgentMail (`aiagent@cook-il.us`)  
**Reason:** PGP signing via Roundcube (Enigma) is working for webmail replies, but system-generated messages sent via remote shell or cron bypass signing.  

**Planned Action:**  
Implement cryptographic signing of all automated messages using `gpg --clearsign`, `mutt`, or wrapper scripts.

**Trigger for Reinstatement:**  
After LangAgentMail's reply automation and message routing are stable.

**Note:**  
This does not impact current public-facing replies from `info@cook-il.us`, which are already PGP-signed and verified.
