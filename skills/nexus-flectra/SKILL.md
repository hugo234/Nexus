---
name: nexus-flectra
description: Connects Nexus to Odoo/Flectra ERP using XML-RPC.
metadata:
  {
    "nexus":
      {
        "emoji": "🔗",
        "requires": { "env": ["FLECTRA_URL", "FLECTRA_DB", "FLECTRA_USER", "FLECTRA_PASSWORD"] },
        "primaryEnv": "FLECTRA_URL"
      }
  }
---

# Nexus Flectra Skill

Use this skill to interact with Flectra/Odoo instances via XML-RPC.

Configure your credentials in the `.env` file or in `~/.nexus/nexus.json`.

```bash
python {baseDir}/scripts/flectra_client.py --action search_read --model res.partner
```
