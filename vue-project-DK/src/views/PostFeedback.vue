<template>
  <div class="post-feedback-page">
    <div class="container">
      <div class="success-container">
        <div class="success-icon">
          <img src="/images/cat.png" alt="Кошачий успех" class="success-image">
        </div>
        <h1>Сообщение отправлено!</h1>
        <p class="success-subtitle">
          Спасибо за ваше сообщение, <strong>{{ feedbackData.username }}</strong>! 
          Мы свяжемся с вами в ближайшее время.
        </p>
      </div>

      <div class="feedback-summary">
        <div class="summary-header">
          <h2>Данные вашего сообщения</h2>
          <p>Проверьте правильность введенной информации</p>
        </div>

        <div class="summary-content">
          <div class="summary-item">
            <div class="summary-label">
              <span class="label-icon">👤</span>
              <strong>Имя:</strong>
            </div>
            <div class="summary-value">{{ feedbackData.username }}</div>
          </div>

          <div class="summary-item">
            <div class="summary-label">
              <span class="label-icon">📧</span>
              <strong>Email:</strong>
            </div>
            <div class="summary-value">{{ feedbackData.usermail }}</div>
          </div>

          <div class="summary-item message-item">
            <div class="summary-label">
              <span class="label-icon">💬</span>
              <strong>Сообщение:</strong>
            </div>
            <div class="summary-value message-content">
              {{ feedbackData.textmess }}
            </div>
          </div>
        </div>
      </div>

      <div class="action-buttons">
        <router-link to="/feedback" class="btn btn-primary">
          📝 Отправить еще одно сообщение
        </router-link>
        <router-link to="/" class="btn btn-secondary">
          🏠 На главную
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
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 2rem;
}

.success-container {
  background: white;
  padding: 3rem 2rem;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  border: 1px solid #e9ecef;
  text-align: center;
  margin-bottom: 2rem;
}

.success-icon {
  margin-bottom: 1.5rem;
  animation: bounce 0.6s ease-in-out;
}

.success-image {
  width: 80px;
  height: 80px;
  object-fit: contain;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}

.success-container h1 {
  color: #2c3e50;
  font-size: 2.5rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.success-subtitle {
  color: #666;
  font-size: 1.2rem;
  line-height: 1.6;
  margin: 0;
}

.success-subtitle strong {
  color: #42b883;
}

.feedback-summary {
  background: white;
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  border: 1px solid #e9ecef;
  margin-bottom: 2rem;
}

.summary-header {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #f0f0f0;
}

.summary-header h2 {
  color: #2c3e50;
  font-size: 1.75rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.summary-header p {
  color: #666;
  font-size: 1rem;
  margin: 0;
}

.summary-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.summary-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  border-radius: 10px;
  background: #f8f9fa;
  transition: background-color 0.3s;
}

.summary-item:hover {
  background: #e9ecef;
}

.message-item {
  flex-direction: column;
  align-items: stretch;
}

.summary-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-width: 120px;
  font-size: 1rem;
  color: #2c3e50;
}

.label-icon {
  font-size: 1.2rem;
}

.summary-value {
  flex: 1;
  color: #2c3e50;
  font-size: 1rem;
  line-height: 1.5;
}

.message-content {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #e9ecef;
  white-space: pre-line;
  line-height: 1.6;
  margin-top: 0.5rem;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn {
  padding: 1rem 2rem;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 1rem;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s;
  cursor: pointer;
  text-align: center;
}

.btn-primary {
  background: #42b883;
  color: white;
}

.btn-primary:hover {
  background: #369870;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(66, 184, 131, 0.3);
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(108, 117, 125, 0.3);
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }
  
  .success-container {
    padding: 2rem 1.5rem;
  }
  
  .feedback-summary {
    padding: 2rem 1.5rem;
  }
  
  .success-container h1 {
    font-size: 2rem;
  }
  
  .success-image {
    width: 70px;
    height: 70px;
  }
  
  .summary-item {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .summary-label {
    min-width: auto;
  }
  
  .action-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .btn {
    width: 100%;
    max-width: 300px;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .success-container {
    padding: 1.5rem 1rem;
  }
  
  .feedback-summary {
    padding: 1.5rem 1rem;
  }
  
  .success-container h1 {
    font-size: 1.75rem;
  }
  
  .success-image {
    width: 60px;
    height: 60px;
  }
  
  .summary-header h2 {
    font-size: 1.5rem;
  }
  
  .message-content {
    padding: 1rem;
  }
}
</style>