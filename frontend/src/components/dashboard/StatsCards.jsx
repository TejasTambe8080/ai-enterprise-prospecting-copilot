import React from 'react';
import { Grid, Paper, Typography, Box } from '@mui/material';
import {
  People as PeopleIcon,
  CheckCircle as CheckCircleIcon,
  Schedule as ScheduleIcon,
  TrendingUp as TrendingUpIcon,
} from '@mui/icons-material';

const StatCard = ({ title, value, icon: Icon, color, subtitle }) => {
  return (
    <Paper className="p-6 rounded-xl shadow-sm card-hover">
      <Box className="flex items-center justify-between">
        <Box>
          <Typography variant="h4" className="font-bold">
            {value}
          </Typography>
          <Typography variant="body2" className="text-gray-500 mt-1">
            {title}
          </Typography>
          {subtitle && (
            <Typography variant="caption" className="text-gray-400">
              {subtitle}
            </Typography>
          )}
        </Box>
        <Box className={`p-3 rounded-full bg-${color}-50`}>
          <Icon className={`text-${color}-600`} />
        </Box>
      </Box>
    </Paper>
  );
};

const StatsCards = ({ stats }) => {
  const cards = [
    {
      title: 'Total Leads',
      value: stats.total || 0,
      icon: PeopleIcon,
      color: 'primary',
    },
    {
      title: 'Qualified',
      value: stats.qualified || 0,
      icon: CheckCircleIcon,
      color: 'success',
      subtitle: `${stats.qualified && stats.total ? Math.round((stats.qualified / stats.total) * 100) : 0}% conversion`,
    },
    {
      title: 'Processing',
      value: stats.processing || 0,
      icon: ScheduleIcon,
      color: 'warning',
    },
    {
      title: 'Avg Score',
      value: stats.avgScore || 0,
      icon: TrendingUpIcon,
      color: 'secondary',
      subtitle: 'MEDDPICC average',
    },
  ];

  return (
    <Grid container spacing={4}>
      {cards.map((card, index) => (
        <Grid item xs={12} sm={6} lg={3} key={index}>
          <StatCard {...card} />
        </Grid>
      ))}
    </Grid>
  );
};

export default StatsCards;