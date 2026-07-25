import { api } from './client';

export const leadAPI = {
  // Get all leads with pagination
  getLeads: (params = {}) => api.get('/leads', { params }),
  
  // Get lead by ID
  getLead: (id) => api.get(`/leads/${id}`),
  
  // Create new lead
  createLead: (data) => api.post('/leads', data),
  
  // Process lead
  processLead: (id) => api.post(`/leads/${id}/process`),
  
  // Process email directly
  processEmail: (emailContent) => api.post('/leads/process-email', { email_content: emailContent }),
};

export const analysisAPI = {
  // Analyze company
  analyzeCompany: (companyName) => api.post('/analysis/analyze', null, { params: { company_name: companyName } }),
};

export const agentAPI = {
  // Get agent status
  getStatus: () => api.get('/agents/status'),
};