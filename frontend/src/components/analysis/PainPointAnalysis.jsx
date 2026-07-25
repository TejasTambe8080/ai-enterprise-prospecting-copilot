import React from 'react';
import { Box, Typography, Paper, Chip, Grid } from '@mui/material';
import { Warning, TrendingUp } from '@mui/icons-material';

const PainPointAnalysis = ({ painPoints = [], opportunities = [] }) => {
  if ((!painPoints || painPoints.length === 0) && (!opportunities || opportunities.length === 0)) {
    return (
      <Box className="text-center py-8">
        <Typography variant="body1" className="text-gray-500">
          No pain points or opportunities identified
        </Typography>
      </Box>
    );
  }

  return (
    <Box className="space-y-6">
      <Grid container spacing={4}>
        <Grid item xs={12} md={6}>
          <Paper variant="outlined" className="p-4">
            <Box className="flex items-center gap-2 mb-4">
              <Warning className="text-red-500" />
              <Typography variant="h6" className="font-semibold">
                Pain Points ({painPoints.length || 0})
              </Typography>
            </Box>
            {painPoints && painPoints.length > 0 ? (
              <Box className="space-y-3">
                {painPoints.map((pain, idx) => (
                  <Box key={idx} className="border-b border-gray-100 pb-3">
                    {typeof pain === 'string' ? (
                      <Typography variant="body2">{pain}</Typography>
                    ) : (
                      <>
                        <Typography variant="body2" className="font-medium">
                          {pain.description || pain}
                        </Typography>
                        {pain.impact && (
                          <Typography variant="caption" className="text-gray-500 block">
                            Impact: {pain.impact}
                          </Typography>
                        )}
                        {pain.flytbase_solution && (
                          <Chip
                            size="small"
                            label={`Solution: ${pain.flytbase_solution}`}
                            color="primary"
                            variant="outlined"
                            className="mt-1"
                          />
                        )}
                      </>
                    )}
                  </Box>
                ))}
              </Box>
            ) : (
              <Typography variant="body2" className="text-gray-500">
                No pain points identified
              </Typography>
            )}
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper variant="outlined" className="p-4">
            <Box className="flex items-center gap-2 mb-4">
              <TrendingUp className="text-green-500" />
              <Typography variant="h6" className="font-semibold">
                Opportunities ({opportunities.length || 0})
              </Typography>
            </Box>
            {opportunities && opportunities.length > 0 ? (
              <Box className="space-y-3">
                {opportunities.map((opp, idx) => (
                  <Box key={idx} className="border-b border-gray-100 pb-3">
                    {typeof opp === 'string' ? (
                      <Typography variant="body2">{opp}</Typography>
                    ) : (
                      <>
                        <Typography variant="body2" className="font-medium">
                          {opp.description || opp}
                        </Typography>
                        {opp.potential && (
                          <Typography variant="caption" className="text-gray-500 block">
                            Potential: {opp.potential}
                          </Typography>
                        )}
                      </>
                    )}
                  </Box>
                ))}
              </Box>
            ) : (
              <Typography variant="body2" className="text-gray-500">
                No opportunities identified
              </Typography>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default PainPointAnalysis;