import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { authService } from '@/services/auth-api';
import Cookies from 'js-cookie';

export const useAuthStore = defineStore('auth', () => {
	const user = ref(null);
	const accessToken = ref(Cookies.get('access_token') || null);
	const refreshTokenValue = ref(Cookies.get('refresh_token') || null);
	const isAuthenticated = computed(() => !!accessToken.value);

	async function login(credentials) {
		try {
			const response = await authService.login(credentials.email, credentials.password);

			if (response.success) {
				user.value = response.user;
				accessToken.value = response.access_token;
				refreshTokenValue.value = response.refresh_token;

				Cookies.set('access_token', response.access_token, { expires: 1 });
				Cookies.set('refresh_token', response.refresh_token, { expires: 30 });

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

	async function refreshToken() {
		try {
			const response = await authService.refreshToken();
			accessToken.value = response.access_token;
			Cookies.set('access_token', response.access_token, { expires: 1 });
			return true;
		} catch (error) {
			this.logout();
			return false;
		}
	}

	function logout() {
		user.value = null;
		accessToken.value = null;
		refreshTokenValue.value = null;

		Cookies.remove('access_token');
		Cookies.remove('refresh_token');

		if (window.location.pathname !== '/') {
			window.location.href = '/';
		}
	}

	return {
		user,
		accessToken,
		refreshToken: refreshTokenValue,
		isAuthenticated,
		login,
		refreshToken: refreshToken,
		logout
	};
});