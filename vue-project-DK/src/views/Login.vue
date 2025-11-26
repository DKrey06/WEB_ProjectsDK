<template>
  <div class="login-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-12 col-md-8 col-lg-6 col-xl-4">
          <div class="card shadow">
            <div class="card-body">
              <h1 class="card-title">Вход в систему</h1>

              <div
                v-if="message"
                :class="[
                  'alert',
                  messageType === 'success' ? 'alert-success' : 'alert-danger',
                  'alert-dismissible fade show',
                ]"
                role="alert"
              >
                {{ message }}
                <button
                  type="button"
                  class="btn-close"
                  @click="message = ''"
                ></button>
              </div>

              <form @submit.prevent="handleLogin">
                <div class="mb-3">
                  <label class="form-label">Email:</label>
                  <input
                    class="form-control"
                    :class="{ 'is-invalid': errors.email }"
                    type="email"
                    v-model="form.email"
                    maxlength="100"
                    placeholder="Введите ваш email"
                  />
                  <div v-if="errors.email" class="invalid-feedback">
                    {{ errors.email }}
                  </div>
                </div>

                <div class="mb-3">
                  <label class="form-label">Пароль:</label>
                  <input
                    class="form-control"
                    :class="{ 'is-invalid': errors.password }"
                    type="password"
                    v-model="form.password"
                    placeholder="Введите ваш пароль"
                  />
                  <div v-if="errors.password" class="invalid-feedback">
                    {{ errors.password }}
                  </div>
                </div>

                <div v-if="errors.login" class="alert alert-danger">
                  {{ errors.login }}
                </div>

                <div class="d-grid">
                  <button
                    type="submit"
                    class="btn btn-primary"
                    :disabled="loading"
                  >
                    {{ loading ? "Вход..." : "Войти" }}
                  </button>
                </div>
              </form>

              <div class="text-center">
                <p>
                  Нет аккаунта?
                  <router-link to="/register">Зарегистрируйтесь</router-link>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const authStore = useAuthStore();

const form = reactive({
  email: "",
  password: "",
});

const errors = ref({});
const loading = ref(false);
const message = ref("");
const messageType = ref("");

const handleLogin = async () => {
  errors.value = {};
  loading.value = true;
  message.value = "";

  if (!form.email) {
    errors.value.email = "Обязательно введите email";
  }
  if (!form.password) {
    errors.value.password = "Обязательно введите пароль";
  }

  if (Object.keys(errors.value).length > 0) {
    loading.value = false;
    return;
  }

  try {
    const result = await authStore.login(form);

    if (result.success) {
      message.value = "Успешный вход!";
      messageType.value = "success";
      setTimeout(() => {
        router.push("/");
      }, 1000);
    } else {
      errors.value.login = result.error || "Ошибка входа";
      messageType.value = "danger";
    }
  } catch (error) {
    errors.value.login = "Ошибка сервера";
    messageType.value = "danger";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-page {
  padding: 2rem 0;
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.container {
  max-width: 400px;
  margin: 0 auto;
  padding: 0 1rem;
}

.card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  border: none;
  overflow: hidden;
}

.card-body {
  padding: 2.5rem;
}

.card-title {
  color: #2c3e50;
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  text-align: center;
}

.form-label {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.5rem;
  display: block;
}

.form-control {
  border: 2px solid #e9ecef;
  border-radius: 10px;
  padding: 0.875rem 1rem;
  font-size: 1rem;
  transition: all 0.3s;
  width: 100%;
  box-sizing: border-box;
}

.form-control:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  outline: none;
}

.form-control.is-invalid {
  border-color: #e74c3c;
  box-shadow: 0 0 0 3px rgba(231, 76, 60, 0.1);
}

.invalid-feedback {
  color: #e74c3c;
  font-size: 0.875rem;
  margin-top: 0.25rem;
  display: block;
}

.mb-3 {
  margin-bottom: 1.5rem !important;
}

.btn {
  width: 100%;
  padding: 0.875rem 2rem;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
}

.btn-primary:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.text-center {
  text-align: center;
  margin-top: 1.5rem;
}

.text-center p {
  color: #6c757d;
  margin: 0;
}

.text-center a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.text-center a:hover {
  color: #764ba2;
  text-decoration: underline;
}

.alert {
  border-radius: 10px;
  border: none;
  margin-bottom: 1.5rem;
  padding: 1rem 1.25rem;
}

.alert-success {
  background: rgba(102, 126, 234, 0.1);
  color: #2c3e50;
  border-left: 4px solid #667eea;
}

.alert-danger {
  background: rgba(231, 76, 60, 0.1);
  color: #2c3e50;
  border-left: 4px solid #e74c3c;
}

.alert-dismissible .btn-close {
  padding: 0.75rem;
}

.alert.alert-danger {
  background: rgba(231, 76, 60, 0.1);
  color: #721c24;
  border: 1px solid rgba(231, 76, 60, 0.2);
}

form {
  margin: 0;
}

.d-grid {
  display: grid;
  gap: 1rem;
}

@media (max-width: 480px) {
  .card-body {
    padding: 2rem 1.5rem;
  }

  .card-title {
    font-size: 1.5rem;
  }

  .container {
    padding: 0 0.5rem;
  }
}
</style>
