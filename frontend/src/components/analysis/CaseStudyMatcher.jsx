import React from 'react';
import { Box, Typography, Paper, Chip, Button } from '@mui/material';
import { CheckCircle, TrendingUp, People } from '@mui/icons-material';

const CaseStudyMatcher = ({ caseStudy }) => {
  if (!caseStudy || Object.keys(caseStudy).length === 0) {
    return (
      <Box className="text-center py-8">
        <Typography variant="body1" className="text-gray-500">
          No case study matched
        </Typography>
      </Box>
    );
  }

  return (
    <Paper variant="outlined" className="p-6">
      <Box className="flex justify-between items-start mb-4">
        <Box>
          <Typography variant="h6" className="font-semibold">
            {caseStudy.title}
          </Typography>
          <Box className="flex items-center gap-2 mt-1">
            <Chip
              size="small"
              label={`Match Score: ${caseStudy.match_score || 0}%`}
              color={caseStudy.match_score >= 80 ? 'success' : 'warning'}
            />
            {caseStudy.industry && (
              <Chip size="small" label={caseStudy.industry} variant="outlined" />
            )}
          </Box>
        </Box>
        <Button variant="outlined" size="small" color="primary">
          View Full Case Study
        </Button>
      </Box>

      <Typography variant="body2" className="text-gray-600 mb-4">
        {caseStudy.description}
      </Typography>

      {caseStudy.results && caseStudy.results.length > 0 && (
        <Box className="bg-green-50 p-4 rounded-lg mb-4">
          <Typography variant="subtitle2" className="text-green-700 font-semibold mb-2">
            Key Results
          </Typography>
          <Box className="flex flex-wrap gap-4">
            {caseStudy.results.map((result, idx) => (
              <Box key={idx} className="flex items-center gap-1">
                <CheckCircle className="text-green-500" fontSize="small" />
                <Typography variant="body2" className="text-green-700">
                  {result}
                </Typography>
              </Box>
            ))}
          </Box>
        </Box>
      )}

      {caseStudy.tags && caseStudy.tags.length > 0 && (
        <Box className="flex flex-wrap gap-2">
          {caseStudy.tags.map((tag, idx) => (
            <Chip key={idx} label={tag} size="small" variant="outlined" />
          ))}
        </Box>
      )}

      {caseStudy.reasoning && (
        <Box className="mt-4 bg-blue-50 p-4 rounded-lg">
          <Typography variant="subtitle2" className="text-blue-700 font-semibold">
            Why This Case Study
          </Typography>
          <Typography variant="body2" className="text-blue-600">
            {caseStudy.reasoning}
          </Typography>
        </Box>
      )}
    </Paper>
  );
};

export default CaseStudyMatcher;