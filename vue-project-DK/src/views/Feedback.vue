<template>
  <div class="feedback-page">
    <div class="container">
      <h1>Обратная связь</h1>
      <p class="page-subtitle">Мы ценим ваше мнение и всегда готовы помочь</p>

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
        <button type="button" class="btn-close" @click="message = ''"></button>
      </div>

      <div class="feedback-wrapper">
        <div class="feedback-box">
          <div class="feedback-header">
            <h2>Напишите нам</h2>
            <p>Заполните форму ниже, и мы ответим вам в ближайшее время</p>
          </div>

          <form @submit.prevent="handleSubmit" class="feedback-form">
            <div class="form-group">
              <label class="form-label">Ваше имя:</label>
              <input
                class="form-control"
                :class="{ 'is-invalid': errors.username }"
                type="text"
                v-model="form.username"
                maxlength="30"
                placeholder="Введите ваше имя"
              />
              <div v-if="errors.username" class="invalid-feedback">
                {{ errors.username }}
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Электронная почта:</label>
              <input
                class="form-control"
                :class="{ 'is-invalid': errors.usermail }"
                type="email"
                v-model="form.usermail"
                maxlength="50"
                placeholder="Введите ваш email"
              />
              <div v-if="errors.usermail" class="invalid-feedback">
                {{ errors.usermail }}
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Текст сообщения:</label>
              <textarea
                class="form-control"
                :class="{ 'is-invalid': errors.textmess }"
                v-model="form.textmess"
                rows="6"
                placeholder="Опишите ваш вопрос или предложение..."
              ></textarea>
              <div v-if="errors.textmess" class="invalid-feedback">
                {{ errors.textmess }}
              </div>
              <div class="form-text">Максимум 1000 символов</div>
            </div>

            <div class="form-actions">
              <button type="submit" class="btn btn-primary" :disabled="loading">
                <span v-if="loading" class="spinner"></span>
                {{ loading ? "Отправка..." : "Отправить сообщение" }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const form = reactive({
  username: "",
  usermail: "",
  textmess: "",
});

const errors = ref({});
const loading = ref(false);
const message = ref("");
const messageType = ref("");

const validateForm = () => {
  errors.value = {};

  if (!form.username.trim()) {
    errors.value.username = "Обязательно введите имя";
  } else if (form.username.trim().length < 2) {
    errors.value.username = "Имя должно содержать минимум 2 символа";
  }

  if (!form.usermail.trim()) {
    errors.value.usermail = "Обязательно введите email";
  } else {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailPattern.test(form.usermail)) {
      errors.value.usermail = "Введите корректный email адрес";
    }
  }

  if (!form.textmess.trim()) {
    errors.value.textmess = "Обязательно введите сообщение";
  } else if (form.textmess.length > 1000) {
    errors.value.textmess = "Сообщение не должно превышать 1000 символов";
  }

  return Object.keys(errors.value).length === 0;
};

const handleSubmit = async () => {
  if (!validateForm()) {
    return;
  }

  loading.value = true;

  try {
    setTimeout(() => {
      message.value =
        "Сообщение успешно отправлено! Спасибо за обратную связь.";
      messageType.value = "success";
      loading.value = false;

      setTimeout(() => {
        router.push({
          name: "post-feedback",
          query: {
            username: form.username,
            usermail: form.usermail,
            textmess: form.textmess,
          },
        });
      }, 1000);
    }, 1000);
  } catch (error) {
    message.value = "Ошибка при отправке сообщения";
    messageType.value = "danger";
    loading.value = false;
  }
};
</script>

<style scoped>
.feedback-page {
  padding: 2rem 0;
  min-height: calc(100vh - 80px);
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding-bottom: 5rem;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 2rem;
}

h1 {
  color: #2c3e50;
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.page-subtitle {
  text-align: center;
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 3rem;
}

.feedback-wrapper {
  display: flex;
  justify-content: center;
}

.feedback-box {
  background: white;
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid #e9ecef;
  width: 100%;
  max-width: 600px;
}

.feedback-header {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #f0f0f0;
}

.feedback-header h2 {
  color: #2c3e50;
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.feedback-header p {
  color: #666;
  font-size: 1rem;
  line-height: 1.5;
}

.feedback-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-label {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.75rem;
  font-size: 1rem;
}

.form-control {
  border: 2px solid #e9ecef;
  border-radius: 10px;
  padding: 1rem;
  font-size: 1rem;
  transition: all 0.3s;
  width: 100%;
  box-sizing: border-box;
  font-family: inherit;
}

.form-control:focus {
  border-color: #42b883;
  box-shadow: 0 0 0 3px rgba(66, 184, 131, 0.1);
  outline: none;
}

.form-control.is-invalid {
  border-color: #e74c3c;
  box-shadow: 0 0 0 3px rgba(231, 76, 60, 0.1);
}

textarea.form-control {
  resize: vertical;
  min-height: 120px;
  line-height: 1.5;
}

.form-text {
  color: #6c757d;
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

.invalid-feedback {
  color: #e74c3c;
  font-size: 0.875rem;
  margin-top: 0.5rem;
  display: block;
}

.form-actions {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
}

.btn {
  padding: 1rem 2rem;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
  min-width: 200px;
  position: relative;
}

.btn-primary {
  background: #42b883;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #369870;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(66, 184, 131, 0.3);
}

.btn-primary:disabled {
  background: #a0a0a0;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.spinner {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border: 2px solid transparent;
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-right: 0.5rem;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.alert {
  border-radius: 10px;
  border: none;
  margin-bottom: 2rem;
  padding: 1.25rem;
}

.alert-success {
  background: rgba(66, 184, 131, 0.1);
  color: #2c3e50;
  border-left: 4px solid #42b883;
}

.alert-danger {
  background: rgba(231, 76, 60, 0.1);
  color: #2c3e50;
  border-left: 4px solid #e74c3c;
}

.alert-dismissible .btn-close {
  padding: 1rem;
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }

  .feedback-box {
    padding: 2rem 1.5rem;
  }

  h1 {
    font-size: 2rem;
  }
}

@media (max-width: 480px) {
  .feedback-box {
    padding: 1.5rem 1rem;
  }

  .form-control {
    padding: 0.875rem;
  }

  .btn {
    padding: 0.875rem 1.5rem;
    min-width: auto;
    width: 100%;
  }
}
</style>
