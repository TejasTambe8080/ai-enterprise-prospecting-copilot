import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Box, Typography, Chip, CircularProgress } from '@mui/material';
import { CheckCircle, ErrorOutline, Schedule, RadioButtonUnchecked } from '@mui/icons-material';
import { fetchAgentStatus } from '../../store/agentSlice';

const AgentStatus = () => {
  const dispatch = useDispatch();
  const { status, loading } = useSelector((state) => state.agents);

  useEffect(() => {
    dispatch(fetchAgentStatus());
    const interval = setInterval(() => {
      dispatch(fetchAgentStatus());
    }, 30000);
    return () => clearInterval(interval);
  }, [dispatch]);

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
      case 'success':
        return <CheckCircle className="text-green-500" fontSize="small" />;
      case 'running':
        return <CircularProgress size={16} className="text-blue-500" />;
      case 'error':
        return <ErrorOutline className="text-red-500" fontSize="small" />;
      default:
        return <RadioButtonUnchecked className="text-gray-300" fontSize="small" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
      case 'success':
        return 'success';
      case 'running':
        return 'info';
      case 'error':
        return 'error';
      default:
        return 'default';
    }
  };

  if (loading) {
    return (
      <Box className="flex justify-center items-center h-32">
        <CircularProgress size={24} />
      </Box>
    );
  }

  const agentList = Object.entries(status);
  if (agentList.length === 0) {
    return (
      <Typography variant="body2" className="text-gray-500 text-center py-4">
        No agents available
      </Typography>
    );
  }

  return (
    <Box className="space-y-2">
      {agentList.map(([name, agentStatus]) => (
        <Box key={name} className="flex items-center justify-between py-2 border-b border-gray-100">
          <Box className="flex items-center gap-2">
            {getStatusIcon(agentStatus)}
            <Typography variant="body2" className="font-medium capitalize">
              {name.replace('_', ' ')}
            </Typography>
          </Box>
          <Chip
            size="small"
            label={agentStatus}
            color={getStatusColor(agentStatus)}
            className="text-xs"
          />
        </Box>
      ))}
    </Box>
  );
};

export default AgentStatus;