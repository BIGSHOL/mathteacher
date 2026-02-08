
import asyncio
import os
import sys
from dotenv import load_dotenv

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

load_dotenv("backend/.env")

from app.services.ai_service import AIService

async def main():
    service = AIService()
    # 덧셈과 뺄셈 (받아내림)
    concept_id = "concept-e3-add-sub-02"
    concept_name = "뺄셈 (받아내림)"
    
    print(f"Generating Visual Decoding questions for {concept_id}...")
    
    try:
        questions = await service.generate_questions(
            concept_name=concept_name,
            concept_id=concept_id,
            grade="elementary_3",
            category="concept",
            part="calc",
            question_type="multiple_choice",
            count=2,
            concept_method="visual_decoding"
        )
        
        if not questions:
            print("Failed to generate questions.")
            return

        print(f"Generated {len(questions)} questions.")
        for q in questions:
            print(f"[{q['id']}] (Diff: {q['difficulty']})")
            print(f"Method: {q.get('concept_method')}")
            print(f"Content: {q['content']}")
            if q.get('options'):
                print("Options:")
                for opt in q['options']:
                    print(f"  {opt['label']}: {opt['text']}")
            print(f"Answer: {q['correct_answer']}")
            print(f"Explanation: {q.get('explanation')}")
            print("-" * 50)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
