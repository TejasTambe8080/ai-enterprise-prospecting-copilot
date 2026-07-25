import React from 'react';
import { Box, Typography, Paper, Timeline, TimelineItem, TimelineSeparator, TimelineConnector, TimelineContent, TimelineDot } from '@mui/lab';
import { CheckCircle, Schedule, ErrorOutline, Pending } from '@mui/icons-material';
import { formatDistanceToNow } from 'date-fns';

const LeadTimeline = ({ logs = [] }) => {
  if (!logs || logs.length === 0) {
    return (
      <Box className="text-center py-8">
        <Typography variant="body1" className="text-gray-500">
          No timeline events available
        </Typography>
      </Box>
    );
  }

  const getIcon = (status) => {
    switch (status) {
      case 'success':
      case 'completed':
        return <CheckCircle className="text-green-500" />;
      case 'running':
      case 'processing':
        return <Schedule className="text-blue-500 animate-pulse" />;
      case 'error':
        return <ErrorOutline className="text-red-500" />;
      default:
        return <Pending className="text-gray-400" />;
    }
  };

  const getColor = (status) => {
    switch (status) {
      case 'success':
      case 'completed':
        return 'success';
      case 'running':
      case 'processing':
        return 'info';
      case 'error':
        return 'error';
      default:
        return 'grey';
    }
  };

  return (
    <Paper variant="outlined" className="p-6">
      <Typography variant="h6" className="font-semibold mb-4">
        Activity Timeline
      </Typography>
      <Timeline position="right">
        {logs.map((log, index) => (
          <TimelineItem key={index}>
            <TimelineSeparator>
              <TimelineDot color={getColor(log.status)}>
                {getIcon(log.status)}
              </TimelineDot>
              {index < logs.length - 1 && <TimelineConnector />}
            </TimelineSeparator>
            <TimelineContent>
              <Typography variant="body2" className="font-medium">
                {log.agent_name || 'System'}
              </Typography>
              <Typography variant="caption" className="text-gray-500">
                {log.action || log.status || 'Event'}
              </Typography>
              {log.timestamp && (
                <Typography variant="caption" className="text-gray-400 block">
                  {formatDistanceToNow(new Date(log.timestamp), { addSuffix: true })}
                </Typography>
              )}
              {log.details && (
                <Typography variant="caption" className="text-gray-600 block mt-1">
                  {log.details}
                </Typography>
              )}
            </TimelineContent>
          </TimelineItem>
        ))}
      </Timeline>
    </Paper>
  );
};

export default LeadTimeline;