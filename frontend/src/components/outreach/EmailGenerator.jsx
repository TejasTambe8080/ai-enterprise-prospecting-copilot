import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  Chip,
  Tabs,
  Tab,
  TextField,
  IconButton,
} from '@mui/material';
import { ContentCopy, Send, Edit } from '@mui/icons-material';
import toast from 'react-hot-toast';

const EmailGenerator = ({ emails = [], linkedin = '' }) => {
  const [activeTab, setActiveTab] = useState(0);

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text);
    toast.success('Copied to clipboard!');
  };

  if ((!emails || emails.length === 0) && !linkedin) {
    return (
      <Box className="text-center py-8">
        <Typography variant="body1" className="text-gray-500">
          No outreach content generated yet
        </Typography>
      </Box>
    );
  }

  return (
    <Box className="space-y-6">
      {/* Email Drafts */}
      {emails && emails.length > 0 && (
        <Paper variant="outlined" className="p-6">
          <Typography variant="h6" className="font-semibold mb-4">
            Email Drafts
          </Typography>
          <Tabs
            value={activeTab}
            onChange={(e, newValue) => setActiveTab(newValue)}
            className="mb-4"
          >
            {emails.map((email, idx) => (
              <Tab
                key={idx}
                label={
                  <Box className="flex items-center gap-2">
                    <span>Level {email.level || idx + 1}</span>
                    {email.level === 3 && (
                      <Chip size="small" label="Best" color="success" />
                    )}
                  </Box>
                }
              />
            ))}
          </Tabs>

          {emails[activeTab] && (
            <Box className="space-y-4">
              <TextField
                fullWidth
                label="Subject Line"
                value={emails[activeTab].subject || ''}
                variant="outlined"
                InputProps={{
                  endAdornment: (
                    <IconButton onClick={() => handleCopy(emails[activeTab].subject)}>
                      <ContentCopy fontSize="small" />
                    </IconButton>
                  ),
                }}
              />
              <TextField
                fullWidth
                label="Email Body"
                value={emails[activeTab].body || ''}
                multiline
                rows={8}
                variant="outlined"
                InputProps={{
                  endAdornment: (
                    <IconButton onClick={() => handleCopy(emails[activeTab].body)}>
                      <ContentCopy fontSize="small" />
                    </IconButton>
                  ),
                }}
              />
              {emails[activeTab].cta && (
                <Box className="bg-blue-50 p-3 rounded-lg">
                  <Typography variant="body2" className="text-blue-700">
                    CTA: {emails[activeTab].cta}
                  </Typography>
                </Box>
              )}
              <Box className="flex gap-2">
                <Button
                  variant="contained"
                  color="primary"
                  startIcon={<Send />}
                  className="normal-case"
                >
                  Send Email
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<Edit />}
                  className="normal-case"
                >
                  Edit Draft
                </Button>
              </Box>
            </Box>
          )}
        </Paper>
      )}

      {/* LinkedIn Message */}
      {linkedin && (
        <Paper variant="outlined" className="p-6">
          <Typography variant="h6" className="font-semibold mb-4">
            LinkedIn Message
          </Typography>
          <Box className="space-y-4">
            <TextField
              fullWidth
              label="Connection Request"
              value={typeof linkedin === 'string' ? linkedin : linkedin.connection_request || ''}
              multiline
              rows={3}
              variant="outlined"
              InputProps={{
                endAdornment: (
                  <IconButton
                    onClick={() =>
                      handleCopy(
                        typeof linkedin === 'string'
                          ? linkedin
                          : linkedin.connection_request || ''
                      )
                    }
                  >
                    <ContentCopy fontSize="small" />
                  </IconButton>
                ),
              }}
            />
            {typeof linkedin === 'object' && linkedin.follow_up_message && (
              <TextField
                fullWidth
                label="Follow-up Message"
                value={linkedin.follow_up_message}
                multiline
                rows={3}
                variant="outlined"
                InputProps={{
                  endAdornment: (
                    <IconButton onClick={() => handleCopy(linkedin.follow_up_message)}>
                      <ContentCopy fontSize="small" />
                    </IconButton>
                  ),
                }}
              />
            )}
            <Button variant="contained" color="secondary" className="normal-case">
              Open LinkedIn
            </Button>
          </Box>
        </Paper>
      )}
    </Box>
  );
};

export default EmailGenerator;