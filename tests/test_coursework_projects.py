"""Focused, offline tests for the small-business project helper logic."""

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))

import project_m1_front_desk as front_desk
import project_m2_business_assistant as business_assistant
import project_m2_content_studio as content_studio


class FrontDeskTests(unittest.TestCase):
    def test_known_question_uses_verified_fact(self) -> None:
        self.assertEqual(
            front_desk.answer_from_facts("What time do you open?"),
            "We are open 9 am to 10 pm every day.",
        )

    def test_unknown_question_is_left_for_ai(self) -> None:
        self.assertIsNone(front_desk.answer_from_facts("Do you have vegan cake?"))


class ContentStudioTests(unittest.TestCase):
    def test_prompt_includes_brief_and_no_invention_rule(self) -> None:
        prompt = content_studio.build_prompt(
            "Sweet Crumbs", "bakery", "Lahore", "families", "cupcakes for 250 PKR"
        )
        self.assertIn("cupcakes for 250 PKR", prompt)
        self.assertIn("families", prompt)
        self.assertIn("Do not invent prices", prompt)

    def test_review_flags_overlong_copy_and_unverified_numbers(self) -> None:
        drafts = {
            "instagram_caption": "Sale ends in 2030",
            "whatsapp_promotion": "Try our cupcake for 250 PKR",
            "promotional_idea": "Family bakery promotion",
        }
        findings = content_studio.review_drafts(
            drafts, "Cupcake price is 250 PKR"
        )
        self.assertTrue(any("2030" in finding for finding in findings))
        self.assertTrue(any("unsupported claim: sale" in finding for finding in findings))


class BusinessAssistantTests(unittest.TestCase):
    def test_price_tool_uses_business_data(self) -> None:
        result = business_assistant.get_price.invoke({"item": "cupcake"})
        self.assertIn("250 PKR", result)

    def test_order_requires_approval_and_persists(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            order_path = Path(folder) / "orders.jsonl"
            with (
                patch.object(business_assistant, "ORDER_FILE", order_path),
                patch("builtins.input", return_value="yes"),
            ):
                result = business_assistant.place_order.invoke(
                    {"item": "cupcake", "quantity": 2, "customer": "Test Customer"}
                )
            saved = json.loads(order_path.read_text(encoding="utf-8").strip())
        self.assertIn("placed", result)
        self.assertEqual(saved["total"], 500)
        self.assertEqual(saved["customer"], "Test Customer")

    def test_order_declined_is_not_saved(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            order_path = Path(folder) / "orders.jsonl"
            with (
                patch.object(business_assistant, "ORDER_FILE", order_path),
                patch("builtins.input", return_value="no"),
            ):
                result = business_assistant.place_order.invoke(
                    {"item": "cupcake", "quantity": 1, "customer": "Test Customer"}
                )
            self.assertIn("not placed", result)
            self.assertFalse(order_path.exists())


if __name__ == "__main__":
    unittest.main()
