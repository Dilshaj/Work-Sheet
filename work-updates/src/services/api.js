import axios from 'axios';

const RAW_BASE_URL = import.meta.env.VITE_API_URL || import.meta.env.VITE_API_BASE_URL || '/api';
const API_BASE_URL = RAW_BASE_URL.endsWith('/') ? RAW_BASE_URL : `${RAW_BASE_URL}/`;

console.log(`[API] Initialized with Base URL: ${API_BASE_URL}`);

const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 15000,
});

// Add request interceptor
api.interceptors.request.use(
    (config) => {
        const savedUser = localStorage.getItem('user_v2');
        if (savedUser) {
            const { token } = JSON.parse(savedUser);
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default api;
