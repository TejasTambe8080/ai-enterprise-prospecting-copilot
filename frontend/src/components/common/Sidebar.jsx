import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  Dashboard as DashboardIcon,
  People as PeopleIcon,
  BarChart as BarChartIcon,
  History as HistoryIcon,
  Settings as SettingsIcon,
  Rocket as RocketIcon,
} from '@mui/icons-material';
import { Box, List, ListItem, ListItemIcon, ListItemText, Typography } from '@mui/material';

const menuItems = [
  { path: '/dashboard', label: 'Dashboard', icon: DashboardIcon },
  { path: '/leads', label: 'Leads', icon: PeopleIcon },
  { path: '/reports', label: 'Reports', icon: BarChartIcon },
  { path: '/history', label: 'History', icon: HistoryIcon },
  { path: '/settings', label: 'Settings', icon: SettingsIcon },
];

const Sidebar = () => {
  return (
    <Box className="fixed left-0 top-0 h-full w-64 bg-white border-r border-gray-200 shadow-sm">
      <Box className="p-6 border-b border-gray-200">
        <Box className="flex items-center gap-3">
          <RocketIcon className="text-primary-600" fontSize="large" />
          <Typography variant="h6" className="font-bold text-gray-800">
            FlytBase BDR
          </Typography>
        </Box>
        <Typography variant="caption" className="text-gray-500">
          Enterprise Lead Automation
        </Typography>
      </Box>
      <List className="p-4">
        {menuItems.map((item) => (
          <ListItem
            key={item.path}
            component={NavLink}
            to={item.path}
            className={({ isActive }) =>
              `rounded-lg mb-1 transition-colors ${
                isActive
                  ? 'bg-primary-50 text-primary-700'
                  : 'text-gray-600 hover:bg-gray-50'
              }`
            }
          >
            <ListItemIcon>
              <item.icon className="text-inherit" />
            </ListItemIcon>
            <ListItemText primary={item.label} />
          </ListItem>
        ))}
      </List>
    </Box>
  );
};

export default Sidebar;