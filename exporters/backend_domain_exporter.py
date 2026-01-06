import os
from core.backend_domain_extractor import detect_backend_domains
from core.coupling_extractor import detect_cross_domain_coupling


def export_backend_domains(tree_root, project_root):
    os.makedirs("output", exist_ok=True)

    domain_map = detect_backend_domains(tree_root)

    for domain, files in domain_map.items():
        out_file = f"output/B0{list(domain_map.keys()).index(domain)+1}_{domain}_system_map.txt"

        with open(out_file, "w", encoding="utf-8") as f:
            f.write(f"### {domain.upper()} BACKEND SYSTEM MAP ###\n")

            for item in files:
                rel = os.path.relpath(item["path"], project_root)
                f.write(
                    f"\n--- ROLE: {item['role']} | FILE: {rel} ---\n"
                )
                f.write(item["content"])

    # Cross-domain coupling
    couplings = detect_cross_domain_coupling(domain_map)

    with open(
        "output/B99_cross_domain_coupling.txt",
        "w",
        encoding="utf-8"
    ) as f:
        f.write("### CROSS DOMAIN COUPLING MAP ###\n\n")
        for c in couplings:
            f.write(f"- {c}\n")
