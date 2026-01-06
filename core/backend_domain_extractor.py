import os

DOMAIN_RULES = {
    "sales": ["sales", "invoice"],
    "purchase": ["purchase", "supplier"],
    "inventory": ["inventory", "stock"],
    "accounting": ["account", "ledger", "voucher", "gst"],
    "service": ["service", "job"],
}

ROLE_HINTS = {
    "ENTITY": ["Entity", "@Entity"],
    "DAO": ["Dao", "@Dao"],
    "REPOSITORY": ["Repository"],
    "USECASE": ["UseCase"],
    "FACADE": ["Facade"],
    "SERVICE": ["Service"],
}


def detect_backend_domains(tree_root):
    domain_map = {d: [] for d in DOMAIN_RULES.keys()}

    def walk(node):
        if not node.is_dir and node.path.endswith(".kt"):
            path_lower = node.path.lower()

            try:
                with open(node.path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception:
                return

            for domain, keywords in DOMAIN_RULES.items():
                if any(k in path_lower for k in keywords):
                    role = "OTHER"
                    for r, hints in ROLE_HINTS.items():
                        if any(h in content or h in node.path for h in hints):
                            role = r
                            break

                    domain_map[domain].append(
                        {
                            "path": node.path,
                            "role": role,
                            "content": content,
                        }
                    )

        for child in node.children:
            walk(child)

    walk(tree_root)
    return domain_map
