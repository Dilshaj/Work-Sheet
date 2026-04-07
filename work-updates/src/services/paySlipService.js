import api from './api';

export const generatePaySlip = async (data) => {
    const response = await api.post('/pay-slips', data);
    return response.data;
};

export const getAllPaySlips = async (projectId = null) => {
    const response = await api.get('/pay-slips', {
        params: { project_id: projectId }
    });
    return response.data;
};

export const getMyPaySlips = async (employeeId) => {
    const response = await api.get(`/pay-slips/my/${employeeId}`);
    return response.data;
};
