import React from 'react';
import { CircularProgress, Box, Typography } from '@mui/material';

const LoadingSpinner = ({ message = 'Loading...', size = 40 }) => {
  return (
    <Box className="flex flex-col items-center justify-center min-h-[200px]">
      <CircularProgress size={size} className="text-primary-600" />
      <Typography variant="body2" className="text-gray-500 mt-4">
        {message}
      </Typography>
    </Box>
  );
};

export default LoadingSpinner;