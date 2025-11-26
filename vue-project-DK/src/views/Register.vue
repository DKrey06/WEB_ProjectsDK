<template>
  <div class="register-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-12 col-md-10 col-lg-8">
          <div class="card shadow">
            <div class="card-body">
              <h1 class="card-title">Регистрация</h1>

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

              <form @submit.prevent="handleRegister">
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label">Имя:</label>
                    <input
                      class="form-control"
                      :class="{ 'is-invalid': errors.name }"
                      type="text"
                      v-model="form.name"
                      maxlength="100"
                      placeholder="Введите ваше имя"
                    />
                    <div v-if="errors.name" class="invalid-feedback">
                      {{ errors.name }}
                    </div>
                  </div>

                  <div class="col-md-6 mb-3">
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
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label">Пароль:</label>
                    <input
                      class="form-control"
                      :class="{ 'is-invalid': errors.password }"
                      type="password"
                      v-model="form.password"
                      minlength="6"
                      placeholder="Введите пароль"
                    />
                    <div v-if="errors.password" class="invalid-feedback">
                      {{ errors.password }}
                    </div>
                    <div class="form-text">Минимум 6 символов</div>
                  </div>

                  <div class="col-md-6 mb-3">
                    <label class="form-label">Повторите пароль:</label>
                    <input
                      class="form-control"
                      :class="{ 'is-invalid': errors.confirmPassword }"
                      type="password"
                      v-model="form.confirmPassword"
                      placeholder="Повторите пароль"
                    />
                    <div v-if="errors.confirmPassword" class="invalid-feedback">
                      {{ errors.confirmPassword }}
                    </div>
                  </div>
                </div>

                <div class="d-grid mt-3">
                  <button
                    type="submit"
                    class="btn btn-primary"
                    :disabled="loading"
                  >
                    {{ loading ? "Регистрация..." : "Зарегистрироваться" }}
                  </button>
                </div>
              </form>

              <div class="text-center">
                <p>
                  Уже есть аккаунт?
                  <router-link to="/login">Войдите</router-link>
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
  name: "",
  email: "",
  password: "",
  confirmPassword: "",
});

const errors = ref({});
const loading = ref(false);
const message = ref("");
const messageType = ref("");

const validateForm = () => {
  errors.value = {};

  if (!form.name) {
    errors.value.name = "Обязательно введите имя";
  } else if (form.name.length < 2) {
    errors.value.name = "Имя должно содержать минимум 2 символа";
  }

  if (!form.email) {
    errors.value.email = "Обязательно введите email";
  } else {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailPattern.test(form.email)) {
      errors.value.email = "Введите корректный email адрес";
    }
  }

  if (!form.password) {
    errors.value.password = "Обязательно введите пароль";
  } else if (form.password.length < 6) {
    errors.value.password = "Пароль должен содержать минимум 6 символов";
  }

  if (!form.confirmPassword) {
    errors.value.confirmPassword = "Обязательно подтвердите пароль";
  } else if (form.password !== form.confirmPassword) {
    errors.value.confirmPassword = "Пароли не совпадают";
  }

  return Object.keys(errors.value).length === 0;
};

const handleRegister = async () => {
  if (!validateForm()) {
    return;
  }

  loading.value = true;
  message.value = "";

  try {
    const result = await authStore.register({
      name: form.name,
      email: form.email,
      password: form.password,
    });

    if (result.success) {
      message.value = "Регистрация прошла успешно! Добро пожаловать!";
      messageType.value = "success";

      setTimeout(() => {
        router.push("/");
      }, 2000);
    } else {
      message.value = result.error || "Ошибка регистрации";
      messageType.value = "danger";
    }
  } catch (error) {
    message.value = "Ошибка регистрации";
    messageType.value = "danger";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.register-page {
  padding: 2rem 0;
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.container {
  max-width: 500px;
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

.form-text {
  color: #6c757d;
  font-size: 0.875rem;
  margin-top: 0.25rem;
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

.row {
  margin: 0 -0.5rem;
}

.col-md-6 {
  padding: 0 0.5rem;
}

form {
  margin: 0;
}

.d-grid {
  display: grid;
  gap: 1rem;
}

.mt-3 {
  margin-top: 1rem !important;
}

@media (max-width: 768px) {
  .card-body {
    padding: 2rem 1.5rem;
  }

  .card-title {
    font-size: 1.5rem;
  }

  .container {
    padding: 0 0.5rem;
  }

  .col-md-6 {
    padding: 0;
    margin-bottom: 1rem;
  }

  .row {
    margin: 0;
  }
}
</style>
