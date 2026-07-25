import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import {
  ArrowBack,
  Download,
  Share,
  MoreVert,
} from '@mui/icons-material';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Button,
  IconButton,
  Chip,
  Divider,
  CircularProgress,
  Tab,
  Tabs,
  Alert,
} from '@mui/material';
import toast from 'react-hot-toast';

import { fetchLeadById, clearCurrentLead, processLead } from '../store/leadSlice';
import LeadScoring from '../components/leads/LeadScoring';
import CompanyIntelligence from '../components/analysis/CompanyIntelligence';
import PainPointAnalysis from '../components/analysis/PainPointAnalysis';
import CaseStudyMatcher from '../components/analysis/CaseStudyMatcher';
import EmailGenerator from '../components/outreach/EmailGenerator';
import { api } from '../api/client';

const LeadView = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { currentLead, loading } = useSelector((state) => state.leads);
  const [activeTab, setActiveTab] = useState(0);
  const [processing, setProcessing] = useState(false);

  useEffect(() => {
    loadLead();
    return () => {
      dispatch(clearCurrentLead());
    };
  }, [id]);

  const loadLead = async () => {
    try {
      await dispatch(fetchLeadById(id)).unwrap();
    } catch (error) {
      toast.error('Failed to load lead details');
      navigate('/dashboard');
    }
  };

  const handleProcessLead = async () => {
    setProcessing(true);
    try {
      await dispatch(processLead(id)).unwrap();
      toast.success('Lead processing started');
      setTimeout(() => loadLead(), 3000);
    } catch (error) {
      toast.error('Failed to process lead');
    } finally {
      setProcessing(false);
    }
  };

  const handleExportSummary = async () => {
    try {
      const response = await api.get(`/leads/${id}/export`);
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      window.open(url);
    } catch (error) {
      toast.error('Failed to export summary');
    }
  };

  if (loading || !currentLead) {
    return (
      <Box className="flex justify-center items-center h-96">
        <CircularProgress />
      </Box>
    );
  }

  const score = currentLead.meddpicc_score?.total_score || 0;
  const isQualified = score >= 60;

  return (
    <Box className="space-y-6">
      {/* Header */}
      <Box className="flex justify-between items-start">
        <Box>
          <Button
            startIcon={<ArrowBack />}
            onClick={() => navigate('/dashboard')}
            className="text-gray-600 mb-2"
          >
            Back to Dashboard
          </Button>
          <Typography variant="h4" className="font-bold">
            {currentLead.first_name} {currentLead.last_name}
          </Typography>
          <Typography variant="body2" className="text-gray-500">
            {currentLead.company_name} • {currentLead.job_title || 'Unknown Role'}
          </Typography>
        </Box>
        <Box className="flex space-x-2">
          <Button
            variant="contained"
            color="primary"
            onClick={handleProcessLead}
            disabled={processing}
            className="normal-case"
          >
            {processing ? <CircularProgress size={24} /> : 'Process Lead'}
          </Button>
          <Button
            variant="outlined"
            startIcon={<Download />}
            onClick={handleExportSummary}
            className="normal-case"
          >
            Export
          </Button>
          <IconButton>
            <MoreVert />
          </IconButton>
        </Box>
      </Box>

      {/* Status Badges */}
      <Box className="flex flex-wrap gap-2">
        <Chip
          label={`Score: ${score}/100`}
          color={isQualified ? 'success' : 'warning'}
          className="font-medium"
        />
        <Chip
          label={`Status: ${currentLead.status || 'Pending'}`}
          color={currentLead.status === 'qualified' ? 'success' : 'default'}
        />
        {currentLead.recommended_motion && (
          <Chip
            label={`Motion: ${currentLead.recommended_motion.replace('_', ' ')}`}
            color="primary"
            variant="outlined"
          />
        )}
        {currentLead.industry && (
          <Chip label={`Industry: ${currentLead.industry}`} variant="outlined" />
        )}
      </Box>

      {/* Quick Stats */}
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <Paper className="p-4 rounded-xl shadow-sm">
            <Typography variant="caption" className="text-gray-500">Employee Count</Typography>
            <Typography variant="h6">{currentLead.company_data?.employee_count || 'N/A'}</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper className="p-4 rounded-xl shadow-sm">
            <Typography variant="caption" className="text-gray-500">Funding Stage</Typography>
            <Typography variant="h6">{currentLead.company_data?.funding_stage || 'N/A'}</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper className="p-4 rounded-xl shadow-sm">
            <Typography variant="caption" className="text-gray-500">Decision Makers</Typography>
            <Typography variant="h6">{currentLead.decision_makers?.length || 0}</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper className="p-4 rounded-xl shadow-sm">
            <Typography variant="caption" className="text-gray-500">Pain Points</Typography>
            <Typography variant="h6">{currentLead.pain_points?.length || 0}</Typography>
          </Paper>
        </Grid>
      </Grid>

      {/* Tabs */}
      <Paper className="rounded-xl shadow-sm">
        <Tabs
          value={activeTab}
          onChange={(e, newValue) => setActiveTab(newValue)}
          variant="scrollable"
          scrollButtons="auto"
          className="border-b"
        >
          <Tab label="Overview" />
          <Tab label="MEDDPICC Scoring" />
          <Tab label="Company Intelligence" />
          <Tab label="Pain Points" />
          <Tab label="Case Study" />
          <Tab label="Outreach" />
        </Tabs>

        <Box className="p-6">
          {activeTab === 0 && (
            <Grid container spacing={4}>
              <Grid item xs={12} md={6}>
                <Paper variant="outlined" className="p-4">
                  <Typography variant="h6" className="mb-3">
                    Lead Information
                  </Typography>
                  <div className="space-y-2">
                    <InfoRow label="Email" value={currentLead.email} />
                    <InfoRow label="Phone" value={currentLead.phone || 'N/A'} />
                    <InfoRow label="Company" value={currentLead.company_name} />
                    <InfoRow label="Industry" value={currentLead.industry || 'N/A'} />
                    <InfoRow label="Source" value={currentLead.source} />
                    <InfoRow label="Received" value={new Date(currentLead.created_at).toLocaleDateString()} />
                    {currentLead.processed_at && (
                      <InfoRow label="Processed" value={new Date(currentLead.processed_at).toLocaleDateString()} />
                    )}
                  </div>
                </Paper>
              </Grid>
              <Grid item xs={12} md={6}>
                <Paper variant="outlined" className="p-4">
                  <Typography variant="h6" className="mb-3">
                    Lead Message
                  </Typography>
                  <Typography variant="body2" className="text-gray-700 bg-gray-50 p-4 rounded-lg min-h-[100px]">
                    {currentLead.message || 'No message provided'}
                  </Typography>
                </Paper>
              </Grid>
            </Grid>
          )}
          {activeTab === 1 && <LeadScoring scoring={currentLead.meddpicc_score} />}
          {activeTab === 2 && <CompanyIntelligence company={currentLead.company_data} />}
          {activeTab === 3 && <PainPointAnalysis painPoints={currentLead.pain_points} opportunities={currentLead.opportunities} />}
          {activeTab === 4 && <CaseStudyMatcher caseStudy={currentLead.matched_case_study} />}
          {activeTab === 5 && <EmailGenerator emails={currentLead.personalized_emails} linkedin={currentLead.linkedin_message} />}
        </Box>
      </Paper>
    </Box>
  );
};

const InfoRow = ({ label, value }) => (
  <Box className="flex justify-between py-2 border-b border-gray-100">
    <Typography variant="body2" className="text-gray-500">
      {label}
    </Typography>
    <Typography variant="body2" className="font-medium">
      {value}
    </Typography>
  </Box>
);

export default LeadView;