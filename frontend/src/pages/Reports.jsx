import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from '@mui/material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';

const Reports = () => {
  const [timeRange, setTimeRange] = useState('30d');
  const [leadData, setLeadData] = useState([]);
  const [statusData, setStatusData] = useState([]);
  const [scoreData, setScoreData] = useState([]);

  useEffect(() => {
    generateReportData();
  }, [timeRange]);

  const generateReportData = () => {
    // Generate sample data (would come from API in production)
    const leads = [];
    const statuses = { qualified: 45, pending: 30, processing: 15, disqualified: 10 };
    const scores = [
      { range: '0-20', count: 5 },
      { range: '21-40', count: 12 },
      { range: '41-60', count: 25 },
      { range: '61-80', count: 30 },
      { range: '81-100', count: 18 },
    ];

    for (let i = 0; i < 30; i++) {
      const date = new Date();
      date.setDate(date.getDate() - i);
      leads.push({
        date: date.toLocaleDateString(),
        leads: Math.floor(Math.random() * 10) + 2,
        qualified: Math.floor(Math.random() * 6) + 1,
      });
    }

    setLeadData(leads.reverse());
    setStatusData(Object.entries(statuses).map(([name, value]) => ({ name, value })));
    setScoreData(scores);
  };

  const COLORS = ['#6366f1', '#22c55e', '#f59e0b', '#ef4444', '#8b5cf6'];

  return (
    <Box className="space-y-6">
      <Box className="flex justify-between items-center">
        <Typography variant="h4" className="font-bold text-gray-800">
          Reports & Analytics
        </Typography>
        <FormControl sx={{ minWidth: 150 }}>
          <InputLabel>Time Range</InputLabel>
          <Select value={timeRange} onChange={(e) => setTimeRange(e.target.value)} label="Time Range">
            <MenuItem value="7d">Last 7 Days</MenuItem>
            <MenuItem value="30d">Last 30 Days</MenuItem>
            <MenuItem value="90d">Last 90 Days</MenuItem>
          </Select>
        </FormControl>
      </Box>

      <Grid container spacing={4}>
        <Grid item xs={12} lg={8}>
          <Paper className="p-6 rounded-xl shadow-sm">
            <Typography variant="h6" className="mb-4 font-semibold">
              Lead Activity Over Time
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={leadData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="leads" fill="#6366f1" name="Total Leads" />
                <Bar dataKey="qualified" fill="#22c55e" name="Qualified" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        <Grid item xs={12} lg={4}>
          <Paper className="p-6 rounded-xl shadow-sm">
            <Typography variant="h6" className="mb-4 font-semibold">
              Lead Status Distribution
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={statusData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {statusData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper className="p-6 rounded-xl shadow-sm">
            <Typography variant="h6" className="mb-4 font-semibold">
              Score Distribution
            </Typography>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={scoreData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="range" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#8b5cf6" name="Number of Leads" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Reports;