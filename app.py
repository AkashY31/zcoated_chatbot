from __future__ import annotations

import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent
INTENTS = ROOT / "intents"
MAX_BODY_BYTES = 8_000
MAX_MESSAGE_CHARS = 500

INTENT_FILES = {
    "conversation_end": "feedback.md",
    "service_information": "services.md",
    "pricing": "pricing.md",
    "booking_pickup_delivery": "booking-pickup-delivery.md",
    "location_contact_hours": "location-contact.md",
    "order_status": "order-status.md",
    "complaint_special_request": "complaints-special-requests.md",
    "human_handoff": "human-handoff.md",
    "fallback": "fallback.md",
}

STATIC_FILES = {
    "/": ("web/index.html", "text/html; charset=utf-8"),
    "/styles.css": ("web/styles.css", "text/css; charset=utf-8"),
    "/app.js": ("web/app.js", "text/javascript; charset=utf-8"),
}


def normalize(text: str) -> str:
    expanded = re.sub(r"\bthat['’]s\b", "that is", text.lower())
    return re.sub(r"[^a-z0-9₹]+", " ", expanded).strip()


def contains_any(text: str, phrases: tuple[str, ...]) -> bool:
    normalized = f" {normalize(text)} "
    return any(f" {normalize(phrase)} " in normalized for phrase in phrases)


def classify(message: str) -> str:
    text = normalize(message)

    if text in {
        "bye",
        "goodbye",
        "see you",
        "thank you",
        "thanks",
        "that is all",
        "that is everything",
        "no more questions",
        "nothing else",
    }:
        return "conversation_end"

    if contains_any(
        text,
        (
            "that is all thanks",
            "that is all thank you",
            "that is everything thanks",
            "that is everything thank you",
            "thanks that is all",
            "thank you that is all",
            "thanks that is everything",
            "thank you that is everything",
        ),
    ):
        return "conversation_end"

    if contains_any(
        text,
        ("human", "real person", "speak to someone", "speak to a person", "talk to someone", "talk to a person", "customer support", "agent"),
    ):
        return "human_handoff"

    if contains_any(
        text,
        ("damaged", "damage", "refund", "complaint", "not happy", "not satisfied", "stain is still", "came back"),
    ):
        return "complaint_special_request"

    if contains_any(
        text,
        ("order status", "track order", "track my", "where is my order", "when will i get", "when will my", "order ready", "delivery status", "my order", "my shoes back"),
    ):
        return "order_status"

    if contains_any(text, ("pickup", "pick up", "collect", "book", "booking", "schedule", "delivery", "deliver", "tomorrow")):
        return "booking_pickup_delivery"

    if contains_any(
        text,
        ("price", "pricing", "cost", "how much", "₹", "rupee", "discount", "tax", "upi", "payment", "pay"),
    ):
        return "pricing"

    if contains_any(
        text,
        ("where", "address", "location", "phone", "number", "whatsapp", "email", "hours", "open", "close", "serving gurgaon"),
    ):
        return "location_contact_hours"

    if contains_any(
        text,
        ("clean", "cleaning", "wash", "repair", "sole", "heel", "stitch", "restore", "restoration", "sneaker", "shoe", "shoes", "bag", "suede", "leather", "service", "services"),
    ):
        return "service_information"

    return "fallback"


def read_intent(intent: str) -> str:
    filename = INTENT_FILES[intent]
    return (INTENTS / filename).read_text(encoding="utf-8")


def markdown_section(document: str, heading: str) -> str:
    target = heading.strip().lower()
    current_heading = ""
    lines: list[str] = []
    collecting = False

    for line in document.splitlines():
        if line.startswith("#"):
            current_heading = line.lstrip("#").strip().lower()
            if collecting:
                break
            collecting = current_heading == target
            continue
        if collecting:
            lines.append(line)

    return "\n".join(lines).strip()


def handoff_details() -> str:
    document = read_intent("human_handoff")
    section = markdown_section(document, "Official contact channels")
    details = [
        line.removeprefix("- ").strip()
        for line in section.splitlines()
        if line.startswith("- ")
    ]
    if details:
        return "\n".join(details)
    return "WhatsApp or call +91 83683 85923, or email support.zcoated@gmail.com."


PRICE_ALIASES = (
    ("premium sneaker spa", "Premium Sneaker Spa"),
    ("sneaker spa", "Premium Sneaker Spa"),
    ("deep cleaning", "Deep Cleaning"),
    ("deep clean", "Deep Clean"),
    ("basic cleaning", "Basic Cleaning"),
    ("basic clean", "Basic Clean"),
    ("minor repair", "Minor Repair"),
    ("heel repair", "Heel Repair"),
    ("sole repair", "Sole Repair"),
    ("full restoration", "Full Restoration"),
    ("full restore", "Full Restore"),
    ("2 shoes basic", "2 Shoes Basic"),
    ("two shoes basic", "2 Shoes Basic"),
    ("2 pairs basic", "2 Shoes Basic"),
    ("2 shoes deep", "2 Shoes Deep"),
    ("two shoes deep", "2 Shoes Deep"),
    ("2 pairs deep", "2 Shoes Deep"),
    ("3 shoes basic", "3 Shoes Basic"),
    ("three shoes basic", "3 Shoes Basic"),
    ("3 shoes deep", "3 Shoes Deep"),
    ("three shoes deep", "3 Shoes Deep"),
    ("basic clean minor repair", "Basic Clean + Minor Repair"),
    ("deep clean repair", "Deep Clean + Repair"),
    ("premium full restore", "Premium + Full Restore"),
)


def pricing_rows(document: str) -> list[tuple[str, str, str]]:
    category = ""
    rows: list[tuple[str, str, str]] = []
    for line in document.splitlines():
        if line.startswith("### "):
            category = line[4:].strip()
            continue
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 2 or cells[0].lower() == "service" or set(cells[0]) <= {"-", ":"}:
            continue
        rows.append((category, cells[0], cells[1]))
    return rows


def pricing_answer(message: str, document: str) -> str:
    query = normalize(message)
    rows = pricing_rows(document)

    if contains_any(message, ("discount", "tax", "upi", "payment method", "price match")):
        return (
            "The published pricing information does not specify discounts, taxes, or payment methods. "
            f"Please confirm with the Zcoated team:\n{handoff_details()}"
        )

    for alias, service_name in sorted(PRICE_ALIASES, key=lambda item: len(item[0]), reverse=True):
        if f" {normalize(alias)} " not in f" {query} ":
            continue
        for category, name, amount in rows:
            if normalize(name) == normalize(service_name):
                repair_note = (
                    " The final repair scope may need confirmation after the team assesses the item."
                    if "repair" in category.lower() or "repair" in name.lower()
                    else ""
                )
                return f"{name} is listed at {amount}.{repair_note}"

    if contains_any(message, ("bag", "backpack", "handbag")):
        return (
            "I don't have a published price for bag cleaning or repair. The Zcoated team can assess the item and confirm:\n"
            f"{handoff_details()}"
        )

    if contains_any(message, ("repair", "sole", "heel", "stitch")) and not contains_any(message, ("clean", "cleaning")):
        categories = {"Shoe Repair"}
    elif contains_any(message, ("combo", "pairs", "pair", "shoes")):
        categories = {"Cleaning + Repair Combo", "Multi Shoes Combo"}
    elif contains_any(message, ("clean", "cleaning", "wash", "sneaker")):
        categories = {"Shoe Cleaning"}
    else:
        categories = {category for category, _, _ in rows}

    selected = [(name, amount) for category, name, amount in rows if category in categories]
    if not selected:
        return f"I don't have a confirmed price for that service. Please check with the Zcoated team:\n{handoff_details()}"

    price_list = "\n".join(f"- {name}: {amount}" for name, amount in selected)
    return f"Here are Zcoated's published prices:\n{price_list}\n\nFor an unlisted service or repair assessment, please confirm with the team."


def contact_answer(message: str, document: str) -> str:
    section = markdown_section(document, "Confirmed information")
    facts = [
        line.removeprefix("- ").strip()
        for line in section.splitlines()
        if line.startswith("- ")
    ]
    query = normalize(message)
    if "phone" in query or "number" in query or "whatsapp" in query or "call" in query:
        wanted = ("phone",)
    elif "email" in query:
        wanted = ("email",)
    elif "hour" in query or "open" in query or "close" in query or "time" in query:
        wanted = ("hours",)
    elif "where" in query or "address" in query or "location" in query:
        wanted = ("location",)
    else:
        wanted = ()

    chosen = [fact for fact in facts if not wanted or any(word in fact.lower() for word in wanted)]
    if not chosen:
        chosen = facts
    answer = "\n".join(chosen)
    if wanted == ("hours",):
        answer += "\nPlease call ahead to confirm before visiting."
    return answer or handoff_details()


def services_answer(message: str, document: str) -> str:
    section = markdown_section(document, "Confirmed service information")
    lines = [line.removeprefix("- ").strip() for line in section.splitlines() if line.startswith("- ")]
    query = normalize(message)
    if "bag" in query or "backpack" in query or "handbag" in query:
        terms = ("bag cleaning",)
    elif "repair" in query or "sole" in query or "heel" in query or "stitch" in query:
        terms = ("shoe repair",)
    elif "restore" in query or "restoration" in query or "repaint" in query or "yellow" in query:
        terms = ("sneaker restoration",)
    elif "clean" in query or "wash" in query or "stain" in query or "odor" in query:
        terms = ("shoe cleaning",)
    else:
        terms = ()

    chosen = [line for line in lines if not terms or any(term in line.lower() for term in terms)]
    details = "\n".join(f"- {line}" for line in chosen)
    return (
        f"Zcoated's listed services include:\n{details}\n\n"
        "Suitability depends on the item's material and condition. The team may need to assess it before confirming the result."
    )


def build_reply(message: str) -> dict[str, str]:
    intent = classify(message)
    document = read_intent(intent)

    if intent == "pricing":
        answer = pricing_answer(message, document)
    elif intent == "conversation_end":
        answer = "Thanks for chatting with Zcoated! Before you go, how was your experience? Your rating helps us improve."
    elif intent == "location_contact_hours":
        answer = contact_answer(message, document)
    elif intent == "service_information":
        answer = services_answer(message, document)
    elif intent == "booking_pickup_delivery":
        answer = (
            "Zcoated advertises free doorstep pickup and delivery in Gurgaon. "
            "Share your locality and the service you need with the team so they can confirm coverage and arrange pickup. "
            "This chat does not create a booking.\n"
            f"{handoff_details()}"
        )
    elif intent == "order_status":
        answer = (
            "I can't see live order progress here, and Zcoated does not publish a standard turnaround time. "
            "Please contact the team with your order/reference number, if available:\n"
            f"{handoff_details()}"
        )
    elif intent == "complaint_special_request":
        answer = (
            "I'm sorry this didn't go as expected. I can't confirm a refund, guarantee, or repair outcome here, "
            "but the Zcoated team can review it. Please share a brief description and your order/reference number, if available:\n"
            f"{handoff_details()}"
        )
    elif intent == "human_handoff":
        answer = f"The Zcoated team can help with that. You can contact them here:\n{handoff_details()}"
    else:
        answer = (
            "I can help with Zcoated services, prices, pickup information, or contacting the team. "
            "What would you like to know?\n"
            f"{handoff_details()}"
        )

    return {"intent": intent, "answer": answer}


class ChatbotHandler(BaseHTTPRequestHandler):
    def send_bytes(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_bytes(status, body, "application/json; charset=utf-8")

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/health":
            self.send_json(200, {"ok": True})
            return

        static_file = STATIC_FILES.get(path)
        if static_file is None:
            self.send_json(404, {"error": "Not found"})
            return

        relative_path, content_type = static_file
        try:
            body = (ROOT / relative_path).read_bytes()
        except FileNotFoundError:
            self.send_json(500, {"error": "A chatbot website file is missing."})
            return
        self.send_bytes(200, body, content_type)

    def do_POST(self) -> None:
        if urlparse(self.path).path != "/api/chat":
            self.send_json(404, {"error": "Not found"})
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self.send_json(400, {"error": "Invalid request size."})
            return
        if content_length < 1 or content_length > MAX_BODY_BYTES:
            self.send_json(413, {"error": "Request is empty or too large."})
            return

        try:
            payload = json.loads(self.rfile.read(content_length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self.send_json(400, {"error": "Send a valid JSON message."})
            return
        if not isinstance(payload, dict) or not isinstance(payload.get("message"), str):
            self.send_json(400, {"error": "A message is required."})
            return

        message = payload["message"].strip()
        if not message:
            self.send_json(400, {"error": "Type a message to continue."})
            return
        if len(message) > MAX_MESSAGE_CHARS:
            self.send_json(413, {"error": f"Keep messages under {MAX_MESSAGE_CHARS} characters."})
            return

        try:
            response = build_reply(message)
        except FileNotFoundError:
            self.send_json(503, {"error": "An intent reference file is missing. Please contact Zcoated directly."})
            return
        self.send_json(200, response)

    def log_message(self, format: str, *args: Any) -> None:
        print(f"{self.address_string()} - {format % args}")


def main() -> None:
    address = ("127.0.0.1", 8765)
    server = ThreadingHTTPServer(address, ChatbotHandler)
    print(f"Zcoated chatbot is running at http://{address[0]}:{address[1]}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Zcoated chatbot.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
