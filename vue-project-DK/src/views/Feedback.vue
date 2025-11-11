<template>
  <div class="feedback-page">
    <div class="container">
      <h1>Обратная связь</h1>
      <p>Заполните форму для обратной связи</p>

      <div v-if="message" :class="['alert', messageType === 'success' ? 'alert-success' : 'alert-danger', 'alert-dismissible fade show']" role="alert">
        {{ message }}
        <button type="button" class="btn-close" @click="message = ''"></button>
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="form-list">
          <div class="mb-3">
            <label class="form-label">Ваше имя:</label>
            <input 
              class="form-control" 
              :class="{ 'is-invalid': errors.username }"
              type="text" 
              v-model="form.username"
              maxlength="30"
            >
            <div v-if="errors.username" class="invalid-feedback d-block">{{ errors.username }}</div>
          </div>
          
          <div class="mb-3">
            <label class="form-label">Электронная почта:</label>
            <input 
              class="form-control" 
              :class="{ 'is-invalid': errors.usermail }"
              type="email" 
              v-model="form.usermail"
              maxlength="50"
            >
            <div v-if="errors.usermail" class="invalid-feedback d-block">{{ errors.usermail }}</div>
          </div>
          
          <div class="mb-3">
            <label class="form-label">Текст сообщения:</label>
            <textarea 
              class="form-control" 
              :class="{ 'is-invalid': errors.textmess }"
              v-model="form.textmess"
              rows="5"
            ></textarea>
            <div v-if="errors.textmess" class="invalid-feedback d-block">{{ errors.textmess }}</div>
          </div>
          
          <div class="mb-3">
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? 'Отправка...' : 'Отправить сообщение' }}
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const form = reactive({
  username: '',
  usermail: '',
  textmess: ''
})

const errors = ref({})
const loading = ref(false)
const message = ref('')
const messageType = ref('')

const validateForm = () => {
  errors.value = {}

  if (!form.username.trim()) {
    errors.value.username = 'Обязательно введите имя'
  }

  if (!form.usermail.trim()) {
    errors.value.usermail = 'Обязательно введите email'
  } else {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
    if (!emailPattern.test(form.usermail)) {
      errors.value.usermail = 'Введите корректный email адрес'
    }
  }

  if (!form.textmess.trim()) {
    errors.value.textmess = 'Обязательно введите сообщение'
  }

  return Object.keys(errors.value).length === 0
}

const handleSubmit = async () => {
  if (!validateForm()) {
    return
  }

  loading.value = true

  try {
    // TODO: Реализовать отправку на бэкенд когда будет API
    // await feedbackService.sendFeedback(form)
    
    // Временно симулируем успешную отправку
    setTimeout(() => {
      message.value = 'Сообщение успешно отправлено! Спасибо за обратную связь.'
      messageType.value = 'success'
      loading.value = false

      setTimeout(() => {
        router.push({
          name: 'post-feedback',
          query: {
            username: form.username,
            usermail: form.usermail,
            textmess: form.textmess
          }
        })
      }, 1000)
    }, 1000)

  } catch (error) {
    message.value = 'Ошибка при отправке сообщения'
    messageType.value = 'danger'
    loading.value = false
  }
}
</script>

<style scoped>
.feedback-page {
  padding: 2rem 0;
  min-height: calc(100vh - 80px);
}
</style>