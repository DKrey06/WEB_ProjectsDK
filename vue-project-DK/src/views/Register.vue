<template>
  <div class="register-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-12 col-md-10 col-lg-12">
          <div class="card shadow">
            <div class="card-body p-5">
              <h1 class="card-title text-center mb-4">Регистрация</h1>

              <div v-if="message" :class="['alert', messageType === 'success' ? 'alert-success' : 'alert-danger', 'alert-dismissible fade show']" role="alert">
                {{ message }}
                <button type="button" class="btn-close" @click="message = ''"></button>
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
                    >
                    <div v-if="errors.name" class="invalid-feedback d-block">{{ errors.name }}</div>
                  </div>

                  <div class="col-md-6 mb-3">
                    <label class="form-label">Email:</label>
                    <input 
                      class="form-control" 
                      :class="{ 'is-invalid': errors.email }"
                      type="email" 
                      v-model="form.email"
                      maxlength="100"
                    >
                    <div v-if="errors.email" class="invalid-feedback d-block">{{ errors.email }}</div>
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
                    >
                    <div v-if="errors.password" class="invalid-feedback d-block">{{ errors.password }}</div>
                    <div class="form-text">Минимум 6 символов</div>
                  </div>

                  <div class="col-md-6 mb-3">
                    <label class="form-label">Повторите пароль:</label>
                    <input 
                      class="form-control" 
                      :class="{ 'is-invalid': errors.confirmPassword }"
                      type="password" 
                      v-model="form.confirmPassword"
                    >
                    <div v-if="errors.confirmPassword" class="invalid-feedback d-block">{{ errors.confirmPassword }}</div>
                  </div>
                </div>

                <div class="d-grid gap-2 mt-3">
                  <button type="submit" class="btn btn-primary btn-lg" :disabled="loading">
                    {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
                  </button>
                </div>
              </form>

              <div class="text-center mt-4">
                <p>Уже есть аккаунт? <router-link to="/login">Войдите</router-link></p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const errors = ref({})
const loading = ref(false)
const message = ref('')
const messageType = ref('')

const validateForm = () => {
  errors.value = {}

  if (!form.name) {
    errors.value.name = 'Обязательно введите имя'
  } else if (form.name.length < 2) {
    errors.value.name = 'Имя должно содержать минимум 2 символа'
  }

  if (!form.email) {
    errors.value.email = 'Обязательно введите email'
  } else {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
    if (!emailPattern.test(form.email)) {
      errors.value.email = 'Введите корректный email адрес'
    }
  }

  if (!form.password) {
    errors.value.password = 'Обязательно введите пароль'
  } else if (form.password.length < 6) {
    errors.value.password = 'Пароль должен содержать минимум 6 символов'
  }

  if (!form.confirmPassword) {
    errors.value.confirmPassword = 'Обязательно подтвердите пароль'
  } else if (form.password !== form.confirmPassword) {
    errors.value.confirmPassword = 'Пароли не совпадают'
  }

  return Object.keys(errors.value).length === 0
}

const handleRegister = async () => {
  if (!validateForm()) {
    return
  }

  loading.value = true
  message.value = ''

  try {
    const result = await authStore.register({
      name: form.name,
      email: form.email,
      password: form.password
    })
    
    if (result.success) {
      message.value = 'Регистрация прошла успешно! Добро пожаловать!'
      messageType.value = 'success'
      
      setTimeout(() => {
        router.push('/')
      }, 2000)
    } else {
      message.value = result.error || 'Ошибка регистрации'
      messageType.value = 'danger'
    }
  } catch (error) {
    message.value = 'Ошибка регистрации'
    messageType.value = 'danger'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  padding: 2rem 0;
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
}
</style>