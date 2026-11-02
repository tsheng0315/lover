"""LOVER's fixed single-card configuration and generation regressions."""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import generate
import settings_config
import styles


class CandidateCountConfigTests(unittest.TestCase):
    def test_settings_persist_the_only_supported_candidate_count(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "env"
            updated = settings_config.write_settings(
                path, "", {"JEV_CANDIDATES_PER_TONE": "1"})
            self.assertIn("export JEV_CANDIDATES_PER_TONE=1", updated)

    def test_settings_reject_any_count_other_than_one(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "env"
            for value in ("0", "2", "6", "not-a-number"):
                with self.subTest(value=value), self.assertRaises(ValueError):
                    settings_config.write_settings(
                        path, "", {"JEV_CANDIDATES_PER_TONE": value})
            self.assertFalse(path.exists())


class CandidateCountGenerationTests(unittest.TestCase):
    def test_relationship_card_uses_structured_reflection_prompt(self):
        generator = generate.Generator()
        response = '{"user_emotion":"有点在意", "surface_message":"对方在说明情况", "language_cues":["没听到"]}'
        with patch.object(generator, "_call", return_value=response) as call:
            texts, error = generator._one_tone("当前消息", "日常互动", "关系理解")

        self.assertEqual(error, "")
        self.assertEqual(len(texts), 1)
        self.assertIn("先给你的感受一点空间\n有点在意", texts[0])
        self.assertIn("我注意到的语言线索\n• 没听到", texts[0])
        prompt = call.call_args.args[0]
        self.assertIn("Return one JSON object", prompt)
        self.assertIn("Write every value in Simplified Chinese", prompt)


if __name__ == "__main__":
    unittest.main()
