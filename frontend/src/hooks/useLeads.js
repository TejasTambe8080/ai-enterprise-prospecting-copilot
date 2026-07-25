import { useState, useEffect } from 'react';
import { leadAPI } from '../api/endpoints';

export const useLeads = (params = {}) => {
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [pagination, setPagination] = useState({});

  useEffect(() => {
    fetchLeads();
  }, [JSON.stringify(params)]);

  const fetchLeads = async () => {
    setLoading(true);
    try {
      const response = await leadAPI.getLeads(params);
      setLeads(response.data.data || []);
      setPagination(response.data.pagination || {});
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const refresh = () => fetchLeads();

  return { leads, loading, error, pagination, refresh };
};