"""Template-based computation question generator service.

Generates unlimited computation questions by randomizing numbers
in predefined templates. Zero AI cost.
"""
import logging
import random

from app.templates import TEMPLATE_REGISTRY

logger = logging.getLogger(__name__)


class TemplateGenerator:
    """Generate computation question variants from registered templates."""

    def get_available_concepts(self) -> list[str]:
        """Return concept_ids that have templates registered."""
        return list(TEMPLATE_REGISTRY.keys())

    def has_templates(self, concept_id: str) -> bool:
        """Check if templates exist for a concept."""
        return concept_id in TEMPLATE_REGISTRY

    def generate(
        self,
        concept_id: str,
        difficulty: int | None = None,
        exclude_ids: set[str] | None = None,
        max_attempts: int = 50,
    ) -> dict | None:
        """Generate one random question variant.

        Args:
            concept_id: target concept
            difficulty: exact difficulty (None = random from available)
            exclude_ids: question IDs to avoid (deduplication)
            max_attempts: max retries to find unique question

        Returns:
            Question dict ready for DB insertion, or None if no template found.
        """
        templates = TEMPLATE_REGISTRY.get(concept_id)
        if not templates:
            return None

        # Filter by difficulty if specified
        if difficulty is not None:
            candidates = [(d, fn) for d, fn in templates if d == difficulty]
            if not candidates:
                # Fallback: closest difficulty
                candidates = sorted(templates, key=lambda t: abs(t[0] - difficulty))
        else:
            candidates = templates

        exclude = exclude_ids or set()

        for _ in range(max_attempts):
            diff, gen_fn = random.choice(candidates)
            question = gen_fn()
            if question["id"] not in exclude:
                return question

        # Last resort: return anyway (better than no question)
        _, gen_fn = random.choice(candidates)
        return gen_fn()

    def generate_batch(
        self,
        concept_id: str,
        count: int,
        difficulty: int | None = None,
        exclude_ids: set[str] | None = None,
    ) -> list[dict]:
        """Generate N unique question variants for a concept.

        Args:
            concept_id: target concept
            count: number of questions to generate
            difficulty: exact difficulty (None = mixed)
            exclude_ids: question IDs to avoid

        Returns:
            List of question dicts (may be fewer than count if templates limited).
        """
        if not self.has_templates(concept_id):
            return []

        exclude = set(exclude_ids) if exclude_ids else set()
        results = []

        for _ in range(count):
            q = self.generate(concept_id, difficulty, exclude)
            if q:
                results.append(q)
                exclude.add(q["id"])

        return results

    def generate_for_grade(
        self,
        grade: str,
        count: int,
        available_concept_ids: list[str] | None = None,
        exclude_ids: set[str] | None = None,
    ) -> list[dict]:
        """Generate questions across all concepts for a grade.

        Distributes evenly across available templated concepts.

        Args:
            grade: grade prefix (e.g., "elementary_3")
            count: total questions to generate
            available_concept_ids: limit to these concepts (student's unlocked)
            exclude_ids: question IDs to avoid

        Returns:
            List of question dicts.
        """
        # Map grade names to concept prefixes
        grade_prefix_map = {
            "elementary_3": "concept-e3-",
            "elementary_4": "concept-e4-",
            "elementary_5": "concept-e5-",
            "elementary_6": "concept-e6-",
            "middle_1": "concept-m1-",
            "middle_2": "concept-m2-",
            "middle_3": "concept-m3-",
            "high_1": "concept-h1-",
            "high_2": "concept-h2-",
        }

        prefix = grade_prefix_map.get(grade, "")
        if not prefix:
            return []

        # Get concepts with templates for this grade
        templated = [
            cid for cid in TEMPLATE_REGISTRY
            if cid.startswith(prefix)
        ]

        # Filter by available concepts if provided
        if available_concept_ids is not None:
            available_set = set(available_concept_ids)
            templated = [cid for cid in templated if cid in available_set]

        if not templated:
            return []

        exclude = set(exclude_ids) if exclude_ids else set()
        results = []

        # Round-robin across concepts
        per_concept = max(1, count // len(templated))
        remainder = count - per_concept * len(templated)

        random.shuffle(templated)
        for i, cid in enumerate(templated):
            n = per_concept + (1 if i < remainder else 0)
            batch = self.generate_batch(cid, n, exclude_ids=exclude)
            results.extend(batch)
            for q in batch:
                exclude.add(q["id"])

        # Trim to requested count
        if len(results) > count:
            results = random.sample(results, count)

        return results
