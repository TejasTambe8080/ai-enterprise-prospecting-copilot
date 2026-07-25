import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  IconButton,
  Skeleton,
  Box,
  Typography,
} from '@mui/material';
import { Visibility, Mail, CheckCircle, Schedule, ErrorOutline } from '@mui/icons-material';
import { formatDistanceToNow } from 'date-fns';

const LeadTable = ({ leads = [], loading = false }) => {
  const navigate = useNavigate();

  const getStatusChip = (status) => {
    const config = {
      qualified: { color: 'success', icon: <CheckCircle className="w-3 h-3" /> },
      pending: { color: 'warning', icon: <Schedule className="w-3 h-3" /> },
      processing: { color: 'info', icon: <Schedule className="w-3 h-3 animate-pulse" /> },
      error: { color: 'error', icon: <ErrorOutline className="w-3 h-3" /> },
    };
    const { color, icon } = config[status] || config.pending;
    return (
      <Chip
        size="small"
        label={status?.charAt(0).toUpperCase() + status?.slice(1) || 'Unknown'}
        color={color}
        icon={icon}
        className="font-medium"
      />
    );
  };

  if (loading) {
    return (
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              {['Lead', 'Company', 'Score', 'Status', 'Actions'].map((col) => (
                <TableCell key={col}>
                  <Skeleton variant="text" width={80} />
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {[1, 2, 3, 4, 5].map((i) => (
              <TableRow key={i}>
                {[1, 2, 3, 4, 5].map((j) => (
                  <TableCell key={j}>
                    <Skeleton variant="text" width={100} />
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    );
  }

  if (!leads || leads.length === 0) {
    return (
      <Box className="text-center py-12">
        <Typography variant="body1" className="text-gray-500">
          No leads found. New leads will appear here.
        </Typography>
      </Box>
    );
  }

  return (
    <TableContainer>
      <Table>
        <TableHead>
          <TableRow className="bg-gray-50">
            <TableCell className="font-semibold">Lead</TableCell>
            <TableCell className="font-semibold">Company</TableCell>
            <TableCell className="font-semibold">Score</TableCell>
            <TableCell className="font-semibold">Status</TableCell>
            <TableCell className="font-semibold text-right">Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {leads.map((lead) => (
            <TableRow
              key={lead.id}
              className="hover:bg-gray-50 cursor-pointer"
              onClick={() => navigate(`/leads/${lead.id}`)}
            >
              <TableCell>
                <div className="flex flex-col">
                  <span className="font-medium text-gray-900">
                    {lead.first_name} {lead.last_name}
                  </span>
                  <span className="text-sm text-gray-500">{lead.email}</span>
                </div>
              </TableCell>
              <TableCell>
                <div className="flex flex-col">
                  <span className="font-medium">{lead.company_name}</span>
                  <span className="text-sm text-gray-500">{lead.industry || 'N/A'}</span>
                </div>
              </TableCell>
              <TableCell>
                <div className="flex items-center space-x-2">
                  <span className={`text-lg font-bold ${
                    lead.meddpicc_score?.total_score >= 70 ? 'text-green-600' :
                    lead.meddpicc_score?.total_score >= 40 ? 'text-yellow-600' :
                    'text-red-600'
                  }`}>
                    {lead.meddpicc_score?.total_score || 0}
                  </span>
                  <span className="text-xs text-gray-400">/100</span>
                </div>
              </TableCell>
              <TableCell>{getStatusChip(lead.status)}</TableCell>
              <TableCell align="right">
                <div className="flex justify-end space-x-2">
                  <IconButton
                    size="small"
                    onClick={(e) => {
                      e.stopPropagation();
                      navigate(`/leads/${lead.id}`);
                    }}
                    className="text-primary-600"
                  >
                    <Visibility fontSize="small" />
                  </IconButton>
                  <IconButton
                    size="small"
                    onClick={(e) => {
                      e.stopPropagation();
                      // Open email composer
                    }}
                    className="text-gray-600"
                  >
                    <Mail fontSize="small" />
                  </IconButton>
                </div>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default LeadTable;