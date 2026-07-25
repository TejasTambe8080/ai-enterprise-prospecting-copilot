import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Grid, Paper, Typography, Box, Button } from '@mui/material';
import { Refresh } from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import toast from 'react-hot-toast';

import { fetchLeads } from '../store/leadSlice';
import StatsCards from '../components/dashboard/StatsCards';
import LeadTable from '../components/dashboard/LeadTable';
import AgentStatus from '../components/dashboard/AgentStatus';

const Dashboard = () => {
  const dispatch = useDispatch();
  const { leads, stats, loading } = useSelector((state) => state.leads);
  const [chartData, setChartData] = React.useState([]);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      await dispatch(fetchLeads({ limit: 20 })).unwrap();
      generateChartData();
    } catch (error) {
      toast.error('Failed to load dashboard data');
    }
  };

  const generateChartData = () => {
    const data = [];
    for (let i = 6; i >= 0; i--) {
      const date = new Date();
      date.setDate(date.getDate() - i);
      data.push({
        date: date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
        leads: Math.floor(Math.random() * 20) + 5,
        qualified: Math.floor(Math.random() * 10) + 2,
      });
    }
    setChartData(data);
  };

  const handleRefresh = () => {
    loadDashboardData();
    toast.success('Dashboard refreshed');
  };

  return (
    <Box className="space-y-6">
      <Box className="flex justify-between items-center">
        <Box>
          <Typography variant="h4" className="font-bold text-gray-800">
            Dashboard
          </Typography>
          <Typography variant="body2" className="text-gray-500">
            Real-time inbound lead intelligence
          </Typography>
        </Box>
        <Button
          variant="outlined"
          startIcon={<Refresh />}
          onClick={handleRefresh}
          className="normal-case"
        >
          Refresh
        </Button>
      </Box>

      <StatsCards stats={stats} />

      <Grid container spacing={4}>
        <Grid item xs={12} lg={8}>
          <Paper className="p-6 rounded-xl shadow-sm">
            <Typography variant="h6" className="mb-4 font-semibold">
              Lead Activity (7 Days)
            </Typography>
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={chartData}>
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="leads"
                  stroke="#6366f1"
                  strokeWidth={2}
                  dot={false}
                />
                <Line
                  type="monotone"
                  dataKey="qualified"
                  stroke="#22c55e"
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
        <Grid item xs={12} lg={4}>
          <Paper className="p-6 rounded-xl shadow-sm h-full">
            <Typography variant="h6" className="mb-4 font-semibold">
              Agent Status
            </Typography>
            <AgentStatus />
          </Paper>
        </Grid>
      </Grid>

      <Paper className="p-6 rounded-xl shadow-sm">
        <Box className="flex justify-between items-center mb-4">
          <Typography variant="h6" className="font-semibold">
            Recent Leads
          </Typography>
        </Box>
        <LeadTable leads={leads} loading={loading} />
      </Paper>
    </Box>
  );
};

export default Dashboard;