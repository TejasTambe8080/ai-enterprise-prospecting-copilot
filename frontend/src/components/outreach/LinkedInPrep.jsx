import React from 'react';
import { Box, Typography, Paper, TextField, Button, Chip, IconButton } from '@mui/material';
import { ContentCopy, OpenInNew } from '@mui/icons-material';
import toast from 'react-hot-toast';

const LinkedInPrep = ({ linkedinData }) => {
  if (!linkedinData) {
    return (
      <Box className="text-center py-8">
        <Typography variant="body1" className="text-gray-500">
          No LinkedIn preparation data available
        </Typography>
      </Box>
    );
  }

  const handleCopy = (text) => {
    if (text) {
      navigator.clipboard.writeText(text);
      toast.success('Copied to clipboard!');
    }
  };

  const handleOpenLinkedIn = () => {
    if (linkedinData.profile_url) {
      window.open(linkedinData.profile_url, '_blank');
    } else {
      toast.info('LinkedIn profile URL not available');
    }
  };

  return (
    <Box className="space-y-4">
      <Paper variant="outlined" className="p-6">
        <Box className="flex justify-between items-center mb-4">
          <Typography variant="h6" className="font-semibold">
            LinkedIn Connection Request
          </Typography>
          <Box className="flex gap-2">
            <Button
              variant="outlined"
              size="small"
              startIcon={<OpenInNew />}
              onClick={handleOpenLinkedIn}
              className="normal-case"
            >
              Open LinkedIn
            </Button>
          </Box>
        </Box>

        <TextField
          fullWidth
          label="Connection Request (300 characters max)"
          value={linkedinData.connection_request || ''}
          multiline
          rows={2}
          variant="outlined"
          InputProps={{
            endAdornment: (
              <IconButton onClick={() => handleCopy(linkedinData.connection_request)}>
                <ContentCopy fontSize="small" />
              </IconButton>
            ),
          }}
        />

        {linkedinData.follow_up_message && (
          <TextField
            fullWidth
            label="Follow-up Message"
            value={linkedinData.follow_up_message}
            multiline
            rows={3}
            variant="outlined"
            className="mt-4"
            InputProps={{
              endAdornment: (
                <IconButton onClick={() => handleCopy(linkedinData.follow_up_message)}>
                  <ContentCopy fontSize="small" />
                </IconButton>
              ),
            }}
          />
        )}

        {linkedinData.inmail && (
          <TextField
            fullWidth
            label="InMail Message"
            value={linkedinData.inmail}
            multiline
            rows={4}
            variant="outlined"
            className="mt-4"
            InputProps={{
              endAdornment: (
                <IconButton onClick={() => handleCopy(linkedinData.inmail)}>
                  <ContentCopy fontSize="small" />
                </IconButton>
              ),
            }}
          />
        )}

        {linkedinData.mutual_connections && (
          <Box className="mt-4">
            <Typography variant="caption" className="text-gray-500">
              Mutual Connections
            </Typography>
            <Box className="flex flex-wrap gap-1 mt-1">
              {linkedinData.mutual_connections.map((conn, idx) => (
                <Chip key={idx} label={conn} size="small" variant="outlined" />
              ))}
            </Box>
          </Box>
        )}
      </Paper>
    </Box>
  );
};

export default LinkedInPrep;