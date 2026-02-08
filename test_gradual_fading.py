
import asyncio
import os
import sys
from dotenv import load_dotenv

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

load_dotenv("backend/.env")

from app.services.ai_service import AIService
from app.services.prompt_context import PROMPT_CONTEXTS

async def main():
    service = AIService()
    concept_id = "concept-e3-add-sub-01"
    concept_name = "덧셈과 뺄셈"
    
    print(f"Generating Gradual Fading questions for {concept_id}...")
    
    try:
        questions = await service.generate_questions(
            concept_name=concept_name,
            concept_id=concept_id,
            grade="elementary_3",
            category="concept",
            part="calc",
            question_type="fill_in_blank",
            count=4,
            concept_method="gradual_fading"
        )
        
        if not questions:
            print("Failed to generate questions.")
            return

        print(f"Generated {len(questions)} questions.")
        for q in questions:
            print(f"[{q['id']}] Level {q.get('fading_level')} (Diff: {q['difficulty']})")
            print(f"Method: {q.get('concept_method')}")
            print(f"Content: {q['content']}")
            print(f"Answer: {q['correct_answer']}")
            print(f"Explanation: {q.get('explanation')}")
            print("-" * 50)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
