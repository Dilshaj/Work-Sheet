import axios from 'axios';
const API = import.meta.env.VITE_API_BASE_URL || '/api';
const API_URL = 'employee';

export const applyLeave = async (leaveData) => {
    try {
        const response = await axios.post(`${API}/${API_URL}/apply-leave`, leaveData);
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.detail || 'Failed to submit leave request');
    }
};

export const getMyLeaves = async (employeeId) => {
    try {
        const response = await axios.get(`${API}/${API_URL}/my-leaves/${employeeId}`);
        return response.data;
    } catch (error) {
        console.error('Failed to fetch user leaves:', error);
        return [];
    }
};

export const getAllLeaves = async (projectId = null) => {
    try {
        const params = {};
        if (projectId) params.project_id = projectId;
        const response = await axios.get(`${API}/${API_URL}/all-leaves`, { params });
        return response.data;
    } catch (error) {
        console.error('Failed to fetch all leaves:', error);
        return [];
    }
};

export const updateLeaveStatus = async (leaveId, status) => {
    try {
        const response = await axios.patch(`${API}/${API_URL}/update-status/${leaveId}?status=${status}`);
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.detail || 'Failed to update leave status');
    }
};
