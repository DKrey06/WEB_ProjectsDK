import axios from 'axios';
import Cookies from 'js-cookie';

const API_BASE_URL = 'http://127.0.0.1:5000';

const api = axios.create({
	baseURL: API_BASE_URL,
	headers: {
		'Content-Type': 'application/json',
	},
});

let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
	failedQueue.forEach(prom => {
		if (error) {
			prom.reject(error);
		} else {
			prom.resolve(token);
		}
	});
	failedQueue = [];
};

const getToken = () => Cookies.get('access_token');
const getRefreshToken = () => Cookies.get('refresh_token');

api.interceptors.request.use(
	(config) => {
		const token = getToken();
		if (token) {
			config.headers.Authorization = `Bearer ${token}`;
		}
		return config;
	},
	(error) => {
		return Promise.reject(error);
	}
);

api.interceptors.response.use(
	(response) => response,
	async (error) => {
		const originalRequest = error.config;

		if (error.response?.status !== 401 || originalRequest._retry) {
			return Promise.reject(error);
		}

		if (isRefreshing) {
			return new Promise((resolve, reject) => {
				failedQueue.push({ resolve, reject });
			}).then(token => {
				originalRequest.headers.Authorization = `Bearer ${token}`;
				return api(originalRequest);
			}).catch(err => {
				return Promise.reject(err);
			});
		}

		originalRequest._retry = true;
		isRefreshing = true;

		try {
			const refreshToken = getRefreshToken();
			if (!refreshToken) {
				throw new Error('No refresh token available');
			}

			console.log('Attempting token refresh...');

			const refreshResponse = await axios.post(`${API_BASE_URL}/api/auth/refresh`, {}, {
				headers: {
					'Authorization': `Bearer ${refreshToken}`
				}
			});

			if (refreshResponse.data.success) {
				const newToken = refreshResponse.data.access_token;

				Cookies.set('access_token', newToken, { expires: 5 / (24 * 60) });

				if (refreshResponse.data.refresh_token) {
					Cookies.set('refresh_token', refreshResponse.data.refresh_token, { expires: 30 });
				}

				processQueue(null, newToken);
				originalRequest.headers.Authorization = `Bearer ${newToken}`;
				return api(originalRequest);
			} else {
				throw new Error('Refresh failed: ' + (refreshResponse.data.error || 'Unknown error'));
			}
		} catch (refreshError) {
			console.error('Token refresh failed:', refreshError);
			processQueue(refreshError, null);

			Cookies.remove('access_token');
			Cookies.remove('refresh_token');

			if (typeof window !== 'undefined') {
				window.location.href = '/login';
			}

			return Promise.reject(refreshError);
		} finally {
			isRefreshing = false;
		}
	}
);

export default api;