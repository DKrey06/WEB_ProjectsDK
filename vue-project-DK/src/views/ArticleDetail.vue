<template>
  <div class="article-detail">
    <div class="container mt-4">
      <nav aria-label="breadcrumb" class="mb-4">
        <ol class="breadcrumb">
          <li class="breadcrumb-item">
            <router-link to="/" class="text-decoration-none">Главная</router-link>
          </li>
          <li class="breadcrumb-item active">{{ article?.title }}</li>
        </ol>
      </nav>

      <div v-if="message" :class="['alert', messageType === 'success' ? 'alert-success' : 'alert-danger', 'alert-dismissible fade show']" role="alert">
        {{ message }}
        <button type="button" class="btn-close" @click="clearMessage"></button>
      </div>

      <article class="news-detail" v-if="article">
        <header class="mb-4 pb-3 border-bottom">
          <div class="d-flex justify-content-between align-items-start">
            <h1 class="display-6 mb-2">{{ article.title }}</h1>
            <span v-if="isNewArticle" class="badge bg-success ms-3 new-badge">НОВОЕ</span>
          </div>
          <p class="text-muted mb-0">
            📅 Опубликовано: {{ formatDate(article.created_date) }}
          </p>
          <p class="text-muted mb-0">Автор: {{ article.author_name || article.author }}</p>
          <p class="text-muted mb-0">Категория: {{ article.category }}</p>
        </header>

        <div class="article-content mb-5">
          <p class="lead">{{ article.text }}</p>
        </div>

        <div class="comments-section mt-5">
          <h4 class="mb-4">Комментарии ({{ comments.length }})</h4>

          <div v-if="authStore.isAuthenticated" class="card mb-4">
            <div class="card-body">
              <h5 class="card-title">Добавить комментарий</h5>
              <p class="text-muted small">Вы вошли как: <strong>{{ authStore.user?.name }}</strong></p>
              <form @submit.prevent="addComment">
                <div class="mb-3">
                  <label class="form-label">Текст комментария:</label>
                  <textarea 
                    class="form-control" 
                    :class="{ 'is-invalid': errors.text }"
                    v-model="commentForm.text"
                    rows="4" 
                    placeholder="Введите ваш комментарий..."
                    :disabled="commentLoading"
                  ></textarea>
                  <div v-if="errors.text" class="invalid-feedback d-block">{{ errors.text }}</div>
                </div>
                <button type="submit" class="btn btn-primary" :disabled="commentLoading || !commentForm.text.trim()">
                  <span v-if="commentLoading" class="spinner-border spinner-border-sm me-2"></span>
                  {{ commentLoading ? 'Отправка...' : 'Отправить комментарий' }}
                </button>
              </form>
            </div>
          </div>

          <div v-else class="card mb-4">
            <div class="card-body text-center">
              <h5 class="card-title">Хотите оставить комментарий?</h5>
              <p class="text-muted">Войдите в систему, чтобы добавить комментарий к этой статье</p>
              <div class="d-flex gap-2 justify-content-center">
                <router-link :to="`/login?redirect=/articles/${article.id}`" class="btn btn-primary">
                  Войти
                </router-link>
                <router-link :to="`/register?redirect=/articles/${article.id}`" class="btn btn-outline-primary">
                  Зарегистрироваться
                </router-link>
              </div>
            </div>
          </div>

          <div v-if="commentsLoading" class="text-center py-4">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Загрузка комментариев...</span>
            </div>
          </div>

          <div v-else-if="comments.length > 0">
            <div v-for="comment in comments" :key="comment.id" class="card mb-3">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start mb-2">
                  <h6 class="card-subtitle mb-1 text-primary">{{ comment.author_name }}</h6>
                  <small class="text-muted">{{ formatDate(comment.date) }}</small>
                </div>
                <p class="card-text">{{ comment.text }}</p>
                <div v-if="canEditComment(comment)" class="mt-2">
                  <button @click="editComment(comment)" class="btn btn-sm btn-outline-warning me-2" :disabled="commentLoading">
                    Редактировать
                  </button>
                  <button @click="deleteComment(comment.id)" class="btn btn-sm btn-outline-danger" :disabled="commentLoading">
                    Удалить
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-4">
            <p class="text-muted">Пока нет комментариев. Будьте первым!</p>
          </div>
        </div>

        <div class="mt-5 pt-3 border-top d-flex justify-content-between">
          <router-link to="/" class="btn btn-secondary">
            ← Вернуться
          </router-link>
          <div v-if="canEditArticle">
            <button @click="editArticle" class="btn btn-warning">
              Редактировать статью
            </button>
          </div>
        </div>
      </article>

      <div v-else-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Загрузка статьи...</span>
        </div>
        <div class="mt-2">Загрузка статьи...</div>
      </div>

      <div v-else class="text-center py-5">
        <div class="error alert alert-danger">Статья не найдена</div>
        <router-link to="/" class="btn btn-primary mt-3">На главную</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { articleService } from '@/services/articles'
import { commentService } from '@/services/comments'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const article = ref(null)
const comments = ref([])
const loading = ref(true)
const commentsLoading = ref(false)
const commentLoading = ref(false)
const message = ref('')
const messageType = ref('')

const commentForm = reactive({
  text: ''
})

const errors = ref({})

const isNewArticle = computed(() => {
  if (!article.value) return false
  const articleDate = new Date(article.value.created_date)
  const today = new Date()
  const diffTime = today - articleDate
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))
  return diffDays < 1
})

const canEditArticle = computed(() => {
  return authStore.isAuthenticated && article.value && authStore.user?.id === article.value.author_id
})

const canEditComment = (comment) => {
  return authStore.isAuthenticated && authStore.user?.id === comment.user_id
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const clearMessage = () => {
  message.value = ''
  messageType.value = ''
}

const showMessage = (text, type = 'success') => {
  message.value = text
  messageType.value = type
}

const fetchArticle = async () => {
  try {
    loading.value = true
    clearMessage()
    
    const articleId = parseInt(route.params.id)
    if (!articleId) {
      throw new Error('Неверный ID статьи')
    }

    const response = await articleService.getArticle(articleId)
    
    if (response.success) {
      article.value = response.article
      await fetchComments()
    } else {
      throw new Error(response.error || 'Статья не найдена')
    }
  } catch (error) {
    console.error('Ошибка загрузки статьи:', error)
    showMessage(error.response?.data?.error || error.message || 'Статья не найдена', 'danger')
  } finally {
    loading.value = false
  }
}

const fetchComments = async () => {
  try {
    commentsLoading.value = true
    const articleId = parseInt(route.params.id)
    
    const response = await commentService.getComments()
    
    if (response.success) {
      comments.value = response.comments.filter(comment => 
        comment.article_id === articleId
      )
    } else {
      throw new Error(response.error || 'Ошибка загрузки комментариев')
    }
  } catch (error) {
    console.error('Ошибка загрузки комментариев:', error)
    console.error('Детали ошибки:', error.response?.data)
    comments.value = []
  } finally {
    commentsLoading.value = false
  }
}

const addComment = async () => {
  errors.value = {}
  
  if (!commentForm.text.trim()) {
    errors.value.text = 'Обязательно введите текст комментария'
    return
  }

  if (commentForm.text.length > 1000) {
    errors.value.text = 'Комментарий не должен превышать 1000 символов'
    return
  }

  commentLoading.value = true
  
  try {
    const commentData = {
      article_id: article.value.id,
      text: commentForm.text.trim()
    }

    console.log('Отправка комментария:', commentData)

    const response = await commentService.createComment(commentData)
    
    if (response.success) {
      showMessage('Комментарий успешно добавлен!', 'success')
      commentForm.text = ''
      await fetchComments()
    } else {
      throw new Error(response.error || 'Ошибка при создании комментария')
    }
  } catch (error) {
    console.error('Ошибка при добавлении комментария:', error)
    console.error('Детали ошибки:', error.response?.data)
    
    if (error.response?.data?.errors) {
      errors.value = error.response.data.errors
    } else {
      showMessage(error.response?.data?.error || error.message || 'Ошибка при добавлении комментария', 'danger')
    }
  } finally {
    commentLoading.value = false
  }
}

const editComment = async (comment) => {
  const newText = prompt('Редактировать комментарий:', comment.text)
  if (newText && newText.trim() !== comment.text) {
    try {
      commentLoading.value = true
      const response = await commentService.updateComment(comment.id, { 
        text: newText.trim() 
      })
      
      if (response.success) {
        showMessage('Комментарий успешно обновлен!', 'success')
        await fetchComments()
      } else {
        throw new Error(response.error || 'Ошибка при обновлении комментария')
      }
    } catch (error) {
      console.error('Ошибка при обновлении комментария:', error)
      showMessage(error.response?.data?.error || error.message || 'Ошибка при обновлении комментария', 'danger')
    } finally {
      commentLoading.value = false
    }
  }
}

const deleteComment = async (commentId) => {
  if (!confirm('Вы уверены, что хотите удалить этот комментарий?')) {
    return
  }

  try {
    commentLoading.value = true
    const response = await commentService.deleteComment(commentId)
    
    if (response.success) {
      showMessage('Комментарий успешно удален!', 'success')
      await fetchComments()
    } else {
      throw new Error(response.error || 'Ошибка при удалении комментария')
    }
  } catch (error) {
    console.error('Ошибка при удалении комментария:', error)
    showMessage(error.response?.data?.error || error.message || 'Ошибка при удалении комментария', 'danger')
  } finally {
    commentLoading.value = false
  }
}

const editArticle = () => {
  router.push(`/edit-article/${article.value.id}`)
}

onMounted(() => {
  fetchArticle()
})
</script>

<style scoped>
.article-detail {
  min-height: calc(100vh - 80px);
  padding-bottom: 2rem;
}

.loading, .error {
  text-align: center;
  padding: 3rem;
  font-size: 1.2rem;
  color: #666;
}

.new-badge {
  font-size: 0.8rem;
  padding: 0.25rem 0.5rem;
}

.comments-section {
  border-top: 1px solid #eee;
  padding-top: 2rem;
}

.article-content {
  line-height: 1.8;
  font-size: 1.1rem;
}
</style>