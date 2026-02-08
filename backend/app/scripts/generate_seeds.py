"""Gemini API를 활용한 시드 데이터 대량 생성 스크립트.

사용법:
    python -m app.scripts.generate_seeds \
        --guide data/초5_수학_개념문제_가이드.md \
        --grade elementary_5 \
        --output backend/app/seeds/elementary_5/

환경변수:
    GEMINI_API_KEY: Google AI Studio API 키
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

# 프로젝트 루트를 path에 추가
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from google import genai
from google.genai import types


SYSTEM_PROMPT = """당신은 2022 개정 교육과정 기반 초등/중등 수학 문제 출제 전문가입니다.

주어진 가이드 문서를 분석하여, 지정된 형식에 맞는 수학 시드 데이터(JSON)를 생성합니다.

## 출력 형식 규칙
1. 각 단원별로 정확히 지정된 수의 문제를 생성합니다.
2. 모든 수학 계산은 반드시 정확해야 합니다. 검산을 수행하세요.
3. 가이드의 핵심 개념, 주요 오개념, 출제 포인트를 반드시 문제에 반영합니다.
4. explanation에는 오개념 교정 내용을 포함합니다.
5. difficulty는 1~10 범위입니다.
6. part 값은 반드시 다음 중 하나: calc, algebra, func, geo, data, word
7. category 값은: computation 또는 concept
8. question_type은: multiple_choice 또는 fill_in_blank

## 객관식(MC) 형식
{
  "id": "e5-1-1-1-lv03-co-001",
  "concept_id": "concept-e5-xxx",
  "category": "computation",
  "part": "calc",
  "question_type": "multiple_choice",
  "difficulty": 3,
  "content": "문제 내용",
  "options": [
    {"label": "A", "text": "선지1"},
    {"label": "B", "text": "선지2"},
    {"label": "C", "text": "선지3"},
    {"label": "D", "text": "선지4"}
  ],
  "correct_answer": "B",
  "explanation": "해설 (오개념 교정 포함)",
  "points": 10
}

## 빈칸채우기(FB) 형식
{
  "id": "e5-1-1-1-lv03-fb-001",
  "concept_id": "concept-e5-xxx",
  "category": "computation",
  "part": "calc",
  "question_type": "fill_in_blank",
  "difficulty": 3,
  "content": "156 × 4 = ____",
  "correct_answer": "624",
  "explanation": "해설",
  "points": 10,
  "accept_formats": ["624"]
}
"""


def build_generation_prompt(guide_content: str, grade: str, grade_prefix: str) -> str:
    """가이드 문서와 학년 정보를 바탕으로 생성 프롬프트를 만듭니다."""
    return f"""다음은 {grade} 수학 개념 문제 개발 가이드입니다.

<guide>
{guide_content}
</guide>

위 가이드를 분석하여, 아래 작업을 수행하세요:

## 작업 1: 개념(Concept) 생성
가이드의 각 단원에 대해 1개씩 개념을 생성하세요.
- id: "concept-{grade_prefix}-단원약어" (예: concept-{grade_prefix}-add-sub)
- grade: "{grade}"
- 연산 단원은 category="computation", part="calc"
- 도형 단원은 category="concept", part="geo"
- 자료/그래프 단원은 category="concept", part="data"
- 규칙/비례 단원은 category="concept", part="algebra"

## 작업 2: 객관식 문제(MC) 생성
각 단원당 3개씩 객관식 문제를 생성하세요.
- 연산 단원: id는 "{grade_prefix}-{{학기}}-{{단원}}-{{개념번호}}-lv{{난이도:02d}}-co-{{순번:003d}}" 형식
- 개념 단원: id는 "{grade_prefix}-{{학기}}-{{단원}}-{{개념번호}}-lv{{난이도:02d}}-cc-{{순번:003d}}" 형식
- 난이도 분포: 각 단원마다 저(1-3), 중(4-6), 고(7-10) 각 1문항
- 선지 4개, 오개념을 반영한 오답 선지 포함

## 작업 3: 빈칸채우기 문제(FB) 생성
각 단원당 2개씩 빈칸채우기 문제를 생성하세요.
- id: "{grade_prefix}-{{학기}}-{{단원}}-{{개념번호}}-lv{{난이도:02d}}-fb-{{순번:003d}}" 형식
- 난이도 분포: 저(1-4) 1문항, 고(5-10) 1문항

## 출력 형식
반드시 아래 JSON 형식으로 출력하세요:
```json
{{
  "concepts": [...],
  "mc_computation": [...],
  "mc_concept": [...],
  "fill_blank": [...]
}}
```

주의: 수학 계산은 반드시 정확해야 합니다. 모든 정답을 검산하세요."""


def parse_json_from_response(text: str) -> dict:
    """Gemini 응답에서 JSON을 추출합니다."""
    # ```json ... ``` 블록 추출
    match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    if match:
        return json.loads(match.group(1))
    # 전체가 JSON인 경우
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # { } 블록 찾기
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            return json.loads(match.group(0))
    raise ValueError("응답에서 JSON을 추출할 수 없습니다.")


def convert_to_computation_py(concepts: list, questions: list, grade_prefix: str) -> str:
    """MC 연산 문제를 computation.py 파일로 변환합니다."""
    lines = [
        f'"""시드 데이터 - 연산 (Gemini 생성)."""',
        "from app.seeds._base import mc, concept",
        "",
        "",
        "def get_concepts():",
        '    """연산 관련 개념 반환."""',
        "    return [",
    ]
    for c in concepts:
        lines.append(f"        concept(")
        lines.append(f'            id="{c["id"]}",')
        lines.append(f'            name="{c["name"]}",')
        lines.append(f'            grade="{c["grade"]}",')
        lines.append(f'            category="{c["category"]}",')
        lines.append(f'            part="{c["part"]}",')
        lines.append(f'            description="{c["description"]}",')
        lines.append(f"        ),")
    lines.append("    ]")
    lines.append("")
    lines.append("")
    lines.append("def get_questions():")
    lines.append('    """연산 문제 반환."""')
    lines.append("    return [")
    for q in questions:
        lines.append("        mc(")
        lines.append(f'            id="{q["id"]}",')
        lines.append(f'            concept_id="{q["concept_id"]}",')
        lines.append(f'            category="{q["category"]}",')
        lines.append(f'            part="{q["part"]}",')
        lines.append(f"            difficulty={q['difficulty']},")
        content = q["content"].replace('"', '\\"')
        lines.append(f'            content="{content}",')
        lines.append("            options=[")
        for opt in q["options"]:
            text = opt["text"].replace('"', '\\"')
            lines.append(f'                ("{text}", "{text}"),')
        lines.append("            ],")
        lines.append(f'            correct="{q["correct_answer"]}",')
        explanation = q["explanation"].replace('"', '\\"')
        lines.append(f'            explanation="{explanation}",')
        lines.append(f"            points={q.get('points', 10)},")
        lines.append("        ),")
    lines.append("    ]")
    lines.append("")
    return "\n".join(lines)


def convert_to_concept_py(concepts: list, questions: list) -> str:
    """MC 개념 문제를 concept_questions.py 파일로 변환합니다."""
    lines = [
        f'"""시드 데이터 - 개념 (Gemini 생성)."""',
        "from app.seeds._base import mc, concept",
        "",
        "",
        "def get_concepts():",
        '    """개념 관련 개념 반환."""',
        "    return [",
    ]
    for c in concepts:
        lines.append(f"        concept(")
        lines.append(f'            id="{c["id"]}",')
        lines.append(f'            name="{c["name"]}",')
        lines.append(f'            grade="{c["grade"]}",')
        lines.append(f'            category="{c["category"]}",')
        lines.append(f'            part="{c["part"]}",')
        lines.append(f'            description="{c["description"]}",')
        lines.append(f"        ),")
    lines.append("    ]")
    lines.append("")
    lines.append("")
    lines.append("def get_questions():")
    lines.append('    """개념 문제 반환."""')
    lines.append("    return [")
    for q in questions:
        lines.append("        mc(")
        lines.append(f'            id="{q["id"]}",')
        lines.append(f'            concept_id="{q["concept_id"]}",')
        lines.append(f'            category="{q["category"]}",')
        lines.append(f'            part="{q["part"]}",')
        lines.append(f"            difficulty={q['difficulty']},")
        content = q["content"].replace('"', '\\"')
        lines.append(f'            content="{content}",')
        lines.append("            options=[")
        for opt in q["options"]:
            text = opt["text"].replace('"', '\\"')
            lines.append(f'                ("{text}", "{text}"),')
        lines.append("            ],")
        lines.append(f'            correct="{q["correct_answer"]}",')
        explanation = q["explanation"].replace('"', '\\"')
        lines.append(f'            explanation="{explanation}",')
        lines.append(f"            points={q.get('points', 10)},")
        lines.append("        ),")
    lines.append("    ]")
    lines.append("")
    return "\n".join(lines)


def convert_to_fill_blank_py(questions: list) -> str:
    """FB 문제를 fill_blank.py 파일로 변환합니다."""
    lines = [
        f'"""시드 데이터 - 빈칸 채우기 (Gemini 생성)."""',
        "from app.seeds._base import fb",
        "",
        "",
        "def get_questions():",
        '    """빈칸 채우기 문제 반환."""',
        "    return [",
    ]
    for q in questions:
        lines.append("        fb(")
        lines.append(f'            id="{q["id"]}",')
        lines.append(f'            concept_id="{q["concept_id"]}",')
        lines.append(f'            category="{q["category"]}",')
        lines.append(f'            part="{q["part"]}",')
        lines.append(f"            difficulty={q['difficulty']},")
        content = q["content"].replace('"', '\\"')
        lines.append(f'            content="{content}",')
        answer = q["correct_answer"].replace('"', '\\"')
        lines.append(f'            answer="{answer}",')
        explanation = q["explanation"].replace('"', '\\"')
        lines.append(f'            explanation="{explanation}",')
        lines.append(f"            points={q.get('points', 10)},")
        if q.get("accept_formats"):
            formats = ", ".join(f'"{f}"' for f in q["accept_formats"])
            lines.append(f"            accept_formats=[{formats}],")
        lines.append("        ),")
    lines.append("    ]")
    lines.append("")
    return "\n".join(lines)


async def generate_seeds(guide_path: str, grade: str, output_dir: str):
    """가이드 문서를 읽고 Gemini로 시드 데이터를 생성합니다."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY 환경변수를 설정하세요.")
        sys.exit(1)

    # 학년 접두사 결정
    grade_prefixes = {
        "elementary_3": "e3", "elementary_4": "e4", "elementary_5": "e5",
        "elementary_6": "e6", "middle_1": "m1", "middle_2": "m2",
        "middle_3": "m3", "high_1": "h1",
    }
    grade_prefix = grade_prefixes.get(grade)
    if not grade_prefix:
        print(f"ERROR: 지원하지 않는 학년: {grade}")
        sys.exit(1)

    # 가이드 읽기
    guide_content = Path(guide_path).read_text(encoding="utf-8")
    print(f"✓ 가이드 읽기 완료: {guide_path} ({len(guide_content)} chars)")

    # Gemini 클라이언트 생성
    client = genai.Client(api_key=api_key)

    # 프롬프트 생성
    prompt = build_generation_prompt(guide_content, grade, grade_prefix)
    print(f"✓ 프롬프트 생성 완료 ({len(prompt)} chars)")
    print("⏳ Gemini API 호출 중...")

    # Gemini 호출
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.3,
            max_output_tokens=16384,
        ),
    )

    # JSON 파싱
    result = parse_json_from_response(response.text)
    print(f"✓ JSON 파싱 완료")

    concepts = result.get("concepts", [])
    mc_comp = result.get("mc_computation", [])
    mc_conc = result.get("mc_concept", [])
    fb = result.get("fill_blank", [])

    comp_concepts = [c for c in concepts if c.get("category") == "computation"]
    conc_concepts = [c for c in concepts if c.get("category") == "concept"]

    print(f"  개념: {len(concepts)}개 (연산 {len(comp_concepts)}, 개념 {len(conc_concepts)})")
    print(f"  MC 연산: {len(mc_comp)}개")
    print(f"  MC 개념: {len(mc_conc)}개")
    print(f"  빈칸채우기: {len(fb)}개")

    # 출력 디렉토리 생성
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    # 파일 생성
    (out / "computation.py").write_text(
        convert_to_computation_py(comp_concepts, mc_comp, grade_prefix),
        encoding="utf-8",
    )
    (out / "concept_questions.py").write_text(
        convert_to_concept_py(conc_concepts, mc_conc),
        encoding="utf-8",
    )
    (out / "fill_blank.py").write_text(
        convert_to_fill_blank_py(fb),
        encoding="utf-8",
    )

    print(f"\n✅ 생성 완료! 파일 위치: {output_dir}")
    print(f"   - computation.py ({len(mc_comp)} MC)")
    print(f"   - concept_questions.py ({len(mc_conc)} MC)")
    print(f"   - fill_blank.py ({len(fb)} FB)")
    print(f"\n⚠️  __init__.py는 수동으로 작성하거나 기존 파일을 업데이트하세요.")
    print(f"⚠️  생성된 문제의 수학 정답을 반드시 검증하세요.")

    # JSON 원본도 저장 (디버깅/검증용)
    json_path = out / "_generated_raw.json"
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"   - _generated_raw.json (원본 JSON)")


def main():
    parser = argparse.ArgumentParser(description="Gemini로 수학 시드 데이터 생성")
    parser.add_argument("--guide", required=True, help="가이드 .md 파일 경로")
    parser.add_argument("--grade", required=True, help="학년 (예: elementary_5)")
    parser.add_argument("--output", required=True, help="출력 디렉토리")
    args = parser.parse_args()

    import asyncio
    asyncio.run(generate_seeds(args.guide, args.grade, args.output))


if __name__ == "__main__":
    main()
