import React from 'react';
import { Outlet } from 'react-router-dom';
import { Box } from '@mui/material';
import Sidebar from './Sidebar';
import Header from './Header';

const Layout = () => {
  return (
    <Box className="flex min-h-screen">
      <Sidebar />
      <Box className="flex-1 ml-64">
        <Header />
        <Box className="p-6">
          <Outlet />
        </Box>
      </Box>
    </Box>
  );
};

export default Layout;