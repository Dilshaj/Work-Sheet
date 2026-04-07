import React, { createContext, useState, useEffect, useContext, useCallback, useMemo } from 'react';
import { getAttendanceLogs, checkIn, checkOut } from '../services/attendanceService';
import { useAuth } from './AuthContext';
import { useProjectFilter } from './ProjectFilterContext';

const AttendanceContext = createContext();

export const useAttendance = () => useContext(AttendanceContext);

export const AttendanceProvider = ({ children }) => {
    const { user } = useAuth();
    const { selectedProjectId } = useProjectFilter();
    const [logs, setLogs] = useState([]);
    const [activeLog, setActiveLog] = useState(null);

    const fetchLogs = useCallback(async (silent = false) => {
        try {
            const isAdmin = user?.role === 'admin';
            const projId = isAdmin ? selectedProjectId : null;
            const data = await getAttendanceLogs(projId);
            setLogs(data);

            if (user) {
                const today = new Date().toISOString().split('T')[0];
                const empId = user.employee_id || user.employeeId;
                const active = data.find(l => l.employeeId === empId && l.date === today && l.status === 'Checked In');
                setActiveLog(active || null);
            }
        } catch (error) {
            console.error("Error fetching attendance logs:", error);
        }
    }, [user, selectedProjectId]);

    useEffect(() => {
        fetchLogs();
    }, [fetchLogs]);

    const handleCheckIn = async () => {
        if (!user) return;
        const empId = user.employee_id || user.employeeId;

        console.log("Checking in...", empId);

        let latitude = null;
        let longitude = null;
        let locationName = null;

        const getBrowserLocation = () => {
            return new Promise((resolve) => {
                if (!navigator.geolocation) {
                    console.warn("Geolocation not supported by this browser.");
                    resolve(null);
                } else {
                    navigator.geolocation.getCurrentPosition(
                        (pos) => resolve({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
                        (err) => {
                            console.warn("Geolocation denied/failed:", err.message);
                            resolve(null);
                        },
                        { timeout: 10000, enableHighAccuracy: true }
                    );
                }
            });
        };

        const getIPLocation = async () => {
            try {
                // Fallback to IP-based location (good for indoor use or when GPS is denied)
                const res = await fetch('https://ipapi.co/json/');
                const data = await res.json();
                if (data && data.latitude) {
                    console.log("IP-based location found:", data.city);
                    return {
                        lat: data.latitude,
                        lng: data.longitude,
                        city: data.city,
                        region: data.region
                    };
                }
            } catch (err) {
                console.error("IP Location fallback failed", err);
            }
            return null;
        };

        // 1. Try GPS first
        let coords = await getBrowserLocation();

        // 2. Try IP fallback if GPS fails
        if (!coords) {
            const ipData = await getIPLocation();
            if (ipData) {
                coords = { lat: ipData.lat, lng: ipData.lng };
                locationName = `${ipData.city}, ${ipData.region}`;
            }
        }

        if (coords) {
            latitude = coords.lat;
            longitude = coords.lng;

            // 3. Try to get a more specific address if we didn't get one from IP
            if (!locationName) {
                try {
                    const response = await fetch(`https://nominatim.openstreetmap.org/reverse?lat=${latitude}&lon=${longitude}&format=json`, {
                        headers: { 'Accept-Language': 'en' }
                    });
                    const data = await response.json();
                    if (data && data.address) {
                        const addr = data.address;
                        locationName = addr.suburb || addr.neighbourhood || addr.city_district || addr.town || addr.city || addr.village || "Unknown Area";
                        const city = addr.city || addr.town || addr.state || "";
                        locationName = (locationName !== city && city) ? `${city}, ${locationName}` : locationName;
                    }
                } catch (err) {
                    console.error("Reverse geocoding failed", err);
                    locationName = "Location captured (GPS)";
                }
            }
        } else {
            console.warn("All location methods failed.");
            locationName = "Location access denied";
        }

        try {
            const newLog = await checkIn({
                userId: user.id,
                employeeId: empId,
                userName: user.name,
                projectId: selectedProjectId,
                latitude,
                longitude,
                location_name: locationName || "Auto-detected Location"
            });
            setLogs(prev => [newLog, ...prev]);
            setActiveLog(newLog);
        } catch (error) {
            alert(error.message);
        }
    };

    const handleCheckOut = async () => {
        if (!user) return;
        const empId = user.employee_id || user.employeeId;
        try {
            const updatedLog = await checkOut(user.id, empId);
            if (updatedLog) {
                setLogs(prev => prev.map(l => l.id === updatedLog.id ? updatedLog : l));
                setActiveLog(null);
            }
        } catch (error) {
            alert(error.message);
        }
    };

    const value = useMemo(() => ({
        logs,
        activeLog,
        handleCheckIn,
        handleCheckOut
    }), [logs, activeLog, handleCheckIn, handleCheckOut]);

    return (
        <AttendanceContext.Provider value={value}>
            {children}
        </AttendanceContext.Provider>
    );
};
