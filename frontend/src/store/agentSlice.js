import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { agentAPI } from '../api/endpoints';

export const fetchAgentStatus = createAsyncThunk(
  'agents/fetchStatus',
  async () => {
    const response = await agentAPI.getStatus();
    return response.data;
  }
);

const initialState = {
  status: {},
  loading: false,
  error: null,
};

const agentSlice = createSlice({
  name: 'agents',
  initialState,
  reducers: {
    updateAgentStatus: (state, action) => {
      state.status = { ...state.status, ...action.payload };
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchAgentStatus.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchAgentStatus.fulfilled, (state, action) => {
        state.loading = false;
        state.status = action.payload.data || {};
      })
      .addCase(fetchAgentStatus.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});

export const { updateAgentStatus } = agentSlice.actions;
export default agentSlice.reducer;