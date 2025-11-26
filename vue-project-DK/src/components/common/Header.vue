<template>
  <header class="header">
    <nav class="nav">
      <div class="nav-brand">
        <router-link to="/" class="logo">
          <img src="/images/LogoCat.png" alt="Логотип" class="logo-image" />
          NEWS_DK
        </router-link>
      </div>

      <ul class="nav-menu">
        <li><router-link to="/">Главная</router-link></li>
        <li><router-link to="/about">О проекте</router-link></li>
        <li><router-link to="/articles">Все статьи</router-link></li>
        <li><router-link to="/contact">Контакты</router-link></li>
        <li><router-link to="/feedback">Обратная связь</router-link></li>
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
          <router-link to="/register" class="btn-register"
            >Регистрация</router-link
          >
        </template>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

const authStore = useAuthStore();
const router = useRouter();

const logout = () => {
  authStore.logout();
  router.push("/");
};
</script>

<style scoped>
.header {
  background: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
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
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
  color: #2c3e50;
  transition: color 0.3s;
}

.logo:hover {
  color: #42b883;
}

.logo-image {
  width: 52px;
  height: 52px;
  object-fit: contain;
  border-radius: 8px;
}

.nav-menu {
  display: flex;
  list-style: none;
  gap: 1.5rem;
  margin: 0;
  padding: 0;
}

.nav-menu a {
  text-decoration: none;
  color: #2c3e50;
  font-weight: 500;
  transition: color 0.3s;
  font-size: 0.9rem;
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
  background: transparent;
  color: #42b883;
  border: 1px solid #42b883;
}

.btn-register:hover {
  background: #42b883;
  color: white;
}

.btn-logout {
  background: #e74c3c;
  color: white;
}

.btn-logout:hover {
  background: #c0392b;
}

@media (max-width: 768px) {
  .nav {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }

  .nav-menu {
    gap: 1rem;
    flex-wrap: wrap;
    justify-content: center;
  }

  .nav-menu a {
    font-size: 0.8rem;
  }

  .nav-auth {
    gap: 0.5rem;
  }

  .user-greeting {
    font-size: 0.8rem;
  }

  .btn-login,
  .btn-register,
  .btn-logout {
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
  }

  .logo {
    font-size: 1.25rem;
  }

  .logo-image {
    width: 40px;
    height: 40px;
  }
}

@media (max-width: 480px) {
  .logo {
    font-size: 1.1rem;
    gap: 0.75rem;
  }

  .logo-image {
    width: 36px;
    height: 36px;
  }
}
</style>
