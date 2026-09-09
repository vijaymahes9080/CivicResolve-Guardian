"""
CivicResolve Guardian - Conversational WhatsApp / USSD Chatbot Simulator
Powers automated multi-turn grievance collection for low-bandwidth, SMS, and WhatsApp channels
in Tamil தமிழ் and English.
"""

from typing import Dict, Any, Optional
from app.core.pii import redact_pii


class WhatsAppChatbotSession:
    """Manages conversational state machine for non-web mobile chat interactions."""

    def __init__(self, phone_number: str, lang: str = "en"):
        self.phone_number = phone_number
        self.lang = lang
        self.state = "INIT"
        self.collected_data: Dict[str, Any] = {"phone": phone_number}

    def process_message(self, user_msg: str) -> Dict[str, Any]:
        msg_clean = user_msg.strip()

        if self.state == "INIT":
            self.state = "AWAIT_DESCRIPTION"
            reply = (
                "வணக்கம்! பெருநகர சென்னை மாநகராட்சி குறைதீர்ப்பு சேவைக்கு வரவேற்கிறோம். உங்கள் புகாரை சுருக்கமாக தட்டச்சு செய்யவும்:"
                if self.lang == "ta"
                else "Hello! Welcome to Greater Chennai Corporation Civic Bot. Please describe your civic grievance:"
            )
            return {"reply": reply, "state": self.state}

        elif self.state == "AWAIT_DESCRIPTION":
            # Redact PII in description
            pii_result = redact_pii(msg_clean)
            self.collected_data["description"] = pii_result["redacted_text"]
            self.state = "AWAIT_WARD"
            reply = (
                "உங்கள் வார்டு எண் அல்லது பகுதியை குறிப்பிடவும் (எ.கா: வார்டு 115, அண்ணா நகர்):"
                if self.lang == "ta"
                else "Please provide your Ward Number or Locality (e.g., Ward 115, Anna Nagar):"
            )
            return {"reply": reply, "state": self.state}

        elif self.state == "AWAIT_WARD":
            self.collected_data["ward"] = msg_clean
            self.state = "CONFIRMED"
            ticket_id = f"WA-{abs(hash(msg_clean + self.phone_number)) % 900000 + 100000}"
            self.collected_data["ticket_id"] = ticket_id

            reply = (
                f"நன்றி! உங்கள் புகார் பதிவு செய்யப்பட்டது. குறிப்பு எண்: #{ticket_id}. "
                f"வார்டு: {msg_clean}. எங்கள் களப்பணியாளர் விரைவில் தொடர்பு கொள்வார்."
                if self.lang == "ta"
                else f"Thank you! Your grievance is registered. Ticket: #{ticket_id}. "
                     f"Ward: {msg_clean}. Officer inspection initiated."
            )
            return {
                "reply": reply,
                "state": self.state,
                "ticket_id": ticket_id,
                "completed": True,
                "collected_data": self.collected_data,
            }

        return {
            "reply": "Your grievance is already under process. Send 'STATUS' to track." if self.lang == "en" else "உங்கள் புகார் பரிசீலனையில் உள்ளது.",
            "state": self.state,
        }
