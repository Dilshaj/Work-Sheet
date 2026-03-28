import axios from 'axios';
const API = import.meta.env.VITE_API_BASE_URL || '/api';
const API_URL = 'employee';

export const updateProfile = async (formData) => {
    try {
        const user = JSON.parse(localStorage.getItem('user_v2'));
        const token = user?.token;

        const response = await axios.put(`${API}/${API_URL}/update-profile`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
                'Authorization': `Bearer ${token}`
            },
        });
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.detail || 'Failed to update profile');
    }
};

export const getProfile = async (userId) => {
    try {
        const user = JSON.parse(localStorage.getItem('user_v2'));
        const token = user?.token;

        const response = await axios.get(`${API}/${API_URL}/profile/${userId}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.detail || 'Failed to fetch profile');
    }
};
