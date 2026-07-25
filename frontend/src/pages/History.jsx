import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  IconButton,
  TextField,
  InputAdornment,
} from '@mui/material';
import { Search, FilterList, Visibility } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { formatDistanceToNow } from 'date-fns';

const History = () => {
  const navigate = useNavigate();
  const [logs, setLogs] = useState([]);
  const [search, setSearch] = useState('');

  useEffect(() => {
    // In production, fetch from API
    generateSampleLogs();
  }, []);

  const generateSampleLogs = () => {
    const sampleLogs = [];
    for (let i = 0; i < 20; i++) {
      const date = new Date();
      date.setHours(date.getHours() - i);
      sampleLogs.push({
        id: `log-${i}`,
        leadName: `Lead ${i + 1}`,
        action: ['Processed', 'Qualified', 'Email Sent', 'Disqualified', 'Scored'][i % 5],
        status: ['success', 'success', 'success', 'error', 'success'][i % 5],
        timestamp: date.toISOString(),
        details: `Processed lead with score ${Math.floor(Math.random() * 100)}`,
      });
    }
    setLogs(sampleLogs);
  };

  const filteredLogs = logs.filter((log) =>
    log.leadName.toLowerCase().includes(search.toLowerCase()) ||
    log.action.toLowerCase().includes(search.toLowerCase())
  );

  const getStatusChip = (status) => {
    const config = {
      success: { color: 'success', label: 'Success' },
      error: { color: 'error', label: 'Error' },
    };
    const { color, label } = config[status] || config.success;
    return <Chip size="small" label={label} color={color} />;
  };

  return (
    <Box className="space-y-6">
      <Box className="flex justify-between items-center">
        <Typography variant="h4" className="font-bold text-gray-800">
          Activity History
        </Typography>
        <TextField
          placeholder="Search logs..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          size="small"
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <Search />
              </InputAdornment>
            ),
          }}
          className="w-64"
        />
      </Box>

      <Paper className="rounded-xl shadow-sm">
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow className="bg-gray-50">
                <TableCell className="font-semibold">Lead</TableCell>
                <TableCell className="font-semibold">Action</TableCell>
                <TableCell className="font-semibold">Status</TableCell>
                <TableCell className="font-semibold">Time</TableCell>
                <TableCell className="font-semibold">Details</TableCell>
                <TableCell className="font-semibold text-right">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredLogs.map((log) => (
                <TableRow key={log.id} className="hover:bg-gray-50">
                  <TableCell className="font-medium">{log.leadName}</TableCell>
                  <TableCell>{log.action}</TableCell>
                  <TableCell>{getStatusChip(log.status)}</TableCell>
                  <TableCell>{formatDistanceToNow(new Date(log.timestamp), { addSuffix: true })}</TableCell>
                  <TableCell>{log.details}</TableCell>
                  <TableCell align="right">
                    <IconButton size="small" className="text-primary-600">
                      <Visibility fontSize="small" />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
              {filteredLogs.length === 0 && (
                <TableRow>
                  <TableCell colSpan={6} className="text-center py-8 text-gray-500">
                    No logs found
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Box>
  );
};

export default History;