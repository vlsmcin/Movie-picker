import axios from "axios";
import { useUserAuthStore } from "@/stores/user";

let isRefreshing = false;
let refreshPromise: Promise<string> | null = null;

const api = axios.create({
    baseURL: 'http://localhost:8000/api/v1',
    headers: {
        'Content-Type': 'application/json',
    },
});

const refreshClient = axios.create({
    baseURL: 'http://localhost:8000/api/v1/auth/refresh',
    headers: {
        'Content-Type': 'application/json',
    },
});

api.interceptors.request.use(
    config => {
        const token = localStorage.getItem('access');

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        
        return config;
    }
);

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        const userAuthStore = useUserAuthStore();

        if (error.response?.status !== 401 || originalRequest._retry) {
            return Promise.reject(error);
        }

        originalRequest._retry = true;

        const refresh = localStorage.getItem('refresh');

        if (!refresh) {
            userAuthStore.logout();
            return Promise.reject(error);
        }

        try {
            if (!isRefreshing) {
                isRefreshing = true;

                refreshPromise = refreshClient
                .post('/', { refresh })
                .then((res) => {
                    const newAccess = res.data.access;
                    localStorage.setItem('access', newAccess);
                    userAuthStore.token = newAccess;
                    return newAccess;
                })
                .catch((err) => {
                    userAuthStore.logout();
                    throw err;
                })
                .finally(() => {
                    isRefreshing = false;
                });
            }

            const newToken = await refreshPromise;

            originalRequest.headers.Authorization = `Bearer ${newToken}`;
            return api(originalRequest);
        } catch (err) {
            return Promise.reject(err);
        }
    }
);

export { api, refreshClient };