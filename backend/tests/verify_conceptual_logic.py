
import random
from collections import Counter

# Mocking ConceptMethod Enum values as strings
class ConceptMethod:
    STANDARD = "standard"
    GRADUAL_FADING = "gradual_fading"
    ERROR_ANALYSIS = "error_analysis"
    VISUAL_DECODING = "visual_decoding"

def pick_random_concept_method(grade: str) -> str:
    r = random.random()
    if grade in ["elementary_1", "elementary_2"]:
        if r < 0.4: return ConceptMethod.STANDARD
        if r < 0.5: return ConceptMethod.GRADUAL_FADING
        if r < 0.7: return ConceptMethod.ERROR_ANALYSIS
        return ConceptMethod.VISUAL_DECODING
    elif grade in ["elementary_3", "elementary_4"]:
        if r < 0.4: return ConceptMethod.STANDARD
        if r < 0.5: return ConceptMethod.GRADUAL_FADING
        if r < 0.8: return ConceptMethod.ERROR_ANALYSIS
        return ConceptMethod.VISUAL_DECODING
    else:
        if r < 0.4: return ConceptMethod.STANDARD
        if r < 0.7: return ConceptMethod.GRADUAL_FADING
        if r < 0.85: return ConceptMethod.ERROR_ANALYSIS
        return ConceptMethod.VISUAL_DECODING

def run_simulation(grade, iterations=1000):
    results = [pick_random_concept_method(grade) for _ in range(iterations)]
    counts = Counter(results)
    percentages = {k: v / iterations * 100 for k, v in counts.items()}
    return percentages

print("Phase 6 Differential Ratio Simulation Results (1,000 iterations per group):")
print("-" * 60)
for g_group in ["elementary_1", "elementary_3", "elementary_5"]:
    label = {
        "elementary_1": "1-2G (Type C Focus)",
        "elementary_3": "3-4G (Type B Focus)",
        "elementary_5": "5-6G+ (Type A Focus)"
    }[g_group]
    res = run_simulation(g_group)
    print(f"[{label}]")
    for method in [ConceptMethod.STANDARD, ConceptMethod.GRADUAL_FADING, ConceptMethod.ERROR_ANALYSIS, ConceptMethod.VISUAL_DECODING]:
        print(f"  - {method}: {res.get(method, 0):.1f}%")
    print()

print("Phase 3 Difficulty Mapping Verification:")
mapping = {1: 2, 2: 4, 3: 6, 4: 8}
for level, diff in mapping.items():
    print(f"  - Level {level} (L{level}) -> Difficulty {diff}")
