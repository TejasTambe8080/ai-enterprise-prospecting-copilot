import React from 'react';
import { Box, Typography, Paper, Grid, Chip } from '@mui/material';
import { Business, People, AttachMoney, LocationOn, CalendarToday } from '@mui/icons-material';

const CompanyIntelligence = ({ company }) => {
  if (!company || Object.keys(company).length === 0) {
    return (
      <Box className="text-center py-8">
        <Typography variant="body1" className="text-gray-500">
          No company intelligence data available
        </Typography>
      </Box>
    );
  }

  const InfoCard = ({ icon: Icon, label, value }) => (
    <Paper variant="outlined" className="p-4">
      <Box className="flex items-start gap-3">
        <Icon className="text-primary-600" />
        <Box>
          <Typography variant="caption" className="text-gray-500">
            {label}
          </Typography>
          <Typography variant="body1" className="font-medium">
            {value || 'N/A'}
          </Typography>
        </Box>
      </Box>
    </Paper>
  );

  return (
    <Box className="space-y-6">
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <InfoCard icon={Business} label="Company Name" value={company.company_name} />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <InfoCard icon={People} label="Employee Count" value={company.employee_count} />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <InfoCard icon={AttachMoney} label="Funding Stage" value={company.funding_stage} />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <InfoCard icon={CalendarToday} label="Founded" value={company.founded_year} />
        </Grid>
      </Grid>

      {company.description && (
        <Paper variant="outlined" className="p-4">
          <Typography variant="subtitle2" className="text-gray-500 mb-2">
            Company Description
          </Typography>
          <Typography variant="body2">{company.description}</Typography>
        </Paper>
      )}

      {company.technologies && company.technologies.length > 0 && (
        <Paper variant="outlined" className="p-4">
          <Typography variant="subtitle2" className="text-gray-500 mb-2">
            Technology Stack
          </Typography>
          <Box className="flex flex-wrap gap-2">
            {company.technologies.map((tech, idx) => (
              <Chip key={idx} label={tech} size="small" variant="outlined" />
            ))}
          </Box>
        </Paper>
      )}

      {company.competitors && company.competitors.length > 0 && (
        <Paper variant="outlined" className="p-4">
          <Typography variant="subtitle2" className="text-gray-500 mb-2">
            Competitors
          </Typography>
          <Box className="flex flex-wrap gap-2">
            {company.competitors.map((comp, idx) => (
              <Chip key={idx} label={comp} size="small" color="warning" variant="outlined" />
            ))}
          </Box>
        </Paper>
      )}

      {company.recent_news && company.recent_news.length > 0 && (
        <Paper variant="outlined" className="p-4">
          <Typography variant="subtitle2" className="text-gray-500 mb-2">
            Recent News
          </Typography>
          <Box className="space-y-2">
            {company.recent_news.slice(0, 3).map((news, idx) => (
              <Box key={idx} className="border-b border-gray-100 pb-2">
                <Typography variant="body2" className="font-medium">
                  {news.title}
                </Typography>
                <Typography variant="caption" className="text-gray-500">
                  {news.source} • {news.date}
                </Typography>
              </Box>
            ))}
          </Box>
        </Paper>
      )}
    </Box>
  );
};

export default CompanyIntelligence;