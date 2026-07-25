import React from 'react';
import { Box, Typography, Paper, Grid, Chip, Divider } from '@mui/material';
import { Email, Phone, Business, Person, CalendarToday, LocationOn } from '@mui/icons-material';
import { formatDistanceToNow } from 'date-fns';

const LeadDetails = ({ lead }) => {
  if (!lead) {
    return (
      <Box className="text-center py-8">
        <Typography variant="body1" className="text-gray-500">
          No lead data available
        </Typography>
      </Box>
    );
  }

  const InfoItem = ({ icon: Icon, label, value }) => (
    <Box className="flex items-start gap-3 py-2 border-b border-gray-100">
      <Icon className="text-gray-400 text-sm mt-0.5" />
      <Box>
        <Typography variant="caption" className="text-gray-500">
          {label}
        </Typography>
        <Typography variant="body2" className="font-medium">
          {value || 'N/A'}
        </Typography>
      </Box>
    </Box>
  );

  return (
    <Paper variant="outlined" className="p-6">
      <Typography variant="h6" className="font-semibold mb-4">
        Lead Information
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <InfoItem icon={Person} label="Full Name" value={`${lead.first_name} ${lead.last_name}`} />
          <InfoItem icon={Email} label="Email" value={lead.email} />
          <InfoItem icon={Phone} label="Phone" value={lead.phone} />
          <InfoItem icon={Business} label="Job Title" value={lead.job_title} />
        </Grid>
        <Grid item xs={12} md={6}>
          <InfoItem icon={Business} label="Company" value={lead.company_name} />
          <InfoItem icon={LocationOn} label="Industry" value={lead.industry} />
          <InfoItem icon={CalendarToday} label="Received" value={formatDistanceToNow(new Date(lead.created_at), { addSuffix: true })} />
          <InfoItem icon={CalendarToday} label="Status" value={lead.status} />
        </Grid>
      </Grid>
      
      {lead.message && (
        <>
          <Divider className="my-4" />
          <Box className="mt-4">
            <Typography variant="subtitle2" className="text-gray-500 mb-2">
              Message
            </Typography>
            <Paper variant="outlined" className="p-4 bg-gray-50">
              <Typography variant="body2">{lead.message}</Typography>
            </Paper>
          </Box>
        </>
      )}
    </Paper>
  );
};

export default LeadDetails;