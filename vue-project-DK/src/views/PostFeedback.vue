<template>
  <div class="post-feedback-page">
    <div class="container">
      <div class="alert alert-success" role="alert">
        <h4 class="alert-heading">Сообщение успешно отправлено!</h4>
        <p>Спасибо за ваше сообщение, <strong>{{ feedbackData.username }}</strong>! Мы свяжемся с вами в ближайшее время.</p>
      </div>

      <div class="card mt-4">
        <div class="card-header">
          <h5>Данные вашего сообщения:</h5>
        </div>
        <div class="card-body">
          <div class="row mb-3">
            <div class="col-md-2"><strong>Имя:</strong></div>
            <div class="col-md-10">{{ feedbackData.username }}</div>
          </div>
          <div class="row mb-3">
            <div class="col-md-2"><strong>Email:</strong></div>
            <div class="col-md-10">{{ feedbackData.usermail }}</div>
          </div>
          <div class="row">
            <div class="col-md-2"><strong>Сообщение:</strong></div>
            <div class="col-md-10">
              <div class="border p-3 bg-light rounded">
                {{ feedbackData.textmess }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-4">
        <router-link to="/feedback" class="btn btn-primary">
          Отправить еще одно сообщение
        </router-link>
        <router-link to="/" class="btn btn-secondary ms-2">
          На главную
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const feedbackData = ref({
  username: '',
  usermail: '',
  textmess: ''
})

onMounted(() => {
  feedbackData.value = {
    username: route.query.username || '',
    usermail: route.query.usermail || '',
    textmess: route.query.textmess || ''
  }
})
</script>

<style scoped>
.post-feedback-page {
  padding: 2rem 0;
  min-height: calc(100vh - 80px);
}
</style>