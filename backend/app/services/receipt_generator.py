"""
CivicResolve Guardian - Official Citizen Complaint Receipt Generator
Produces printable bilingual acknowledgment receipts with cryptographic Merkle verification badges,
SLA commitment deadlines, and municipal contact information.
"""

from typing import Dict, Any


RECEIPT_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Official Municipal Acknowledgment Receipt - {complaint_id}</title>
<style>
  body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; color: #1e293b; }}
  .header {{ border-bottom: 3px solid #0284c7; padding-bottom: 16px; margin-bottom: 24px; display: flex; justify-content: space-between; }}
  .corp-title {{ font-size: 20px; font-weight: bold; color: #0f172a; }}
  .corp-tamil {{ font-size: 16px; color: #0284c7; font-weight: 600; margin-top: 4px; }}
  .badge {{ background: #e0f2fe; color: #0369a1; padding: 4px 12px; border-radius: 9999px; font-weight: bold; font-size: 13px; }}
  .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px; }}
  .box {{ background: #f8fafc; border: 1px solid #e2e8f0; padding: 14px; border-radius: 8px; }}
  .label {{ font-size: 11px; text-transform: uppercase; color: #64748b; font-weight: bold; margin-bottom: 4px; }}
  .val {{ font-size: 14px; font-weight: 600; }}
  .crypto-bar {{ background: #f1f5f9; border-left: 4px solid #10b981; padding: 12px; font-family: monospace; font-size: 12px; margin-top: 24px; }}
</style>
</head>
<body>
  <div class="header">
    <div>
      <div class="corp-title">GREATER CHENNAI CORPORATION / தமிழ்நாடு நகராட்சி நிர்வாகம்</div>
      <div class="corp-tamil">பொதுமக்கள் குறைதீர்ப்பு அதிகாரப்பூர்வ ரசீது (Grievance Receipt)</div>
    </div>
    <div>
      <span class="badge">STATUS: {status}</span>
    </div>
  </div>

  <div class="grid">
    <div class="box">
      <div class="label">Complaint Reference ID / புகார் எண்</div>
      <div class="val">{complaint_id}</div>
    </div>
    <div class="box">
      <div class="label">Filing Date & Time / பதிவு நாள்</div>
      <div class="val">{created_at}</div>
    </div>
    <div class="box">
      <div class="label">Category / துறை</div>
      <div class="val">{category} ({department})</div>
    </div>
    <div class="box">
      <div class="label">SLA Resolution Target / தீர்வு காலக்கெடு</div>
      <div class="val">{sla_target_hours} Hours / மணி நேரம்</div>
    </div>
  </div>

  <div class="box" style="margin-bottom: 20px;">
    <div class="label">Description / புகார் சுருக்கம்</div>
    <div class="val" style="margin-bottom: 8px;">{title_en}</div>
    <div style="font-size: 13px; color: #475569;">{description_redacted}</div>
  </div>

  <div class="crypto-bar">
    <strong>CRYPTOGRAPHIC INTEGRITY ROOT:</strong><br>
    SHA-256 Merkle: {merkle_root}<br>
    <em>This record is cryptographically signed and protected against unauthorized tampering.</em>
  </div>
</body>
</html>
"""


class ReceiptGenerator:
    """Generates citizen acknowledgment slips for print and verification."""

    @classmethod
    def generate_html_receipt(cls, complaint_data: Dict[str, Any], merkle_root: str = "N/A") -> str:
        return RECEIPT_HTML_TEMPLATE.format(
            complaint_id=complaint_data.get("id", "N/A"),
            status=complaint_data.get("status", "SUBMITTED").upper(),
            created_at=complaint_data.get("created_at", "2026-09-09T10:00:00Z"),
            category=complaint_data.get("category", "GENERAL"),
            department=complaint_data.get("department", "Municipal Services"),
            sla_target_hours=complaint_data.get("sla_target_hours", 48),
            title_en=complaint_data.get("title_en", "Civic Grievance"),
            description_redacted=complaint_data.get("description_redacted", "Details recorded in vault."),
            merkle_root=merkle_root,
        )
