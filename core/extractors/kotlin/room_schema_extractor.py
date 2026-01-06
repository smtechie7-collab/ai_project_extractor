import re
import os
from core.utils.file_reader import read_text_file

# Regex patterns for Room
ENTITY_PATTERN = re.compile(r'@Entity')
TABLE_NAME_PATTERN = re.compile(r'tableName\s*=\s*"([^"]+)"')
CLASS_NAME_PATTERN = re.compile(r'data\s+class\s+(\w+)')
FIELD_PATTERN = re.compile(r'(val|var)\s+(\w+)\s*:\s*([A-Za-z0-9_<>]+)')
PRIMARY_KEY_PATTERN = re.compile(r'@PrimaryKey')

def extract_room_schema(tree_root):
    tables = []

    def walk(node):
        if not node.is_dir and node.path.endswith(".kt"):
            try:
                code = read_text_file(node.path)
            except:
                return

            if "@Entity" in code:
                # 1. Extract Table Name
                table_match = TABLE_NAME_PATTERN.search(code)
                class_match = CLASS_NAME_PATTERN.search(code)
                
                if not class_match:
                    return

                class_name = class_match.group(1)
                # Agar tableName explicit nahi hai, to class name use karo
                table_name = table_match.group(1) if table_match else class_name

                # 2. Extract Fields (Columns)
                fields = []
                lines = code.splitlines()
                
                for line in lines:
                    field_match = FIELD_PATTERN.search(line)
                    if field_match:
                        col_name = field_match.group(2)
                        col_type = field_match.group(3)
                        is_pk = "@PrimaryKey" in line
                        
                        fields.append({
                            "name": col_name,
                            "type": col_type,
                            "pk": is_pk
                        })

                tables.append({
                    "table": table_name,
                    "class": class_name,
                    "path": node.path,
                    "columns": fields
                })

        for child in node.children:
            walk(child)

    walk(tree_root)
    return format_schema_output(tables)

def format_schema_output(tables):
    if not tables:
        return "No Room @Entities found. Ensure you are using Room Database."

    lines = []
    lines.append("=" * 50)
    lines.append("ROOM DATABASE SCHEMA (AI OPTIMIZED)")
    lines.append("=" * 50)
    lines.append("")
    
    # 1. Concise Summary (For AI fast reading)
    lines.append("## SUMMARY TABLES")
    for t in tables:
        cols = [c['name'] for c in t['columns']]
        lines.append(f"- Table `{t['table']}` ({len(cols)} columns)")
    lines.append("")

    # 2. Detailed Schema
    lines.append("## DETAILED STRUCTURE")
    
    for t in tables:
        lines.append(f"TABLE: {t['table']}")
        lines.append(f"CLASS: {t['class']}")
        lines.append("-" * 30)
        
        for col in t['columns']:
            marker = "🔑 " if col['pk'] else "   "
            lines.append(f"{marker}{col['name']:<20} : {col['type']}")
        lines.append("")

    # 3. Mermaid Diagram Code (Bonus for Visualization)
    lines.append("## MERMAID CLASS DIAGRAM (Copy into Mermaid Live Editor)")
    lines.append("```mermaid")
    lines.append("classDiagram")
    for t in tables:
        lines.append(f"    class {t['table']} {{")
        for col in t['columns']:
            # Clean types for mermaid
            clean_type = col['type'].replace("<", "~").replace(">", "~")
            lines.append(f"        +{clean_type} {col['name']}")
        lines.append("    }")
    lines.append("```")
    
    return "\n".join(lines)