import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { authService } from '@/services/auth';

export const useAuthStore = defineStore('auth', () => {
	const user = ref(null);
	const isAuthenticated = ref(false);

	async function login(credentials) {
		try {
			const response = await authService.login(credentials.email, credentials.password);
			user.value = response.user;
			isAuthenticated.value = true;
			return { success: true };
		} catch (error) {
			return {
				success: false,
				error: error.response?.data?.error || 'Ошибка авторизации'
			};
		}
	}

	function logout() {
		user.value = null;
		isAuthenticated.value = false;
	}

	return {
		user,
		isAuthenticated,
		login,
		logout
	};
});