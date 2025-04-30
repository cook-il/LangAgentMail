# LangAgentMail

**LangAgentMail** is a reference design and first implementation of a self-hosted AI email agent, built on [LangChain](https://www.langchain.com/) and deployed as part of a secure, domain-anchored communication stack.

Version **0.0.9** represents the first working milestone, where the system receives free-form email requests via `info@cook-il.us` and sends back automated responses. At this stage, the system operates in echo mode, and responses are cryptographically signed using GPG.

The primary accomplishment in this release is not the AI reply logic itself, but the establishment of a **fully RFC-compliant infrastructure**:
- ✅ Hardened **BIND DNS** with isolated configuration
- ✅ Working **IPv4 and IPv6** for both **UDP and TCP** protocols
- ✅ Verified **SPF**, **DKIM**, and **DMARC** policy enforcement
- ✅ Clean, reputation-free IPs and domains (no blacklisting)
- ✅ End-to-end cryptographic trust via **PGP** for commit signing and email identity
- ✅ **SSH-based GitHub deployment** and push infrastructure
- ✅ Verified GPG signatures on every commit and outbound reply

This setup is intended to serve as a civic-grade template. The recommended deployment stack involves:
- A **main domain** (e.g., `cook-il.us`) handling all email delivery and cryptographic policy
- One or more **subdomains** (e.g., `ai.cook-il.us`) operating AI interfaces or application endpoints
- A shared mailbox relay and identity system for secure, multi-domain routing

Future versions will build upon this foundation to add structured parsing, natural language understanding, request classification, and multi-turn semantic reply behavior.

---

## 🗺️ Roadmap

See [`ROADMAP.md`](./ROADMAP.md) for the full versioned milestone plan through v1.0.

---

## 📜 License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

LangAgentMail is intended for use by individuals and civic groups whose goals align with the reference deployment at [cook-il.us](https://cook-il.us). This license permits full use, study, and modification, but **requires that any publicly hosted derivative works must also release their source code**.

The AGPL-3.0 protects LangAgentMail from closed commercial forks and ensures that improvements remain available to the public.

🔗 [View full license](https://www.gnu.org/licenses/agpl-3.0.html)
