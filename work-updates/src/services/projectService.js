import axios from 'axios';
const API = import.meta.env.VITE_API_BASE_URL || '/api';
const API_URL = 'projects';

export const getProjects = async (skip = 0, limit = 100) => {
    try {
        const response = await axios.get(`${API}/${API_URL}/`, {
            params: { skip, limit }
        });
        return response.data;
    } catch (error) {
        console.error('Failed to fetch projects:', error);
        return [];
    }
};

export const getProject = async (id) => {
    try {
        const response = await axios.get(`${API}/${API_URL}/${id}`);
        return response.data;
    } catch (error) {
        console.error(`Failed to fetch project ${id}:`, error);
        return null;
    }
};

export const addProject = async (projectData) => {
    try {
        const response = await axios.post(`${API}/${API_URL}/`, projectData);
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.detail || 'Failed to create project');
    }
};

export const updateProject = async (id, projectUpdate) => {
    try {
        const response = await axios.put(`${API}/${API_URL}/${id}`, projectUpdate);
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.detail || 'Failed to update project');
    }
};

export const deleteProject = async (id) => {
    try {
        const response = await axios.delete(`${API}/${API_URL}/${id}`);
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.detail || 'Failed to delete project');
    }
};
