<template>
  <div class="edit-article-page">
    <div class="container">
      <h1>Редактирование статьи</h1>
      <p>Внесите изменения в статью</p>

      <div v-if="message" :class="['alert', messageType === 'success' ? 'alert-success' : 'alert-danger', 'alert-dismissible fade show']" role="alert">
        {{ message }}
        <button type="button" class="btn-close" @click="message = ''"></button>
      </div>

      <div v-if="loading" class="text-center py-4">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Загрузка...</span>
        </div>
        <div class="mt-2">Загрузка статьи...</div>
      </div>

      <form v-else @submit.prevent="handleSubmit">
        <div class="form-list">
          <div class="mb-3">
            <label class="form-label">Заголовок статьи:</label>
            <input 
              class="form-control" 
              :class="{ 'is-invalid': errors.title }"
              type="text" 
              v-model="form.title"
              maxlength="200"
              placeholder="Введите заголовок статьи"
            >
            <div v-if="errors.title" class="invalid-feedback">{{ errors.title }}</div>
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
            <div v-if="errors.category" class="invalid-feedback">{{ errors.category }}</div>
            <div class="form-text">
              Или введите новую категорию:
              <input 
                type="text" 
                class="form-control" 
                v-model="form.newCategory" 
                placeholder="Введите новую категорию"
              >
            </div>
          </div>

          <div class="mb-3">
            <label class="form-label">Текст статьи:</label>
            <textarea 
              class="form-control" 
              :class="{ 'is-invalid': errors.text }"
              v-model="form.text"
              rows="12"
              placeholder="Напишите текст вашей статьи..."
            ></textarea>
            <div v-if="errors.text" class="invalid-feedback">{{ errors.text }}</div>
          </div>
          
          <div class="mb-3 d-flex gap-2">
            <button type="submit" class="btn btn-primary" :disabled="submitting">
              {{ submitting ? 'Сохранение...' : 'Сохранить изменения' }}
            </button>
            <router-link :to="`/articles/${articleId}`" class="btn btn-secondary">Отмена</router-link>
            <button type="button" @click="deleteArticle" class="btn btn-danger ms-auto">
              Удалить статью
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { articleService } from '@/services/articles'

const route = useRoute()
const router = useRouter()

const articleId = route.params.id
const form = reactive({
  title: '',
  category: '',
  newCategory: '',
  text: ''
})

const errors = ref({})
const loading = ref(true)
const submitting = ref(false)
const message = ref('')
const messageType = ref('')

const fetchArticle = async () => {
  try {
    loading.value = true
    const response = await articleService.getArticle(articleId)
    
    if (response.success) {
      const article = response.article
      form.title = article.title
      form.category = article.category
      form.text = article.text
    } else {
      throw new Error(response.error || 'Статья не найдена')
    }
  } catch (error) {
    message.value = error.response?.data?.error || 'Ошибка загрузки статьи'
    messageType.value = 'danger'
  } finally {
    loading.value = false
  }
}

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

  submitting.value = true
  message.value = ''

  try {
    const articleData = {
      title: form.title,
      text: form.text,
      category: form.newCategory || form.category
    }

    const response = await articleService.updateArticle(articleId, articleData)
    
    message.value = 'Статья успешно обновлена!'
    messageType.value = 'success'
    
    setTimeout(() => {
      router.push(`/articles/${articleId}`)
    }, 1000)

  } catch (error) {
    message.value = error.response?.data?.error || 'Ошибка обновления статьи'
    messageType.value = 'danger'
  } finally {
    submitting.value = false
  }
}

const deleteArticle = async () => {
  if (!confirm('Вы уверены, что хотите удалить эту статью? Это действие нельзя отменить.')) {
    return
  }

  try {
    submitting.value = true
    const response = await articleService.deleteArticle(articleId)
    
    if (response.success) {
      message.value = 'Статья успешно удалена!'
      messageType.value = 'success'
      
      setTimeout(() => {
        router.push('/')
      }, 1500)
    } else {
      throw new Error(response.error || 'Ошибка при удалении статьи')
    }
  } catch (error) {
    message.value = error.response?.data?.error || 'Ошибка удаления статьи'
    messageType.value = 'danger'
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchArticle()
})
</script>

<style scoped>
.edit-article-page {
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
  margin-bottom: 0.5rem;
  font-size: 2.5rem;
  font-weight: 700;
  text-align: center;
}

p {
  color: #666;
  margin-bottom: 2rem;
  font-size: 1.1rem;
  text-align: center;
}

.form-list {
  background: white;
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  border: 1px solid #e9ecef;
}

.form-label {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.75rem;
  display: block;
  font-size: 1.1rem;
}

.form-control {
  border: 2px solid #e9ecef;
  border-radius: 10px;
  padding: 1rem;
  font-size: 1rem;
  transition: all 0.3s;
  width: 100%;
  box-sizing: border-box;
  margin-bottom: 0.5rem;
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

select.form-control {
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 1rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 3rem;
}

textarea.form-control {
  min-height: 250px;
  resize: vertical;
  line-height: 1.6;
}

.form-text {
  color: #6c757d;
  font-size: 0.9rem;
  margin-top: 0.5rem;
  margin-bottom: 1rem;
}

.form-text .form-control {
  margin-top: 0.5rem;
  margin-bottom: 0;
}

.btn {
  padding: 0.875rem 2rem;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 1rem;
  text-decoration: none;
  display: inline-block;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background: #42b883;
  color: white;
}

.btn-primary:hover {
  background: #369870;
  transform: translateY(-1px);
  box-shadow: 0 5px 15px rgba(66, 184, 131, 0.3);
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
  transform: translateY(-1px);
}

.btn-danger {
  background: #e74c3c;
  color: white;
}

.btn-danger:hover {
  background: #c0392b;
  transform: translateY(-1px);
}

.btn:disabled {
  background: #a0a0a0;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
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

.invalid-feedback {
  color: #e74c3c;
  font-size: 0.875rem;
  margin-top: 0.25rem;
  display: block;
}

.d-flex.gap-2 {
  gap: 1rem;
}

.ms-auto {
  margin-left: auto;
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }
  
  .form-list {
    padding: 2rem 1.5rem;
  }
  
  h1 {
    font-size: 2rem;
  }
  
  .d-flex.gap-2 {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
    margin-bottom: 1rem;
  }
  
  .ms-auto {
    margin-left: 0;
  }
}

@media (max-width: 480px) {
  .form-list {
    padding: 1.5rem 1rem;
  }
  
  h1 {
    font-size: 1.75rem;
  }
  
  .form-control {
    padding: 0.875rem;
  }
}
</style>