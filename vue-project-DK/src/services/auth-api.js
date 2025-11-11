import api from './api';

export const authService = {
	async register(userData) {
		const response = await api.post('/api/auth/register', userData);
		return response.data;
	},

	async login(email, password) {
		const response = await api.post('/api/auth/login', { email, password });
		return response.data;
	},

	async refreshToken() {
		const response = await api.post('/api/auth/refresh');
		return response.data;
	},

	async verifyToken() {
		const response = await api.post('/api/auth/verify');
		return response.data;
	}
};