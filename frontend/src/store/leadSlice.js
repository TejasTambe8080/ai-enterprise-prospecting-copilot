import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { leadAPI } from '../api/endpoints';

// Async thunks
export const fetchLeads = createAsyncThunk(
  'leads/fetchLeads',
  async (params) => {
    const response = await leadAPI.getLeads(params);
    return response.data;
  }
);

export const fetchLeadById = createAsyncThunk(
  'leads/fetchLeadById',
  async (id) => {
    const response = await leadAPI.getLead(id);
    return response.data;
  }
);

export const createLead = createAsyncThunk(
  'leads/createLead',
  async (data) => {
    const response = await leadAPI.createLead(data);
    return response.data;
  }
);

export const processLead = createAsyncThunk(
  'leads/processLead',
  async (id) => {
    const response = await leadAPI.processLead(id);
    return response.data;
  }
);

const initialState = {
  leads: [],
  currentLead: null,
  stats: {
    total: 0,
    qualified: 0,
    processing: 0,
    avgScore: 0,
  },
  loading: false,
  error: null,
};

const leadSlice = createSlice({
  name: 'leads',
  initialState,
  reducers: {
    clearCurrentLead: (state) => {
      state.currentLead = null;
    },
    updateLeadStatus: (state, action) => {
      const { id, status } = action.payload;
      const lead = state.leads.find((l) => l.id === id);
      if (lead) {
        lead.status = status;
      }
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch leads
      .addCase(fetchLeads.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchLeads.fulfilled, (state, action) => {
        state.loading = false;
        state.leads = action.payload.data || [];
        state.stats = calculateStats(action.payload.data || []);
      })
      .addCase(fetchLeads.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
      // Fetch lead by ID
      .addCase(fetchLeadById.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchLeadById.fulfilled, (state, action) => {
        state.loading = false;
        state.currentLead = action.payload.data;
      })
      .addCase(fetchLeadById.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
      // Create lead
      .addCase(createLead.fulfilled, (state, action) => {
        // Could add to leads list if needed
      })
      // Process lead
      .addCase(processLead.fulfilled, (state, action) => {
        // Could update lead status
      });
  },
});

// Helper function to calculate stats
const calculateStats = (leads) => {
  const total = leads.length;
  const qualified = leads.filter((l) => l.status === 'qualified').length;
  const processing = leads.filter((l) => l.status === 'processing').length;
  const scores = leads
    .map((l) => l.meddpicc_score?.total_score || 0)
    .filter((s) => s > 0);
  const avgScore = scores.length > 0 
    ? scores.reduce((a, b) => a + b, 0) / scores.length 
    : 0;
  
  return { total, qualified, processing, avgScore: Math.round(avgScore) };
};

export const { clearCurrentLead, updateLeadStatus } = leadSlice.actions;
export default leadSlice.reducer;