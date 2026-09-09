"""
CivicResolve Guardian - Multi-Channel Notification Dispatch Engine
Dispatches bilingual (Tamil தமிழ் / English) alerts via WhatsApp Business, SMS, and Email
with tracking deep-links and simulated delivery verification.
"""

from typing import Dict, Any, Optional
from datetime import datetime, timezone


NOTIFICATION_TEMPLATES = {
    "COMPLAINT_RECEIVED": {
        "en": "CivicResolve: Your complaint #{id} for '{category}' has been registered. Track status: {link}",
        "ta": "CivicResolve: உங்கள் புகார் #{id} பதிவு செய்யப்பட்டுள்ளது. நிலை அறிய: {link}",
    },
    "OFFICER_APPROVED": {
        "en": "CivicResolve: Officer has approved your complaint #{id}. Assigned to {dept}. SLA target: {sla}h.",
        "ta": "CivicResolve: உங்கள் புகார் #{id} அதிகாரி ஒப்புதல் அளித்தார். துறை: {dept}.",
    },
    "WORK_COMPLETED": {
        "en": "CivicResolve: Work completed for complaint #{id}. Please verify resolution: {link}",
        "ta": "CivicResolve: புகார் #{id} பணி நிறைவுற்றது. சரிபார்க்க: {link}",
    },
}


class NotificationDispatcher:
    """Dispatches notifications across digital and telephonic channels."""

    @classmethod
    def dispatch_alert(
        cls,
        channel: str,
        recipient: str,
        template_key: str,
        lang: str,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        template_group = NOTIFICATION_TEMPLATES.get(template_key, NOTIFICATION_TEMPLATES["COMPLAINT_RECEIVED"])
        template_str = template_group.get(lang.lower(), template_group["en"])

        message_body = template_str.format(**context)
        channel_upper = channel.upper()

        dispatch_id = f"NOTIF-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{recipient[-4:] if len(recipient)>=4 else '0000'}"

        return {
            "dispatch_id": dispatch_id,
            "channel": channel_upper,
            "recipient_masked": recipient[:3] + "******" + recipient[-2:] if len(recipient) >= 8 else recipient,
            "language": lang.lower(),
            "template_key": template_key,
            "message_body": message_body,
            "status": "DELIVERED_SIMULATED",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
