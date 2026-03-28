import axios from 'axios';
const API = import.meta.env.VITE_API_BASE_URL || '/api';

// ─── Tasks ───────────────────────────────────────────────
export const getTasks = async () => {
    try {
        const res = await axios.get(`${API}/tasks`);
        return res.data;
    } catch { return []; }
};

export const getTasksByEmployee = async (userId) => {
    try {
        const res = await axios.get(`${API}/tasks/employee/${userId}`);
        return res.data;
    } catch { return []; }
};

export const addTask = async (task) => {
    try {
        const res = await axios.post(`${API}/tasks`, {
            title: task.title,
            description: task.description,
            deadline: task.deadline,
            priority: task.priority,
            timeline: task.timeline,
            assignedTo: task.assignedTo,
            projectId: task.projectId,
        });
        return res.data;
    } catch (error) {
        throw new Error(error.response?.data?.detail || 'Failed to add task');
    }
};

export const updateTaskStatus = async (id, status) => {
    try {
        const res = await axios.patch(`${API}/tasks/${id}/status`, { status });
        return res.data;
    } catch (error) {
        throw new Error(error.response?.data?.detail || 'Failed to update task status');
    }
};

// ─── Employees ───────────────────────────────────────────
export const getEmployees = async (projectId = null) => {
    try {
        const params = {};
        if (projectId) params.project_id = projectId;
        const res = await axios.get(`${API}/employees`, { params });
        return res.data;
    } catch { return []; }
};

export const updateEmployeeProgress = async (id, newProgressStats) => {
    try {
        const res = await axios.put(`${API}/employees/${id}/progress`, {
            dailyProgress: newProgressStats.dailyProgress,
            weeklyProgress: newProgressStats.weeklyProgress,
        });
        return res.data;
    } catch (error) {
        throw new Error(error.response?.data?.detail || 'Failed to update progress');
    }
};

export const addEmployee = async (employee) => {
    // Sends all fields including project_id for immediate assignment
    const res = await axios.post(`${API}/employees`, {
        employee_id: employee.employeeId,
        name: employee.name,
        role: employee.role,
        project_id: employee.projectId,
    });
    return res.data;
};

export const searchEmployee = async ({ employeeId, name }) => {
    try {
        const params = {};
        if (employeeId) params.employee_id = employeeId;
        if (name) params.name = name;
        const res = await axios.get(`${API}/employees/search`, { params });
        return res.data;
    } catch (error) {
        if (error.response?.status === 404) return null;
        throw error;
    }
};

export const assignEmployeeToProject = async (id, projectId) => {
    try {
        const res = await axios.put(`${API}/employees/${id}/assign`, { projectId });
        return res.data;
    } catch (error) {
        throw new Error(error.response?.data?.detail || 'Failed to assign project');
    }
};

export const deleteEmployee = async (employeeId) => {
    try {
        const res = await axios.delete(`${API}/employees/admin/delete-employee/${employeeId}`);
        return res.data;
    } catch (error) {
        const detail = error.response?.data?.detail || 'Failed to delete employee';
        throw new Error(detail);
    }
};
