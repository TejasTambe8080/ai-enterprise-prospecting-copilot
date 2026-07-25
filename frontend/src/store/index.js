import { configureStore } from '@reduxjs/toolkit';
import leadReducer from './leadSlice';
import agentReducer from './agentSlice';

export const store = configureStore({
  reducer: {
    leads: leadReducer,
    agents: agentReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false,
    }),
});