import re
import csv

def parse_coverage_report(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by grade
    grades = re.split(r'## (초등|중등|고등) (\d학년)', content)[1:]
    
    results = []
    
    # Unit level mapping (approximate for semesters)
    # This is a simplified heuristic or manual mapping if units are known.
    # We will just list units as they appear.

    current_grade = ""
    for i in range(0, len(grades), 3):
        prefix = grades[i]
        level = grades[i+1]
        current_grade = f"{prefix} {level}"
        grade_body = grades[i+2]
        
        # Split by unit
        units = re.split(r'### 단원: (.*)', grade_body)[1:]
        
        for j in range(0, len(units), 2):
            unit_name = units[j].strip()
            unit_body = units[j+1]
            
            # Find concepts in this unit
            concepts = re.findall(r'\| \*\*(.*?)\*\* \| (CO|CC|FB) \| (.*?) \|', unit_body)
            # Find total summary row for the concept
            # | ... | **합** | lv1 | lv2 ... | 합계 |
            
            # The structure is often:
            # | Concept | Type | lv1 | ... | Total |
            # |         | Type | ... |
            # | Summary | **합** | ... |
            
            # Let's extract concept blocks
            concept_blocks = re.split(r'\| \*\*(.*?)\*\* \| CO \|', unit_body)[1:]
            for k in range(0, len(concept_blocks), 2):
                concept_name = concept_blocks[k].strip()
                block_content = concept_blocks[k+1]
                
                # Extract CO, CC, FB rows
                co_match = re.search(r'- \| (.*?) \| \*\*(\d+)\*\*', "- | " + block_content) # Prefix with CO
                # Wait, regex for the table row
                rows = block_content.split('\n')
                
                # I'll use a simpler approach: finding the "합" line in the block
                # | ⚠... | **합** | lv1 | ... | lv10 | 합계 |
                summary_match = re.search(r'\|.*?\*\*합\*\* \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| \*\*(\d+)\*\*', block_content)
                
                cc_row = re.search(r'CC \| (.*?) \| \*\*(\d+)\*\*', block_content)
                fb_row = re.search(r'FB \| (.*?) \| \*\*(\d+)\*\*', block_content)
                co_row = re.search(r'CO \| (.*?) \| \*\*(\d+)\*\*', "CO | " + block_content)

                if summary_match:
                    lv_counts = [summary_match.group(m) for m in range(1, 11)]
                    total = int(summary_match.group(11))
                    
                    cc_count = int(cc_row.group(2)) if cc_row else 0
                    fb_count = int(fb_row.group(2)) if fb_row else 0
                    co_count = total - cc_count - fb_count
                    
                    results.append({
                        "Grade": current_grade,
                        "Unit": unit_name,
                        "Concept": concept_name,
                        "Total": total,
                        "CC": cc_count,
                        "FB": fb_count,
                        "CO": co_count,
                        "lv1-2": sum(1 for x in lv_counts[:2] if x.strip() != '-'), # This counts kinds, not items
                        # Wait, the table contains items if it's a number, or '-' if 0.
                        # The summary row in coverage_report.md actually has counts.
                        "lv1": summary_match.group(1),
                        "lv2": summary_match.group(2),
                        "lv3": summary_match.group(3),
                        "lv4": summary_match.group(4),
                        "lv5": summary_match.group(5),
                        "lv6": summary_match.group(6),
                        "lv7": summary_match.group(7),
                        "lv8": summary_match.group(8),
                        "lv9": summary_match.group(9),
                        "lv10": summary_match.group(10),
                    })
    
    return results

data = parse_coverage_report('f:/math_test/coverage_report.md')
with open('f:/math_test/docs/work-plans/full_inventory.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

print(f"Parsed {len(data)} concepts.")
