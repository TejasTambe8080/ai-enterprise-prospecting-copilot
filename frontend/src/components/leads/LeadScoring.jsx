import React from 'react';
import { Box, Typography, Paper, Grid, LinearProgress } from '@mui/material';

const LeadScoring = ({ scoring }) => {
  if (!scoring) {
    return (
      <Box className="text-center py-8">
        <Typography variant="body1" className="text-gray-500">
          No scoring data available
        </Typography>
      </Box>
    );
  }

  const dimensions = [
    { key: 'metrics', label: 'Metrics', weight: '20%' },
    { key: 'economic_buyer', label: 'Economic Buyer', weight: '15%' },
    { key: 'decision_criteria', label: 'Decision Criteria', weight: '15%' },
    { key: 'decision_process', label: 'Decision Process', weight: '15%' },
    { key: 'paper_process', label: 'Paper Process', weight: '10%' },
    { key: 'internal_champion', label: 'Internal Champion', weight: '15%' },
    { key: 'competition', label: 'Competition', weight: '10%' },
  ];

  const getColor = (value) => {
    if (value >= 70) return '#22c55e';
    if (value >= 50) return '#f59e0b';
    return '#ef4444';
  };

  return (
    <Box className="space-y-6">
      <Grid container spacing={4}>
        <Grid item xs={12} md={8}>
          <Paper variant="outlined" className="p-6">
            <Typography variant="h6" className="mb-4 font-semibold">
              MEDDPICC Score Breakdown
            </Typography>
            <Box className="space-y-4">
              {dimensions.map((dim) => (
                <Box key={dim.key}>
                  <Box className="flex justify-between mb-1">
                    <Typography variant="body2" className="text-gray-600">
                      {dim.label}
                      <span className="text-gray-400 text-xs ml-1">({dim.weight})</span>
                    </Typography>
                    <Typography variant="body2" className="font-medium">
                      {scoring[dim.key] || 0}/100
                    </Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={scoring[dim.key] || 0}
                    sx={{
                      height: 8,
                      borderRadius: 4,
                      backgroundColor: '#f3f4f6',
                      '& .MuiLinearProgress-bar': {
                        backgroundColor: getColor(scoring[dim.key] || 0),
                        borderRadius: 4,
                      },
                    }}
                  />
                </Box>
              ))}
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper variant="outlined" className="p-6">
            <Typography variant="h6" className="mb-4 font-semibold">
              Score Summary
            </Typography>
            <Box className="text-center">
              <Box className="relative inline-flex">
                <svg className="w-32 h-32" viewBox="0 0 100 100">
                  <circle
                    className="text-gray-200"
                    strokeWidth="8"
                    stroke="currentColor"
                    fill="transparent"
                    r="44"
                    cx="50"
                    cy="50"
                  />
                  <circle
                    className="text-primary-600"
                    strokeWidth="8"
                    strokeLinecap="round"
                    stroke="currentColor"
                    fill="transparent"
                    r="44"
                    cx="50"
                    cy="50"
                    strokeDasharray={`${scoring.total_score * 2.76} 276`}
                    strokeDashoffset="0"
                    style={{ transition: 'stroke-dasharray 0.5s ease' }}
                  />
                </svg>
                <Box className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
                  <Typography variant="h4" className="font-bold">
                    {scoring.total_score || 0}
                  </Typography>
                  <Typography variant="caption" className="text-gray-500">
                    Total Score
                  </Typography>
                </Box>
              </Box>
            </Box>

            <Box className="mt-6 space-y-2">
              <Typography variant="body2" className="text-gray-600">
                Qualification: <span className="font-medium">{scoring.qualification || 'Unknown'}</span>
              </Typography>
              <Typography variant="body2" className="text-gray-600">
                Motion: <span className="font-medium">{scoring.recommended_motion?.replace('_', ' ') || 'Not set'}</span>
              </Typography>
            </Box>

            {scoring.strengths && scoring.strengths.length > 0 && (
              <Box className="mt-4">
                <Typography variant="body2" className="text-green-600 font-medium">
                  Strengths:
                </Typography>
                <ul className="text-sm text-gray-600 list-disc pl-4 mt-1">
                  {scoring.strengths.slice(0, 3).map((strength, idx) => (
                    <li key={idx}>{strength}</li>
                  ))}
                </ul>
              </Box>
            )}

            {scoring.risks && scoring.risks.length > 0 && (
              <Box className="mt-3">
                <Typography variant="body2" className="text-red-600 font-medium">
                  Risks:
                </Typography>
                <ul className="text-sm text-gray-600 list-disc pl-4 mt-1">
                  {scoring.risks.slice(0, 3).map((risk, idx) => (
                    <li key={idx}>{risk}</li>
                  ))}
                </ul>
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default LeadScoring;