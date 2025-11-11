<template>
  <div class="login-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-12 col-md-10 col-lg-12">
          <div class="card shadow">
            <div class="card-body p-5">
              <h1 class="card-title text-center mb-4">Вход в систему</h1>

              <div v-if="message" :class="['alert', messageType === 'success' ? 'alert-success' : 'alert-danger', 'alert-dismissible fade show']" role="alert">
                {{ message }}
                <button type="button" class="btn-close" @click="message = ''"></button>
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
                  >
                  <div v-if="errors.email" class="invalid-feedback d-block">{{ errors.email }}</div>
                </div>

                <div class="mb-3">
                  <label class="form-label">Пароль:</label>
                  <input 
                    class="form-control" 
                    :class="{ 'is-invalid': errors.password }"
                    type="password" 
                    v-model="form.password"
                  >
                  <div v-if="errors.password" class="invalid-feedback d-block">{{ errors.password }}</div>
                </div>

                <div v-if="errors.login" class="alert alert-danger">{{ errors.login }}</div>

                <div class="d-grid gap-2">
                  <button type="submit" class="btn btn-primary btn-lg" :disabled="loading">
                    {{ loading ? 'Вход...' : 'Войти' }}
                  </button>
                </div>
              </form>

              <div class="text-center mt-4">
                <p>Нет аккаунта? <router-link to="/register">Зарегистрируйтесь</router-link></p>
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
  email: '',
  password: ''
})

const errors = ref({})
const loading = ref(false)
const message = ref('')
const messageType = ref('')

const handleLogin = async () => {
  errors.value = {}
  loading.value = true
  message.value = ''

  // Валидация
  if (!form.email) {
    errors.value.email = 'Обязательно введите email'
  }
  if (!form.password) {
    errors.value.password = 'Обязательно введите пароль'
  }

  if (Object.keys(errors.value).length > 0) {
    loading.value = false
    return
  }

  try {
    const result = await authStore.login(form)
    
    if (result.success) {
      message.value = 'Успешный вход!'
      messageType.value = 'success'
      setTimeout(() => {
        router.push('/')
      }, 1000)
    } else {
      errors.value.login = result.error || 'Ошибка входа'
      messageType.value = 'danger'
    }
  } catch (error) {
    errors.value.login = 'Ошибка сервера'
    messageType.value = 'danger'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  padding: 2rem 0;
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
}
</style>