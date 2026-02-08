import re

def parse_detailed_coverage(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    inventory = []
    current_grade = ""
    current_unit = ""
    current_concept = None
    
    # regex for grade/unit
    grade_re = re.compile(r'^## (.*)')
    unit_re = re.compile(r'^### 단원: (.*)')
    
    temp_data = None

    for line in lines:
        line = line.strip()
        if not line: continue
        
        # Grade detection
        gm = grade_re.match(line)
        if gm:
            current_grade = gm.group(1).strip()
            continue
            
        # Unit detection
        um = unit_re.match(line)
        if um:
            current_unit = um.group(1).strip()
            continue
            
        if line.startswith('|') and '---' not in line and '유형' not in line:
            parts = [p.strip() for p in line.split('|')]
            # | 개념 | 유형 | lv1 | lv2 | lv3 | lv4 | lv5| lv6 | lv7 | lv8 | lv9 | lv10 | 합계 | 템플릿 |
            # parts will be ['', '개념', '유형', 'v1', ..., 'v10', '합계', '템플릿', ''] (index 0 and last are empty)
            
            if len(parts) < 14: continue
            
            concept_col = parts[1]
            type_plus_warning = parts[2] # "⚠FB없음 CO" or just "CO"
            # Extract type (CO, CC, FB, or "합")
            type_match = re.search(r'(CO|CC|FB|합)', type_plus_warning)
            if not type_match: continue
            q_type = type_match.group(1)
            
            counts = parts[3:13] # lv1 to lv10
            numeric_counts = []
            for c in counts:
                # remove bold or warning markers
                clean_c = re.sub(r'[\*\*\⚠]', '', c).strip()
                if clean_c == '-':
                    numeric_counts.append(0)
                elif clean_c.isdigit():
                    numeric_counts.append(int(clean_c))
                else:
                    numeric_counts.append(0)

            if concept_col and concept_col != '개념':
                # New concept start
                if temp_data: inventory.append(temp_data)
                
                clean_concept = re.sub(r'[\*\*\⚠]', '', concept_col).strip()
                temp_data = {
                    "Grade": current_grade,
                    "Unit": current_unit,
                    "Concept": clean_concept,
                    "CC": [0]*10,
                    "FB": [0]*10,
                    "CO": [0]*10
                }
            
            if temp_data and q_type in ["CC", "FB", "CO"]:
                temp_data[q_type] = numeric_counts
            
            # Note: "합" row is ignored as it's redundant but marks transition
            if q_type == "합":
                # Concept block finished
                pass

    if temp_data: inventory.append(temp_data)
    return inventory

def export_to_md(inventory, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# 수학 문항 세부 인벤토리 보고서 (난이도별 x 유형별)\n\n")
        f.write("> **구성**: 학년 > 단원 > 개념 > [난이도별 유형별 문항수]\n")
        f.write("> **기수**: CC (개념 완성), FB (빈칸 채우기), CO (연산)\n\n")
        
        current_grade = ""
        current_unit = ""
        
        for item in inventory:
            if item["Grade"] != current_grade:
                current_grade = item["Grade"]
                f.write(f"\n## {current_grade}\n\n")
                current_unit = ""
            
            if item["Unit"] != current_unit:
                current_unit = item["Unit"]
                f.write(f"### 단원: {current_unit}\n\n")
            
            f.write(f"#### {item['Concept']}\n")
            f.write("| 유형 | lv1 | lv2 | lv3 | lv4 | lv5 | lv6 | lv7 | lv8 | lv9 | lv10 | 합계 |\n")
            f.write("|---|---|---|---|---|---|---|---|---|---|---|---|\n")
            
            for t in ["CC", "FB", "CO"]:
                vals = item[t]
                total = sum(vals)
                row = f"| {t} | " + " | ".join(str(v) if v > 0 else "-" for v in vals) + f" | {total} |\n"
                f.write(row)
            
            # 합계
            totals = [item["CC"][i] + item["FB"][i] + item["CO"][i] for i in range(10)]
            row_total = f"| **합** | " + " | ".join(f"**{v}**" if v > 0 else "-" for v in totals) + f" | **{sum(totals)}** |\n\n"
            f.write(row_total)

if __name__ == "__main__":
    data = parse_detailed_coverage('f:/math_test/coverage_report.md')
    export_to_md(data, 'f:/math_test/docs/work-plans/ultra-detailed-inventory.md')
    print(f"Parsed {len(data)} concepts.")
