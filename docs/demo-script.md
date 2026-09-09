# Interactive 5-Minute Demo Walkthrough

Follow this step-by-step walkthrough to present CivicResolve Guardian during a portfolio review or technical demo:

---

### Step 1: Citizen Submission in Tamil (தமிழ்)
1. Open `http://localhost:5173`.
2. Click the **Language Toggle** in the top right to switch to **தமிழ் (TA)**.
3. Observe all labels, titles, and placeholders updating smoothly into authentic Tamil.
4. Click **Record Voice Note** or paste:
   > *"எங்கள் பகுதியில் கதவு எண் 12, 4வது குறுக்குத் தெருவில் கடந்த மூன்று நாட்களாக குடிநீர் குழாய் உடைந்து குடிநீரில் கழிவுநீர் துர்நாற்றம் வீசுகிறது. தொடர்பு எண் 9840123456."*
5. Click **Preview PII Redaction** to verify that `9840123456` and `கதவு எண் 12` are masked live.
6. Click **புகாரை சமர்ப்பிக்கவும் (Submit Grievance)**.
7. Copy the generated Complaint UUID.

---

### Step 2: Officer Queue & AI Triage Review
1. Switch the simulated user role in the top navbar to **Officer (GRO)**.
2. Click on the **Officer Queue** tab.
3. Locate the newly filed complaint at the top of the queue.
4. Click **Run AI Triage**. Notice the AI categorizing it into:
   - Department: `Water Supply & Sewerage Board`
   - Priority: `CRITICAL`
   - Confidence: ~`88%`
5. Click **Approve Routing** to open the **Human-in-the-Loop Review Drawer**.

---

### Step 3: Inspect Policy Citations & Confirm Routing
1. Inside the drawer, view the side-by-side **Grounded Policy Citations Panel**:
   - Citations link directly to **Section 1.1: Drinking Water Contamination & Discoloration** of the *Tamil Nadu Water Supply & Sewerage Charter*.
   - Target SLA: `24 Hours`.
2. Notice the **Missing Evidence Gaps** alert requesting photographic evidence of the pipe burst.
3. Click **Confirm & Dispatch Field Team**.
4. The case transitions to `ROUTED_ASSIGNED`.

---

### Step 4: Resolution Veracity & Contradiction Checking
1. Click **Verify Resolution**.
2. Type an incomplete or contradictory resolution note:
   > *"Temporary patch placed, cannot be repaired today due to funds awaited."*
3. Click **Evaluate Resolution Quality**.
4. Notice the AI Resolution Auditor immediately flagging:
   - **Verdict**: `Contradiction Detected` (Confidence 90%)
   - **Explanation**: Detected phrase `funds awaited` indicating incomplete remediation.
5. Now update the resolution note with verifiable completion proof:
   > *"Main pipeline valve replaced and sanitized with bleaching powder. Water pressure restored and tested zero coliform."*
6. Attach a photo and re-run evaluation.
7. Observe the verdict changing to **Likely Genuinely Resolved** (Confidence 92%) and the case transitioning to `VERIFIED_RESOLVED`.

---

### Step 5: Cryptographic Audit Trail Verification
1. Open the case details and inspect the **Cryptographic Audit Trail**.
2. Review all lifecycle events: `COMPLAINT_CREATED` -> `TRIAGE_RECOMMENDED` -> `ROUTING_APPROVED` -> `RESOLUTION_EVALUATED`.
3. Highlight the unique `HMAC-SHA256` signature attached to every single event, ensuring tampering is impossible.
