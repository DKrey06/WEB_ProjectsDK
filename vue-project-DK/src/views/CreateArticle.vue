<template>
  <div class="create-article-page">
    <div class="container">
      <h1>Создание новой статьи</h1>
      <p>Заполните форму для создания статьи</p>

      <div v-if="message" :class="['alert', messageType === 'success' ? 'alert-success' : 'alert-danger', 'alert-dismissible fade show']" role="alert">
        {{ message }}
        <button type="button" class="btn-close" @click="message = ''"></button>
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="form-list">
          <div class="mb-3">
            <label class="form-label">Заголовок статьи:</label>
            <input 
              class="form-control" 
              :class="{ 'is-invalid': errors.title }"
              type="text" 
              v-model="form.title"
              maxlength="200"
            >
            <div v-if="errors.title" class="invalid-feedback d-block">{{ errors.title }}</div>
          </div>

          <div class="mb-3">
            <label class="form-label">Категория:</label>
            <select 
              class="form-control" 
              :class="{ 'is-invalid': errors.category }"
              v-model="form.category"
            >
              <option value="">Выберите категорию</option>
              <option value="Технологии">Технологии</option>
              <option value="Медицина">Медицина</option>
              <option value="Общее">Общее</option>
              <option value="Наука">Наука</option>
              <option value="Спорт">Спорт</option>
            </select>
            <div v-if="errors.category" class="invalid-feedback d-block">{{ errors.category }}</div>
            <div class="form-text">
              Или введите новую категорию:
              <input 
                type="text" 
                class="form-control mt-1" 
                v-model="form.newCategory" 
                placeholder="Новая категория"
              >
            </div>
          </div>

          <div class="mb-3">
            <label class="form-label">Текст статьи:</label>
            <textarea 
              class="form-control" 
              :class="{ 'is-invalid': errors.text }"
              v-model="form.text"
              rows="10"
            ></textarea>
            <div v-if="errors.text" class="invalid-feedback d-block">{{ errors.text }}</div>
          </div>
          
          <div class="mb-3">
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? 'Создание...' : 'Создать статью' }}
            </button>
            <router-link to="/" class="btn btn-secondary ms-2">Отмена</router-link>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { articleService } from '@/services/articles'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  title: '',
  category: '',
  newCategory: '',
  text: ''
})

const errors = ref({})
const loading = ref(false)
const message = ref('')
const messageType = ref('')

const validateForm = () => {
  errors.value = {}

  if (!form.title) {
    errors.value.title = 'Обязательно введите заголовок'
  }

  if (!form.category && !form.newCategory) {
    errors.value.category = 'Обязательно выберите или введите категорию'
  }

  if (!form.text) {
    errors.value.text = 'Обязательно введите текст статьи'
  }

  return Object.keys(errors.value).length === 0
}

const handleSubmit = async () => {
  if (!validateForm()) {
    return
  }

  loading.value = true
  message.value = ''

  try {
    const articleData = {
      title: form.title,
      text: form.text,
      category: form.newCategory || form.category
    }

    const response = await articleService.createArticle(articleData)
    
    message.value = 'Статья успешно создана!'
    messageType.value = 'success'
    
    setTimeout(() => {
      router.push(`/articles/${response.article.id}`)
    }, 1000)

  } catch (error) {
    message.value = error.response?.data?.error || 'Ошибка создания статьи'
    messageType.value = 'danger'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.create-article-page {
  padding: 2rem 0;
  min-height: calc(100vh - 80px);
}
</style>