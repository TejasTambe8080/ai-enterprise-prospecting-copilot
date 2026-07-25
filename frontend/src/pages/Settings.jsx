import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  TextField,
  Button,
  Switch,
  FormControlLabel,
  Divider,
  Alert,
  Snackbar,
} from '@mui/material';
import { Save } from '@mui/icons-material';

const Settings = () => {
  const [settings, setSettings] = useState({
    companyName: 'Acme Corp',
    emailSignature: 'Best regards,\n[Name]\nFlytBase BDR',
    autoProcess: true,
    autoEmail: false,
    emailDelay: 24,
    maxLeadsPerDay: 100,
    meddpiccThreshold: 60,
  });
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  const handleChange = (field) => (event) => {
    setSettings({
      ...settings,
      [field]: event.target.type === 'checkbox' ? event.target.checked : event.target.value,
    });
  };

  const handleSave = () => {
    setSnackbar({
      open: true,
      message: 'Settings saved successfully!',
      severity: 'success',
    });
  };

  return (
    <Box className="space-y-6">
      <Typography variant="h4" className="font-bold text-gray-800">
        Settings
      </Typography>

      <Paper className="p-6 rounded-xl shadow-sm">
        <Typography variant="h6" className="mb-4 font-semibold">
          General Settings
        </Typography>
        <Grid container spacing={4}>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Company Name"
              value={settings.companyName}
              onChange={handleChange('companyName')}
              variant="outlined"
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Email Signature"
              value={settings.emailSignature}
              onChange={handleChange('emailSignature')}
              multiline
              rows={3}
              variant="outlined"
            />
          </Grid>
        </Grid>
      </Paper>

      <Paper className="p-6 rounded-xl shadow-sm">
        <Typography variant="h6" className="mb-4 font-semibold">
          Automation Settings
        </Typography>
        <Grid container spacing={4}>
          <Grid item xs={12} md={6}>
            <FormControlLabel
              control={
                <Switch
                  checked={settings.autoProcess}
                  onChange={handleChange('autoProcess')}
                  color="primary"
                />
              }
              label="Auto-process incoming leads"
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <FormControlLabel
              control={
                <Switch
                  checked={settings.autoEmail}
                  onChange={handleChange('autoEmail')}
                  color="primary"
                />
              }
              label="Auto-send emails to qualified leads"
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              type="number"
              label="Email Delay (hours)"
              value={settings.emailDelay}
              onChange={handleChange('emailDelay')}
              variant="outlined"
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              type="number"
              label="Max Leads Per Day"
              value={settings.maxLeadsPerDay}
              onChange={handleChange('maxLeadsPerDay')}
              variant="outlined"
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              type="number"
              label="MEDDPICC Threshold"
              value={settings.meddpiccThreshold}
              onChange={handleChange('meddpiccThreshold')}
              variant="outlined"
              helperText="Minimum score to qualify a lead"
            />
          </Grid>
        </Grid>
      </Paper>

      <Box className="flex justify-end">
        <Button
          variant="contained"
          color="primary"
          startIcon={<Save />}
          onClick={handleSave}
          className="normal-case"
        >
          Save Settings
        </Button>
      </Box>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <Alert severity={snackbar.severity} onClose={() => setSnackbar({ ...snackbar, open: false })}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default Settings;