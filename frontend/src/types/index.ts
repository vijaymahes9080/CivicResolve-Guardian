export interface User {
  id: string;
  email: string;
  full_name: string;
  role: 'citizen' | 'officer' | 'admin';
  phone_number?: string;
  preferred_language: 'en' | 'ta';
  department?: string;
  ward?: string;
  zone?: string;
}

export interface PolicyCitation {
  policy_id: string;
  section_id: string;
  title: string;
  excerpt: string;
  relevance_score: number;
}

export interface PolicyDocumentOut {
  id: string;
  title: string;
  department: string;
  jurisdiction: string;
  version: string;
  effective_date?: string;
  sla_hours: number;
  summary?: string;
}

export interface RoutingRecommendation {
  id: string;
  complaint_id: string;
  suggested_category: string;
  suggested_department: string;
  priority_score: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  confidence: number;
  reasons: string[];
  citations: PolicyCitation[];
  duplicate_candidates: Array<{
    complaint_id: string;
    similarity_score: number;
    status: string;
  }>;
  missing_evidence: string[];
  draft_citizen_response?: string;
  approval_required: boolean;
  is_approved: boolean;
  is_overridden: boolean;
  override_reason?: string;
  created_at: string;
  approved_at?: string;
}

export interface EvidenceItem {
  id: string;
  complaint_id: string;
  file_name: string;
  file_type: string;
  file_size_bytes: number;
  storage_path: string;
  is_redacted: boolean;
  sha256_hash?: string;
  description?: string;
  uploaded_by_role: string;
  uploaded_at: string;
}

export interface ResolutionAssessment {
  id: string;
  complaint_id: string;
  evaluation_verdict: 'likely_resolved' | 'weak_resolution' | 'insufficient_evidence' | 'contradiction_detected';
  confidence: number;
  explanation: string;
  deterministic_checks_passed: boolean;
  checks_detail: {
    required_fields_present?: boolean;
    resolution_evidence_attached?: boolean;
    dates_consistent?: boolean;
    addressed_requested_issue?: boolean;
    valid_status_transition?: boolean;
  };
  contradiction_detected: boolean;
  contradiction_notes?: string;
  evidence_references: string[];
  citizen_satisfaction_score?: number;
  evaluated_at: string;
}

export interface ComplaintRecord {
  id: string;
  citizen_id: string;
  original_language: 'en' | 'ta';
  redacted_content: string;
  raw_content?: string;
  has_audio: boolean;
  audio_consent_stored: boolean;
  transcription?: string;
  category?: string;
  department?: string;
  ward?: string;
  zone?: string;
  priority: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  status:
    | 'SUBMITTED'
    | 'TRIAGED_PENDING_APPROVAL'
    | 'ROUTED_ASSIGNED'
    | 'IN_PROGRESS'
    | 'ACTION_PROPOSED'
    | 'RESOLVED_PENDING_VERIFICATION'
    | 'VERIFIED_RESOLVED'
    | 'REOPENED'
    | 'REJECTED';
  assigned_officer_id?: string;
  officer_notes?: string;
  resolution_summary?: string;
  created_at: string;
  updated_at: string;
  sla_due_at?: string;
  evidence_items?: EvidenceItem[];
  recommendation?: RoutingRecommendation;
  resolution_assessment?: ResolutionAssessment;
}

export interface AuditEvent {
  id: string;
  case_id: string;
  actor_id: string;
  actor_role: 'citizen' | 'officer' | 'admin' | 'system' | 'mcp_tool';
  action_type: string;
  details: Record<string, any>;
  previous_state?: string;
  new_state?: string;
  timestamp: string;
  signature: string;
}
