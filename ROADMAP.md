## 🗺️ Project Roadmap

LangAgentMail follows a deliberate versioning plan tied to infrastructure, identity, and response capabilities.

### ✅ v0.0.9 — Infrastructure Milestone (Done)
- RFC-compliant DNS + mail routing (BIND, SPF, DKIM, DMARC)
- Working dual-stack IPv4/IPv6 with TCP/UDP
- SMTP relay via YunoHost with trusted domain/IPs
- PGP identity + SSH-secured GitHub deploys
- Signed commits and echo replies via info@cook-il.us
- `.env`-based credential management
- Virtualenv setup with reproducible `requirements.txt`

---

### ✅ v0.1.1 — Message Ingestion and HTML Sanitization (Done)
- IMAP polling using unseen filter
- SQLite-backed queue (`mailstore.db`) with message metadata
- Normalization pipeline: strip HTML/CSS/JS, decode safely
- Persistent status tracking (`pending`, `processed`)
- Message preview and state updates via `post_process.py`

---

### ✅ v0.1.2 — Command-aware Responses (Done)
- Free-form command parsing (e.g. `/status`, `/help`)
- Improved formatting of AI replies (clear prompts, inline context)
- Reply only to verified domains or whitelisted senders
- Internal logging with source timestamps for traceability

---

### ✅ v0.1.3 — Reply Queuing and Delivery (Done)
- Replies stored in SQLite (`replies` table)
- Includes sender, subject, and reply content
- Secure delivery using `smtplib` and STARTTLS
- Regex-based parsing of sender from "Name 'email'"
- Only whitelisted domains are allowed to receive replies

---

### ✅ v0.1.4 — Archiving and Tagging (Done)
- `messages` table now includes `archived_at` and `tag`
- `/mine` command archives all prior messages from sender
- Tag format: `mine-localpart` (e.g., `mine-theron`)
- Updated `/help` to reflect new command set

---

### ✅ v0.2.0 — LangChain Integration (Done)
- `/ask` and `/ai` commands now routed through LangChain
- Uses up to 5 prior messages from the sender as context
- Archived messages tagged and passed as prompt input
- Modern LangChain syntax: `prompt | llm`, `.invoke()`, `.content`
- Foundation laid for full RAG pipeline with FAISS/Chroma

---

### ✅ v0.2.1 — Prompt Engineering (Done)
- Prompts now include subject, sender, and message history
- AI replies use consistent, polite, minimal tone
- Replies remain graceful when no prior messages exist
- Controlled hallucination acts as privacy shield

---

### 🟡 v0.2.2 — User-defined Tags & Command Chaining (Next)
- Support `/tag something` to apply custom tags to archived messages
- Enable command chaining: `/mine && /status`, etc.
- Begin concept of user profiles or per-domain behavior presets

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

---

### 🔁 Deferred Items

- **Signed commits and echo replies via `info@cook-il.us`**  
  Status: **Deferred**  
  Reason: PGP signing works in Roundcube for webmail, but not yet implemented for automated replies from `aiagent` or non-interactive scripts.  
  Will be reinstated once LangAgentMail reply automation is finalized and GPG integration extended to backend processes.
