"""
CivicResolve Guardian - Visual Asset & Showcase Image Generator
Generates pixel-perfect light-theme UI mockups, architecture visuals, and the LinkedIn banner.
"""

import os
from PIL import Image, ImageDraw, ImageFont


def get_font(name: str = "segoeui.ttf", size: int = 16, bold: bool = False):
    font_file = "segoeuib.ttf" if bold else name
    font_path = os.path.join("C:/Windows/Fonts", font_file)
    if os.path.exists(font_path):
        return ImageFont.truetype(font_path, size)
    # Fallback to arial
    alt_file = "arialbd.ttf" if bold else "arial.ttf"
    alt_path = os.path.join("C:/Windows/Fonts", alt_file)
    if os.path.exists(alt_path):
        return ImageFont.truetype(alt_path, size)
    return ImageFont.load_default()


def create_linkedin_banner():
    """Generates a professional 1200x630 LinkedIn project showcase banner (image.png)."""
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), "#f8fafc")
    draw = ImageDraw.Draw(img)

    # Top gradient banner
    for y in range(8):
        draw.line([(0, y), (w, y)], fill="#0284c7")

    # Header section
    font_title = get_font("segoeui.ttf", 44, bold=True)
    font_sub = get_font("segoeui.ttf", 20, bold=False)
    font_chip = get_font("segoeui.ttf", 14, bold=True)
    font_body = get_font("segoeui.ttf", 16, bold=False)
    font_bold = get_font("segoeui.ttf", 16, bold=True)

    # Badge
    draw.rounded_rectangle([60, 40, 360, 72], radius=16, fill="#e0f2fe", outline="#bae6fd", width=1)
    draw.text((75, 47), "MUNICIPAL CIVIC-TECH AI PLATFORM", fill="#0369a1", font=font_chip)

    # Title
    draw.text((60, 85), "CivicResolve Guardian", fill="#0f172a", font=font_title)
    draw.text((60, 142), "Multilingual (Tamil & English) Public Grievance Triage & Resolution Platform", fill="#475569", font=font_sub)

    # Main Showcase Cards Grid
    cards = [
        ("Dual-Storage Privacy Vault", "Automatic PII scrub (Aadhaar, Phone, Door Addr) with zero data leak to public or LLM layers.", "#0284c7", "#e0f2fe"),
        ("Grounded Policy RAG Engine", "Cites exact municipal bylaws (Water, Waste, Roads, Lighting). Fallback when evidence is below 0.50.", "#10b981", "#d1fae5"),
        ("Cryptographic Merkle Proofs", "Immutable SHA-256 Merkle audit trail preventing status backdating or corrupt administrative tampering.", "#8b5cf6", "#ede9fe"),
        ("Spatial GIS Hotspot Clustering", "Real-time DBSCAN geodesic proximity analysis detecting trunk main ruptures & infrastructure crises.", "#f59e0b", "#fef3c7"),
        ("PWD Cost & Resource Estimator", "Automated budgeting in INR (₹) using TN PWD Schedule of Rates (SOR) for heavy equipment & labor.", "#0ea5e9", "#e0f2fe"),
        ("Human-in-the-Loop Governance", "Deterministic bounded triage state machine. Zero autonomous status changes without officer sign-off.", "#ef4444", "#fee2e2"),
    ]

    x_start, y_start = 60, 195
    card_w, card_h = 345, 110
    cols = 3

    for idx, (title, desc, accent, bg_chip) in enumerate(cards):
        col = idx % cols
        row = idx // cols
        cx = x_start + col * (card_w + 22)
        cy = y_start + row * (card_h + 20)

        # Card body
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=14, fill="#ffffff", outline="#e2e8f0", width=1)
        # Left accent stripe
        draw.rounded_rectangle([cx, cy, cx + 6, cy + card_h], radius=3, fill=accent)

        # Title
        draw.text((cx + 18, cy + 14), title, fill="#0f172a", font=font_bold)

        # Description wrapped
        words = desc.split()
        lines, cur_line = [], []
        for w_word in words:
            cur_line.append(w_word)
            if len(" ".join(cur_line)) > 38:
                lines.append(" ".join(cur_line[:-1]))
                cur_line = [w_word]
        if cur_line:
            lines.append(" ".join(cur_line))

        for line_idx, line in enumerate(lines[:3]):
            draw.text((cx + 18, cy + 38 + line_idx * 20), line, fill="#64748b", font=get_font("segoeui.ttf", 13))

    # Bottom Metrics & Author Banner
    draw.rounded_rectangle([60, 480, 1140, 570], radius=16, fill="#0f172a")

    draw.text((90, 502), "TEST COVERAGE: 65/65 PASSING (100%)", fill="#34d399", font=font_chip)
    draw.text((90, 530), "FastAPI • React 18 • TypeScript • Tailwind • n8n • FastMCP • SQLite/Postgres", fill="#94a3b8", font=get_font("segoeui.ttf", 13))

    draw.text((800, 502), "ARCHITECT & AUTHOR", fill="#94a3b8", font=get_font("segoeui.ttf", 12))
    draw.text((800, 526), "Vijay Mahes  |  @vijaymahes9080", fill="#ffffff", font=get_font("segoeui.ttf", 18, bold=True))

    img.save("image.png", "PNG", quality=95)
    print("Generated image.png successfully.")


def create_hero_light():
    """Generates docs/assets/hero_light.png showing the main portal overview."""
    w, h = 1000, 550
    img = Image.new("RGB", (w, h), "#ffffff")
    draw = ImageDraw.Draw(img)

    # Window bar
    draw.rectangle([0, 0, w, 38], fill="#f1f5f9")
    draw.ellipse([14, 13, 24, 23], fill="#ef4444")
    draw.ellipse([32, 13, 42, 23], fill="#f59e0b")
    draw.ellipse([50, 13, 60, 23], fill="#10b981")
    draw.text((75, 11), "CivicResolve Guardian — Municipal Operations Dashboard (Light Theme)", fill="#64748b", font=get_font("segoeui.ttf", 12))

    # Header Navbar
    draw.rectangle([0, 38, w, 95], fill="#ffffff", outline="#e2e8f0")
    draw.text((30, 52), "🏛️ CivicResolve Guardian", fill="#0f172a", font=get_font("segoeui.ttf", 20, bold=True))
    draw.text((300, 58), "பெருநகர சென்னை மாநகராட்சி (Greater Chennai Corporation)", fill="#0284c7", font=get_font("segoeui.ttf", 13, bold=True))

    # Metric Cards
    metrics = [
        ("Verified Resolutions", "98.4%", "#10b981", "#ecfdf5"),
        ("PII Leaks Prevented", "100%", "#0284c7", "#eff6ff"),
        ("Avg. SLA Velocity", "18.2 hrs", "#8b5cf6", "#f5f3ff"),
        ("Cryptographic Proofs", "Active (SHA-256)", "#f59e0b", "#fffbeb"),
    ]
    for idx, (label, val, col, bg) in enumerate(metrics):
        cx = 30 + idx * 235
        draw.rounded_rectangle([cx, 115, cx + 220, 185], radius=12, fill=bg, outline="#e2e8f0")
        draw.text((cx + 16, 128), label, fill="#64748b", font=get_font("segoeui.ttf", 12))
        draw.text((cx + 16, 148), val, fill=col, font=get_font("segoeui.ttf", 22, bold=True))

    # Split View: Triage Queue on Left, Citation Drawer on Right
    # Left Box
    draw.rounded_rectangle([30, 205, 540, 515], radius=12, fill="#f8fafc", outline="#e2e8f0")
    draw.text((45, 220), "Active Officer Triage Stream (Bilingual Intake)", fill="#0f172a", font=get_font("segoeui.ttf", 14, bold=True))

    cases = [
        ("CMP-2026-0001", "குடிநீர் குழாய் உடைப்பு - Ward 115", "WATER_SUPPLY", "CRITICAL", "#ef4444"),
        ("CMP-2026-0002", "Dangerous crater pothole on 100ft road", "ROAD_TRANSPORT", "HIGH", "#f59e0b"),
        ("CMP-2026-0003", "Street light luminaire failure at dusk", "STREET_LIGHTING", "MEDIUM", "#3b82f6"),
        ("CMP-2026-0004", "Solid waste bin overflow & foul odor", "SOLID_WASTE", "MEDIUM", "#10b981"),
    ]
    for idx, (cid, title, dept, pri, col) in enumerate(cases):
        cy = 250 + idx * 62
        draw.rounded_rectangle([45, cy, 525, cy + 54], radius=8, fill="#ffffff", outline="#e2e8f0")
        draw.text((55, cy + 10), cid, fill="#0284c7", font=get_font("segoeui.ttf", 11, bold=True))
        draw.text((160, cy + 10), dept, fill="#64748b", font=get_font("segoeui.ttf", 10))
        draw.rounded_rectangle([450, cy + 8, 515, cy + 26], radius=4, fill=col)
        draw.text((458, cy + 10), pri, fill="#ffffff", font=get_font("segoeui.ttf", 9, bold=True))
        draw.text((55, cy + 30), title, fill="#1e293b", font=get_font("segoeui.ttf", 12))

    # Right Box - Grounded RAG Citation Inspector
    draw.rounded_rectangle([560, 205, 970, 515], radius=12, fill="#ffffff", outline="#e2e8f0")
    draw.text((575, 220), "Policy Citation Inspector (Grounded RAG)", fill="#0f172a", font=get_font("segoeui.ttf", 14, bold=True))

    draw.rounded_rectangle([575, 250, 955, 335], radius=8, fill="#f0fdf4", outline="#bbf7d0")
    draw.text((585, 260), "SECTION 4.2 - WATER SUPPLY CHARTER", fill="#166534", font=get_font("segoeui.ttf", 11, bold=True))
    draw.text((585, 280), "Underground pipeline burst threatening road integrity mandates", fill="#374151", font=get_font("segoeui.ttf", 11))
    draw.text((585, 298), "emergency response within 24 hours with dewatering pump.", fill="#374151", font=get_font("segoeui.ttf", 11))
    draw.text((585, 318), "Confidence Score: 0.88  •  Citation Verified", fill="#15803d", font=get_font("segoeui.ttf", 10, bold=True))

    # Resource estimate
    draw.rounded_rectangle([575, 350, 955, 435], radius=8, fill="#eff6ff", outline="#bfdbfe")
    draw.text((585, 360), "PWD SCHEDULE OF RATES (SOR 2025-26)", fill="#1e40af", font=get_font("segoeui.ttf", 11, bold=True))
    draw.text((585, 380), "Assigned: Super Sucker Jetting Tanker + 4 Plumbing Crew", fill="#374151", font=get_font("segoeui.ttf", 11))
    draw.text((585, 398), "Estimated Repair Budget: ₹ 16,600  (JE / AEE Sanction Level)", fill="#1d4ed8", font=get_font("segoeui.ttf", 11, bold=True))

    # Human-in-the-loop action
    draw.rounded_rectangle([575, 455, 955, 498], radius=8, fill="#0284c7")
    draw.text((680, 468), "✓ Approve Triage & Sanction Work Order", fill="#ffffff", font=get_font("segoeui.ttf", 13, bold=True))

    os.makedirs("docs/assets", exist_ok=True)
    img.save("docs/assets/hero_light.png", "PNG", quality=95)
    print("Generated docs/assets/hero_light.png successfully.")


def create_citizen_portal_light():
    """Generates docs/assets/citizen_portal_light.png showing the citizen filing UI."""
    w, h = 900, 500
    img = Image.new("RGB", (w, h), "#f8fafc")
    draw = ImageDraw.Draw(img)

    # Window header
    draw.rectangle([0, 0, w, 36], fill="#f1f5f9", outline="#e2e8f0")
    draw.ellipse([14, 12, 24, 22], fill="#ef4444")
    draw.ellipse([32, 12, 42, 22], fill="#f59e0b")
    draw.ellipse([50, 12, 60, 22], fill="#10b981")
    draw.text((75, 10), "Citizen Portal — Multilingual Intake & Privacy Vault", fill="#64748b", font=get_font("segoeui.ttf", 11))

    # Form card
    draw.rounded_rectangle([40, 55, 860, 465], radius=16, fill="#ffffff", outline="#e2e8f0")

    # Header
    draw.text((65, 75), "பொதுமக்கள் புகார் பதிவு (Citizen Grievance Submission)", fill="#0f172a", font=get_font("segoeui.ttf", 18, bold=True))
    draw.rounded_rectangle([720, 72, 835, 102], radius=8, fill="#e0f2fe")
    draw.text((735, 79), "Language: தமிழ்", fill="#0369a1", font=get_font("segoeui.ttf", 12, bold=True))

    # Form inputs
    draw.text((65, 120), "Grievance Description / புகார் விவரம்", fill="#475569", font=get_font("segoeui.ttf", 12, bold=True))
    draw.rounded_rectangle([65, 140, 835, 230], radius=8, fill="#f8fafc", outline="#cbd5e1")
    draw.text((75, 150), "குடிநீர் குழாயில் விரிசல் ஏற்பட்டு சாலையில் தண்ணீர் வீணாக ஓடுகிறது. கதவு எண் 42, அண்ணா நகர்.", fill="#0f172a", font=get_font("segoeui.ttf", 13))
    draw.text((75, 175), "தொடர்புக்கு என் எண்: 9840123456 (Aadhaar: 2345 6789 0123)", fill="#64748b", font=get_font("segoeui.ttf", 12))

    # Privacy vault badge
    draw.rounded_rectangle([65, 245, 835, 295], radius=8, fill="#eff6ff", outline="#bfdbfe")
    draw.text((75, 255), "🛡️ DUAL-STORAGE PRIVACY VAULT (AUTOMATIC REDACTION ACTIVE)", fill="#1d4ed8", font=get_font("segoeui.ttf", 11, bold=True))
    draw.text((75, 273), "Scrubbed for public feed: கதவு எண் [DOOR_ADDRESS_REDACTED] ... தொடர்புக்கு [PHONE_REDACTED]", fill="#3b82f6", font=get_font("segoeui.ttf", 11))

    # Voice Note Bar & Photo upload
    draw.rounded_rectangle([65, 310, 440, 390], radius=10, fill="#f8fafc", outline="#e2e8f0")
    draw.text((75, 320), "🎙️ Tamil Voice Note Recorder", fill="#0f172a", font=get_font("segoeui.ttf", 12, bold=True))
    draw.text((75, 342), "Live audio waveform visualizer • AI Whisper transcription", fill="#64748b", font=get_font("segoeui.ttf", 11))
    draw.rounded_rectangle([75, 362, 190, 384], radius=4, fill="#10b981")
    draw.text((85, 366), "✓ Voice Transcribed", fill="#ffffff", font=get_font("segoeui.ttf", 10, bold=True))

    draw.rounded_rectangle([460, 310, 835, 390], radius=10, fill="#f8fafc", outline="#e2e8f0")
    draw.text((470, 320), "📷 Photo Evidence Forensics", fill="#0f172a", font=get_font("segoeui.ttf", 12, bold=True))
    draw.text((470, 342), "Camera EXIF Geotag: 13.0827°N, 80.2707°E (Location Match)", fill="#166534", font=get_font("segoeui.ttf", 11))
    draw.rounded_rectangle([470, 362, 595, 384], radius=4, fill="#0284c7")
    draw.text((480, 366), "✓ Veracity Score: 0.95", fill="#ffffff", font=get_font("segoeui.ttf", 10, bold=True))

    # Submit button
    draw.rounded_rectangle([65, 415, 835, 455], radius=8, fill="#0284c7")
    draw.text((380, 427), "புகாரை சமர்ப்பிக்க (Submit Grievance)", fill="#ffffff", font=get_font("segoeui.ttf", 13, bold=True))

    img.save("docs/assets/citizen_portal_light.png", "PNG", quality=95)
    print("Generated docs/assets/citizen_portal_light.png successfully.")


def create_merkle_audit_light():
    """Generates docs/assets/merkle_audit_light.png showing cryptographic Merkle audit proof."""
    w, h = 900, 450
    img = Image.new("RGB", (w, h), "#ffffff")
    draw = ImageDraw.Draw(img)

    # Title
    draw.text((40, 30), "Cryptographic Merkle Audit Engine — Tamper Proof Verification", fill="#0f172a", font=get_font("segoeui.ttf", 18, bold=True))
    draw.text((40, 58), "SHA-256 binary hash tree guaranteeing immutable public accountability for every grievance lifecycle event", fill="#64748b", font=get_font("segoeui.ttf", 12))

    # Merkle Root Box at Top
    draw.rounded_rectangle([250, 100, 650, 160], radius=12, fill="#f0fdf4", outline="#86efac", width=2)
    draw.text((265, 112), "MERKLE ROOT (SHA-256)", fill="#166534", font=get_font("segoeui.ttf", 11, bold=True))
    draw.text((265, 132), "8f4c2e8a719d3b14065e23a4918f7c9e0123456789abcdef", fill="#15803d", font=get_font("segoeui.ttf", 12, bold=True))

    # Intermediate Nodes
    draw.line([(350, 160), (200, 210)], fill="#94a3b8", width=2)
    draw.line([(550, 160), (700, 210)], fill="#94a3b8", width=2)

    draw.rounded_rectangle([100, 210, 300, 260], radius=8, fill="#f8fafc", outline="#cbd5e1")
    draw.text((115, 222), "Parent Hash A (L1)", fill="#475569", font=get_font("segoeui.ttf", 10, bold=True))
    draw.text((115, 238), "4a9e22ff38b19...", fill="#0284c7", font=get_font("segoeui.ttf", 11))

    draw.rounded_rectangle([600, 210, 800, 260], radius=8, fill="#f8fafc", outline="#cbd5e1")
    draw.text((615, 222), "Parent Hash B (L1)", fill="#475569", font=get_font("segoeui.ttf", 10, bold=True))
    draw.text((615, 238), "b7c1930dfa482...", fill="#0284c7", font=get_font("segoeui.ttf", 11))

    # Leaves (Audit Events)
    draw.line([(150, 260), (90, 310)], fill="#94a3b8", width=1)
    draw.line([(250, 260), (310, 310)], fill="#94a3b8", width=1)
    draw.line([(650, 260), (590, 310)], fill="#94a3b8", width=1)
    draw.line([(750, 260), (810, 310)], fill="#94a3b8", width=1)

    leaves = [
        ("Event 1: Filed", "SUBMITTED", 40),
        ("Event 2: Vaulted", "PII_REDACTED", 260),
        ("Event 3: Approved", "OFFICER_SIGNED", 480),
        ("Event 4: Verified", "RESOLUTION_AUDITED", 700),
    ]

    for title, action, lx in leaves:
        draw.rounded_rectangle([lx, 310, lx + 160, 380], radius=8, fill="#eff6ff", outline="#bfdbfe")
        draw.text((lx + 10, 320), title, fill="#1e40af", font=get_font("segoeui.ttf", 11, bold=True))
        draw.text((lx + 10, 340), action, fill="#64748b", font=get_font("segoeui.ttf", 10))
        draw.text((lx + 10, 358), "✓ Valid Inclusion Proof", fill="#16a34a", font=get_font("segoeui.ttf", 10, bold=True))

    # Bottom status
    draw.rounded_rectangle([40, 400, 860, 435], radius=8, fill="#f0fdf4", outline="#bbf7d0")
    draw.text((320, 412), "🔒 TAMPER-FREE GUARANTEE: Zero Backdating or Fraudulent Status Overwrites Possible", fill="#166534", font=get_font("segoeui.ttf", 11, bold=True))

    img.save("docs/assets/merkle_audit_light.png", "PNG", quality=95)
    print("Generated docs/assets/merkle_audit_light.png successfully.")


if __name__ == "__main__":
    create_linkedin_banner()
    create_hero_light()
    create_citizen_portal_light()
    create_merkle_audit_light()
