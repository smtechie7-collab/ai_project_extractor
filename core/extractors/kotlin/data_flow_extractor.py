import re
from core.utils.file_reader import read_text_file

# --- REGEX PATTERNS ---

# 1. Class Definition (handles standard primary constructors, annotations like @Inject, and explicit constructor)
CLASS_DEF_PATTERN = re.compile(
    r'class\s+([A-Za-z0-9_]+)(?:<[^>]+>)?\s*(?:@[A-Za-z0-9_.]+(?:\([^)]*\))?\s*)*(?:(?:private|protected|internal|public)\s+)?(?:constructor)?\s*\(([^)]+)\)', 
    re.MULTILINE
)

# 2. Parameter Extraction (handles modifiers, annotations, val/var, and param types)
PARAM_PATTERN = re.compile(r'(?:(?:private|protected|public|internal)\s+)?(?:val|var)?\s*(?:@[A-Za-z0-9_.]+\s+)?(\w+)\s*:\s*([A-Za-z0-9_<>.]+)')

# 3. Instantiation inside Return Statements (Common in AppContainer helper functions)
# Looks for: return MyViewModel( ... )
RETURN_INSTANTIATION_PATTERN = re.compile(r'return\s+([A-Z]\w+ViewModel(?:Factory)?)\s*\(([\s\S]*?)\)')

# 4. Standard Instantiation
INSTANTIATION_PATTERN = re.compile(r'([A-Z]\w+ViewModel(?:Factory)?)\s*\(([\s\S]*?)\)')

def extract_data_flow(tree_root):
    registry = {}
    
    def register_class(name, dependencies, source_type):
        if name not in registry:
            registry[name] = {"params": set(), "type": _guess_type(name)}
        
        for dep in dependencies:
            clean_dep = dep.split('<')[0].split('.')[-1]
            if clean_dep not in ["Context", "Application", "String", "Int", "Long", "Boolean", "null"]:
                registry[name]["params"].add(clean_dep)

    def extract_deps_from_args(args_block):
        deps = []
        # Key = Value pattern
        for assign in re.findall(r'(\w+)\s*=', args_block):
            deps.append(_capitalize_first(assign))
        
        # Direct Variable pattern (e.g. (repo, dao))
        if not deps:
             for var in re.findall(r'(\w+)(?=[,\)])', args_block):
                 if var not in ["null", "true", "false"]:
                     deps.append(_capitalize_first(var))
        return deps

    def walk(node):
        if node.is_dir:
            for child in getattr(node, "children", []):
                walk(child)
            return

        if node.path.endswith(".kt"):
            try:
                code = read_text_file(node.path)
            except Exception:
                return

            # --- STRATEGY 1: Parse Class Definitions ---
            for match in CLASS_DEF_PATTERN.finditer(code):
                cls_name = match.group(1)
                args_block = match.group(2)
                deps = []
                for p_match in PARAM_PATTERN.findall(args_block):
                    deps.append(p_match[1]) 
                register_class(cls_name, deps, "DEFINITION")

            # --- STRATEGY 2: Deep Scan for Instantiations (AppContainer) ---
            # Check specifically for 'return ViewModel(...)' patterns
            for match in RETURN_INSTANTIATION_PATTERN.finditer(code):
                cls_name = match.group(1)
                args_block = match.group(2)
                deps = extract_deps_from_args(args_block)
                register_class(cls_name, deps, "RETURN_STATEMENT")

            # --- STRATEGY 3: General Instantiations (Factories) ---
            if "Factory" in node.name or "AppContainer" in node.name:
                for match in INSTANTIATION_PATTERN.finditer(code):
                    cls_name = match.group(1)
                    args_block = match.group(2)
                    deps = extract_deps_from_args(args_block)
                    register_class(cls_name, deps, "INSTANTIATION")

    walk(tree_root)
    return _build_flow_report(registry)

def _capitalize_first(s):
    if not s: return s
    return s[0].upper() + s[1:]

def _guess_type(name):
    if "ViewModel" in name: return "VM"
    if "Repository" in name: return "REPO"
    if "Dao" in name: return "DAO"
    if "UseCase" in name: return "USECASE"
    return "OTHER"

def _build_flow_report(registry):
    lines = []
    lines.append("=" * 60)
    lines.append("DATA FLOW TRACER (ViewModel -> Repository -> Dao)")
    lines.append("=" * 60)
    lines.append("")

    vms = [k for k, v in registry.items() if v["type"] == "VM"]
    
    if not vms:
        lines.append("No ViewModels found.")
        return "\n".join(lines)

    for vm in sorted(vms):
        # We generally skip Factories in the final report to keep it clean,
        # unless they are the only source of truth.
        if "Factory" in vm:
            continue
            
        vm_data = registry[vm]
        deps = sorted(list(vm_data["params"]))
        
        lines.append(f"ViewModel: {vm}")
        
        if not deps:
            lines.append("  └── (No dependencies detected)")
        
        for dep in deps:
            if "Repository" in dep or "Dao" in dep or "UseCase" in dep or "Facade" in dep:
                is_known = dep in registry
                type_tag = registry[dep]["type"] if is_known else "INFERRED"
                
                lines.append(f"  └── {dep} ({type_tag})")
                
                if is_known:
                    sub_deps = sorted(list(registry[dep]["params"]))
                    for sub in sub_deps:
                        if "Dao" in sub or "Repository" in sub:
                             lines.append(f"      └── {sub} (DAO/REPO)")

    return "\n".join(lines)