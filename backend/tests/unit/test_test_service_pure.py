"""shuffle_question_options 순수 함수 테스트."""

from app.services.test_service import shuffle_question_options


def _make_options(labels=("A", "B", "C", "D")):
    return [{"id": str(i + 1), "label": l, "text": f"option_{l}"} for i, l in enumerate(labels)]


class TestShuffleQuestionOptions:
    def test_empty_options(self):
        result, new_correct = shuffle_question_options([], "A")
        assert result == []
        assert new_correct == "A"

    def test_single_option(self):
        opts = [{"id": "1", "label": "A", "text": "only"}]
        result, new_correct = shuffle_question_options(opts, "A")
        assert len(result) == 1
        assert new_correct == "A"
        assert result[0]["label"] == "A"

    def test_correct_answer_tracked(self):
        opts = _make_options()
        result, new_correct = shuffle_question_options(opts, "B")
        # 정답 option id "2"가 새 라벨에 매핑되어야 함
        correct_opt = next(o for o in result if o["id"] == "2")
        assert new_correct == correct_opt["label"]

    def test_labels_reassigned_abcd(self):
        opts = _make_options()
        result, _ = shuffle_question_options(opts, "A")
        labels = [o["label"] for o in result]
        assert labels == ["A", "B", "C", "D"]

    def test_original_not_mutated(self):
        opts = _make_options()
        original_labels = [o["label"] for o in opts]
        shuffle_question_options(opts, "A")
        assert [o["label"] for o in opts] == original_labels

    def test_four_options_all_present(self):
        opts = _make_options()
        original_ids = {o["id"] for o in opts}
        result, _ = shuffle_question_options(opts, "A")
        result_ids = {o["id"] for o in result}
        assert result_ids == original_ids

    def test_six_options(self):
        opts = _make_options(("A", "B", "C", "D", "E", "F"))
        result, new_correct = shuffle_question_options(opts, "D")
        assert len(result) == 6
        labels = [o["label"] for o in result]
        assert labels == ["A", "B", "C", "D", "E", "F"]
        correct_opt = next(o for o in result if o["id"] == "4")
        assert new_correct == correct_opt["label"]

    def test_no_id_field_graceful(self):
        opts = [{"label": "A", "text": "x"}, {"label": "B", "text": "y"}]
        result, new_correct = shuffle_question_options(opts, "A")
        assert len(result) == 2
        # id가 없으면 correct_option_id=None, new_correct은 원래 값 유지 가능
        assert new_correct in ("A", "B")
