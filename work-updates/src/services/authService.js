import axios from 'axios';
const API = import.meta.env.VITE_API_BASE_URL || '/api';
const API_URL = 'auth';

export const login = async (email, employeeId, password) => {
    try {
        const payload = {};
        if (email) payload.email = email;
        if (employeeId) payload.employee_id = employeeId;
        payload.password = password;

        const response = await axios.post(`${API}/${API_URL}/login`, payload);
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.detail || 'Invalid credentials');
    }
};

export const changePassword = async (token, newPassword) => {
    try {
        const response = await axios.post(
            `${API}/${API_URL}/change-password`,
            { newPassword },
            { headers: { Authorization: `Bearer ${token}` } }
        );
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.detail || 'Failed to change password');
    }
};
