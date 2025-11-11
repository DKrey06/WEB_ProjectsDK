<template>
  <header class="header">
    <nav class="nav">
      <div class="nav-brand">
        <router-link to="/" class="logo">NEWS_DK</router-link>
      </div>
      
      <ul class="nav-menu">
        <li><router-link to="/">Главная</router-link></li>
		<li><router-link to="/about">О проекте</router-link></li>
        <li><router-link to="/articles">Все статьи</router-link></li>
        <li v-if="authStore.isAuthenticated">
          <router-link to="/create-article">Создать статью</router-link>
        </li>
      </ul>

      <div class="nav-auth">
        <template v-if="authStore.isAuthenticated">
          <span class="user-greeting">Привет, {{ authStore.user?.name }}!</span>
          <button @click="logout" class="btn-logout">Выйти</button>
        </template>
        <template v-else>
          <router-link to="/login" class="btn-login">Войти</router-link>
          <router-link to="/register" class="btn-register">Регистрация</router-link>
        </template>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();

const logout = () => {
  authStore.logout();
};
</script>

<style scoped>
.header {
  background: #fff;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
  color: #2c3e50;
}

.nav-menu {
  display: flex;
  list-style: none;
  gap: 2rem;
  margin: 0;
  padding: 0;
}

.nav-menu a {
  text-decoration: none;
  color: #2c3e50;
  font-weight: 500;
  transition: color 0.3s;
}

.nav-menu a:hover,
.nav-menu a.router-link-active {
  color: #42b883;
}

.nav-auth {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-greeting {
  color: #666;
  font-size: 0.9rem;
}

.btn-login,
.btn-register,
.btn-logout {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s;
}

.btn-login {
  background: transparent;
  color: #42b883;
  border: 1px solid #42b883;
}

.btn-login:hover {
  background: #42b883;
  color: white;
}

.btn-register {
  background: #42b883;
  color: white;
}

.btn-register:hover {
  background: #369870;
}

.btn-logout {
  background: #e74c3c;
  color: white;
}

.btn-logout:hover {
  background: #c0392b;
}
</style>