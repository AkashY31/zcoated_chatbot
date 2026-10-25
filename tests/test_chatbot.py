import unittest

import app


class IntentRoutingTests(unittest.TestCase):
    def test_routes_common_intents(self):
        cases = {
            "How much is deep cleaning?": "pricing",
            "Can you pick up from my home?": "booking_pickup_delivery",
            "Where are you located?": "location_contact_hours",
            "What services do you offer?": "service_information",
            "What is my order status?": "order_status",
            "My shoes came back damaged": "complaint_special_request",
            "I want to speak to a person": "human_handoff",
            "Do you repair leather bags?": "service_information",
            "Thanks, that's all": "conversation_end",
            "goodbye": "conversation_end",
            "Thanks, how much is shoe cleaning?": "pricing",
        }
        for message, expected in cases.items():
            with self.subTest(message=message):
                self.assertEqual(app.classify(message), expected)

    def test_deep_clean_price_comes_from_intent_markdown(self):
        reply = app.build_reply("How much is deep cleaning?")
        self.assertEqual(reply["intent"], "pricing")
        self.assertIn("Deep Cleaning is listed at ₹499", reply["answer"])

    def test_unlisted_bag_price_hands_off_without_guessing(self):
        reply = app.build_reply("How much does bag cleaning cost?")
        self.assertIn("don't have a published price", reply["answer"])
        self.assertIn("+91 83683 85923", reply["answer"])

    def test_order_status_does_not_claim_live_tracking(self):
        reply = app.build_reply("What is my order status?")
        self.assertIn("can't see live order progress", reply["answer"])

    def test_conversation_end_asks_for_feedback(self):
        reply = app.build_reply("That's all, thank you")
        self.assertEqual(reply["intent"], "conversation_end")
        self.assertIn("how was your experience", reply["answer"])


if __name__ == "__main__":
    unittest.main()
