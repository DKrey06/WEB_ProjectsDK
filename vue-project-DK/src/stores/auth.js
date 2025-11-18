import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { authService } from '@/services/auth-api';
import Cookies from 'js-cookie';

export const useAuthStore = defineStore('auth', () => {
	const user = ref(null);
	const accessToken = ref(Cookies.get('access_token') || null);
	const isAuthenticated = computed(() => !!accessToken.value);

	async function login(credentials) {
		try {
			const response = await authService.login(credentials.email, credentials.password);

			if (response.success) {
				user.value = response.user;
				accessToken.value = response.access_token;

				Cookies.set('access_token', response.access_token, { expires: 5 / (24 * 60) });
				Cookies.set('refresh_token', response.refresh_token, { expires: 30 });

				await checkAuth();

				return { success: true };
			} else {
				return { success: false, error: response.error };
			}
		} catch (error) {
			return {
				success: false,
				error: error.response?.data?.error || 'Ошибка авторизации'
			};
		}
	}

	async function register(userData) {
		try {
			const response = await authService.register(userData);

			if (response.success) {
				user.value = response.user;
				accessToken.value = response.access_token;

				Cookies.set('access_token', response.access_token, { expires: 5 / (24 * 60) });
				Cookies.set('refresh_token', response.refresh_token, { expires: 30 });

				await checkAuth();

				return { success: true };
			} else {
				return { success: false, error: response.error };
			}
		} catch (error) {
			return {
				success: false,
				error: error.response?.data?.error || 'Ошибка регистрации'
			};
		}
	}

	function logout() {
		user.value = null;
		accessToken.value = null;

		Cookies.remove('access_token');
		Cookies.remove('refresh_token');

		if (window.location.pathname !== '/') {
			window.location.href = '/';
		}
	}

	async function checkAuth() {
		if (!accessToken.value) {
			return false;
		}

		try {
			const response = await authService.verifyToken();
			if (response.success) {
				user.value = response.user;
				return true;
			}
		} catch (error) {
			console.log('Auth check failed:', error.response?.data?.error || error.message);
			return false;
		}
		return false;
	}

	return {
		user,
		accessToken,
		isAuthenticated,
		login,
		register,
		logout,
		checkAuth
	};
});