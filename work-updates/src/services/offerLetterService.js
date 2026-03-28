import axios from 'axios';
const API = import.meta.env.VITE_API_BASE_URL || '/api';
const API_URL = 'offer-letter';

export const saveOfferLetter = async (offerData) => {
    try {
        const response = await axios.post(`${API}/${API_URL}/`, offerData);
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.detail || 'Failed to save offer letter');
    }
};

export const getOfferLetters = async (projectId = null) => {
    try {
        const params = {};
        if (projectId) params.project_id = projectId;
        const response = await axios.get(`${API}/${API_URL}/`, { params });
        return response.data;
    } catch (error) {
        console.error('Failed to fetch offer letters:', error);
        return [];
    }
};

export const downloadOfferLetter = async (employeeId) => {
    try {
        const response = await axios({
            url: `${API}/${API_URL}/${employeeId}`,
            method: 'GET',
            responseType: 'blob', // Important
        });

        // Create blob link to download
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `OfferLetter_${employeeId}.pdf`);
        document.body.appendChild(link);
        link.click();

        // Clean up
        link.parentNode.removeChild(link);
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error('Download error:', error);
        alert('Failed to download offer letter. Please try again.');
    }
};
