import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

const API_BASE_URL = '/api';

const api = axios.create({
	baseURL: API_BASE_URL,
	headers: {
		'Content-Type': 'application/json',
	},
});

// Интерцептор для добавления токена
api.interceptors.request.use(
	(config) => {
		const authStore = useAuthStore();
		const token = authStore.accessToken;

		if (token) {
			config.headers.Authorization = `Bearer ${token}`;
		}

		return config;
	},
	(error) => {
		return Promise.reject(error);
	}
);

// Интерцептор для обработки ошибок
api.interceptors.response.use(
	(response) => response,
	async (error) => {
		const originalRequest = error.config;

		if (error.response?.status === 401 && !originalRequest._retry) {
			originalRequest._retry = true;

			const authStore = useAuthStore();
			try {
				// Используем правильное имя функции
				const success = await authStore.refreshToken();
				if (success) {
					return api(originalRequest);
				}
			} catch (refreshError) {
				authStore.logout();
				window.location.href = '/login';
				return Promise.reject(refreshError);
			}
		}

		return Promise.reject(error);
	}
);

export default api;