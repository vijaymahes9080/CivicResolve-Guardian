import { ComplaintRecord, RoutingRecommendation, ResolutionAssessment, AuditEvent, PolicyCitation, PolicyDocumentOut } from '../types';

const API_BASE_URL = 'http://localhost:8000/api/v1';

// Preset tokens for simulated testing and interactive demonstration
export const DEMO_TOKENS = {
  citizen: '', // Dynamically fetched or auto-logged in
  officer: '',
  admin: ''
};

class ApiService {
  private token: string | null = null;
  private currentRole: 'citizen' | 'officer' | 'admin' = 'citizen';

  setRole(role: 'citizen' | 'officer' | 'admin') {
    this.currentRole = role;
  }

  getRole() {
    return this.currentRole;
  }

  async authenticate(role: 'citizen' | 'officer' | 'admin') {
    const creds = {
      citizen: { email: 'citizen@civicresolve.gov.in', password: 'Citizen@2026!' },
      officer: { email: 'officer@civicresolve.gov.in', password: 'Officer@2026!' },
      admin: { email: 'admin@civicresolve.gov.in', password: 'Admin@2026!' }
    };
    
    try {
      const resp = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(creds[role])
      });
      if (resp.ok) {
        const data = await resp.json();
        this.token = data.access_token;
        this.currentRole = role;
        return data.user;
      }
    } catch (e) {
      console.warn('Backend offline, using local client mode', e);
    }
    return null;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    if (!this.token) {
      await this.authenticate(this.currentRole);
    }

    const headers: Record<string, string> = {
      ...(options.headers as Record<string, string> || {}),
      'Authorization': `Bearer ${this.token || ''}`
    };

    if (!(options.body instanceof FormData)) {
      headers['Content-Type'] = 'application/json';
    }

    const resp = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers
    });

    if (!resp.ok) {
      const err = await resp.json().catch(() => ({ detail: 'Network request failed' }));
      throw new Error(err.detail || `Error ${resp.status}: ${resp.statusText}`);
    }

    return resp.json();
  }

  async createComplaint(data: { content: string; language?: string; ward?: string; zone?: string; has_audio?: boolean }): Promise<ComplaintRecord> {
    return this.request<ComplaintRecord>('/complaints', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async getComplaints(params?: { status?: string; department?: string; ward?: string }): Promise<ComplaintRecord[]> {
    const query = new URLSearchParams(params as any).toString();
    return this.request<ComplaintRecord[]>(`/complaints${query ? `?${query}` : ''}`);
  }

  async getComplaint(id: string): Promise<ComplaintRecord> {
    return this.request<ComplaintRecord>(`/complaints/${id}`);
  }

  async uploadEvidence(id: string, file: File, description?: string): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);
    if (description) formData.append('description', description);
    
    return this.request(`/complaints/${id}/evidence`, {
      method: 'POST',
      body: formData
    });
  }

  async runTriage(id: string): Promise<RoutingRecommendation> {
    return this.request<RoutingRecommendation>(`/complaints/${id}/triage`, {
      method: 'POST'
    });
  }

  async approveRouting(id: string, data: { approved_department?: string; approved_priority?: string; override_reason?: string; officer_notes?: string }): Promise<ComplaintRecord> {
    return this.request<ComplaintRecord>(`/complaints/${id}/approve-routing`, {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async evaluateResolution(id: string, data: { action_taken_summary: string; completion_notes?: string }): Promise<ResolutionAssessment> {
    return this.request<ResolutionAssessment>(`/complaints/${id}/resolution-check`, {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async getAuditTrail(caseId: string): Promise<AuditEvent[]> {
    return this.request<AuditEvent[]>(`/audit/${caseId}`);
  }

  async searchPolicies(query: string, department?: string): Promise<PolicyCitation[]> {
    const q = new URLSearchParams({ query, ...(department ? { department } : {}) }).toString();
    return this.request<PolicyCitation[]>(`/policies/search?${q}`);
  }

  async getPolicyDocuments(): Promise<PolicyDocumentOut[]> {
    return this.request<PolicyDocumentOut[]>('/policies/documents');
  }
}

export const api = new ApiService();
