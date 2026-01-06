import re

COUPLING_KEYWORDS = [
    ("sales", "inventory"),
    ("sales", "accounting"),
    ("purchase", "inventory"),
    ("returns", "inventory"),
]


def detect_cross_domain_coupling(domain_map):
    couplings = []

    for domain, files in domain_map.items():
        for item in files:
            content = item["content"].lower()
            for src, target in COUPLING_KEYWORDS:
                if src == domain and target in content:
                    couplings.append(
                        f"{src.upper()} → {target.upper()} :: {item['path']}"
                    )

    return sorted(set(couplings))
