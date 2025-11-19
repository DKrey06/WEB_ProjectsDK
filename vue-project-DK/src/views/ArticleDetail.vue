<template>
  <div class="article-detail">
    <div class="container mt-4">
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
        <button type="button" class="btn-close" @click="clearMessage"></button>
      </div>

      <article class="news-detail" v-if="article">
        <header class="mb-4 pb-3 border-bottom">
          <div class="d-flex justify-content-between align-items-start mb-3">
            <h1 class="display-6 mb-0 flex-grow-1">{{ article.title }}</h1>
            <div class="d-flex align-items-center gap-2 ms-3">
              <span v-if="isNewArticle" class="badge bg-success new-badge"
                >НОВОЕ</span
              >
              <div v-if="authStore.isAuthenticated" class="article-actions">
                <button @click="editArticle" class="btn btn-warning btn-sm">
                  ✏️ Редактировать
                </button>
                <button @click="deleteArticle" class="btn btn-danger btn-sm">
                  🗑️ Удалить
                </button>
              </div>
            </div>
          </div>
          <p class="text-muted mb-1">
            📅 Опубликовано: {{ formatDate(article.created_date) }}
          </p>
          <p class="text-muted mb-1">
            Автор: {{ article.author_name || article.author }}
          </p>
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
              <p class="text-muted small">
                Вы вошли как: <strong>{{ authStore.user?.name }}</strong>
              </p>
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
                  <div v-if="errors.text" class="invalid-feedback d-block">
                    {{ errors.text }}
                  </div>
                </div>
                <button
                  type="submit"
                  class="btn btn-primary"
                  :disabled="commentLoading || !commentForm.text.trim()"
                >
                  <span
                    v-if="commentLoading"
                    class="spinner-border spinner-border-sm me-2"
                  ></span>
                  {{ commentLoading ? "Отправка..." : "Отправить комментарий" }}
                </button>
              </form>
            </div>
          </div>

          <div v-else class="card mb-4">
            <div class="card-body text-center">
              <h5 class="card-title">Хотите оставить комментарий?</h5>
              <p class="text-muted">
                Войдите в систему, чтобы добавить комментарий к этой статье
              </p>
              <div class="d-flex gap-2 justify-content-center">
                <router-link
                  :to="`/login?redirect=/articles/${article.id}`"
                  class="btn btn-primary"
                >
                  Войти
                </router-link>
                <router-link
                  :to="`/register?redirect=/articles/${article.id}`"
                  class="btn btn-outline-primary"
                >
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
            <div
              v-for="comment in comments"
              :key="comment.id"
              class="card mb-3"
            >
              <div class="card-body">
                <div
                  class="d-flex justify-content-between align-items-start mb-2"
                >
                  <h6 class="card-subtitle mb-1 text-primary">
                    {{ comment.author_name }}
                  </h6>
                  <small class="text-muted">{{
                    formatDate(comment.date)
                  }}</small>
                </div>
                <p class="card-text">{{ comment.text }}</p>
                <div
                  v-if="
                    authStore.isAuthenticated &&
                    authStore.user?.id === comment.user_id
                  "
                  class="mt-2"
                >
                  <button
                    @click="editComment(comment)"
                    class="btn btn-sm btn-outline-warning me-2"
                    :disabled="commentLoading"
                  >
                    Редактировать
                  </button>
                  <button
                    @click="deleteComment(comment.id)"
                    class="btn btn-sm btn-outline-danger"
                    :disabled="commentLoading"
                  >
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

        <div class="mt-5 pt-3 border-top">
          <router-link to="/" class="btn btn-secondary">
            ← Вернуться на главную
          </router-link>
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
        <router-link to="/" class="btn btn-primary mt-3"
          >На главную</router-link
        >
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { articleService } from "@/services/articles";
import { commentService } from "@/services/comments";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const article = ref(null);
const comments = ref([]);
const loading = ref(true);
const commentsLoading = ref(false);
const commentLoading = ref(false);
const message = ref("");
const messageType = ref("");

const commentForm = reactive({
  text: "",
});

const errors = ref({});

const isNewArticle = computed(() => {
  if (!article.value) return false;
  const articleDate = new Date(article.value.created_date);
  const today = new Date();
  const diffTime = today - articleDate;
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
  return diffDays < 1;
});

const formatDate = (dateString) => {
  if (!dateString) return "";
  const date = new Date(dateString);
  return date.toLocaleDateString("ru-RU", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

const clearMessage = () => {
  message.value = "";
  messageType.value = "";
};

const showMessage = (text, type = "success") => {
  message.value = text;
  messageType.value = type;
};

const fetchArticle = async () => {
  try {
    loading.value = true;
    clearMessage();

    const articleId = parseInt(route.params.id);
    if (!articleId) {
      throw new Error("Неверный ID статьи");
    }

    const response = await articleService.getArticle(articleId);

    if (response.success) {
      article.value = response.article;
      await fetchComments();
    } else {
      throw new Error(response.error || "Статья не найдена");
    }
  } catch (error) {
    showMessage(
      error.response?.data?.error || error.message || "Статья не найдена",
      "danger"
    );
  } finally {
    loading.value = false;
  }
};

const fetchComments = async () => {
  try {
    commentsLoading.value = true;
    const articleId = parseInt(route.params.id);

    const response = await commentService.getComments();

    if (response.success) {
      comments.value = response.comments.filter(
        (comment) => comment.article_id === articleId
      );
    } else {
      throw new Error(response.error || "Ошибка загрузки комментариев");
    }
  } catch (error) {
    comments.value = [];
  } finally {
    commentsLoading.value = false;
  }
};

const addComment = async () => {
  errors.value = {};

  if (!commentForm.text.trim()) {
    errors.value.text = "Обязательно введите текст комментария";
    return;
  }

  if (commentForm.text.length > 1000) {
    errors.value.text = "Комментарий не должен превышать 1000 символов";
    return;
  }

  commentLoading.value = true;

  try {
    const commentData = {
      article_id: article.value.id,
      text: commentForm.text.trim(),
    };

    const response = await commentService.createComment(commentData);

    if (response.success) {
      showMessage("Комментарий успешно добавлен!", "success");
      commentForm.text = "";
      await fetchComments();
    } else {
      throw new Error(response.error || "Ошибка при создании комментария");
    }
  } catch (error) {
    showMessage(
      error.response?.data?.error ||
        error.message ||
        "Ошибка при добавлении комментария",
      "danger"
    );
  } finally {
    commentLoading.value = false;
  }
};

const editComment = async (comment) => {
  const newText = prompt("Редактировать комментарий:", comment.text);
  if (newText && newText.trim() !== comment.text) {
    try {
      commentLoading.value = true;
      const response = await commentService.updateComment(comment.id, {
        text: newText.trim(),
      });

      if (response.success) {
        showMessage("Комментарий успешно обновлен!", "success");
        await fetchComments();
      } else {
        throw new Error(response.error || "Ошибка при обновлении комментария");
      }
    } catch (error) {
      showMessage("Ошибка при редактировании комментария", "danger");
    } finally {
      commentLoading.value = false;
    }
  }
};

const deleteComment = async (commentId) => {
  if (!confirm("Вы уверены, что хотите удалить этот комментарий?")) {
    return;
  }

  try {
    commentLoading.value = true;
    const response = await commentService.deleteComment(commentId);

    if (response.success) {
      showMessage("Комментарий успешно удален!", "success");
      await fetchComments();
    } else {
      throw new Error(response.error || "Ошибка при удалении комментария");
    }
  } catch (error) {
    showMessage("Ошибка при удалении комментария", "danger");
  } finally {
    commentLoading.value = false;
  }
};

const editArticle = () => {
  router.push(`/edit-article/${article.value.id}`);
};

const deleteArticle = async () => {
  if (
    !confirm(
      "Вы уверены, что хотите удалить эту статью? Это действие нельзя отменить."
    )
  ) {
    return;
  }

  try {
    loading.value = true;
    const response = await articleService.deleteArticle(article.value.id);

    if (response.success) {
      showMessage("Статья успешно удалена!", "success");
      setTimeout(() => {
        router.push("/");
      }, 1500);
    } else {
      throw new Error(response.error || "Ошибка при удалении статьи");
    }
  } catch (error) {
    showMessage(
      error.response?.data?.error ||
        error.message ||
        "Ошибка при удалении статьи",
      "danger"
    );
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchArticle();
});
</script>

<style scoped>
.article-detail {
  min-height: calc(100vh - 80px);
  padding: 2rem 0;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 2rem;
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

.news-detail {
  background: white;
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid #e9ecef;
}

.display-6 {
  color: #2c3e50;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  line-height: 1.2;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.article-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.badge {
  font-size: 0.8rem;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
}

.bg-success {
  background: #42b883 !important;
}

.text-muted {
  color: #6c757d !important;
  margin-bottom: 0.5rem;
}

.article-content {
  line-height: 1.8;
  font-size: 1.1rem;
  color: #2c3e50;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.lead {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #2c3e50;
  white-space: pre-line;
  word-wrap: break-word;
  overflow-wrap: break-word;
  overflow: hidden;
  max-width: 100%;
}

.comments-section {
  border-top: 2px solid #e9ecef;
  padding-top: 2.5rem;
  margin-top: 2rem;
}

.comments-section h4 {
  color: #2c3e50;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.08);
  margin-bottom: 1.5rem;
}

.card-body {
  padding: 1.5rem;
}

.card-title {
  color: #2c3e50;
  font-weight: 600;
  margin-bottom: 1rem;
}

.form-label {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.75rem;
  display: block;
}

.form-control {
  border: 2px solid #e9ecef;
  border-radius: 10px;
  padding: 1rem;
  font-size: 1rem;
  transition: all 0.3s;
  width: 100%;
  box-sizing: border-box;
  word-wrap: break-word;
  overflow-wrap: break-word;
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
  min-height: 120px;
  resize: vertical;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  text-decoration: none;
  display: inline-block;
  cursor: pointer;
  transition: all 0.3s;
  margin-right: 0.5rem;
  margin-bottom: 0.5rem;
  white-space: nowrap;
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

.btn-warning {
  background: #ffc107;
  color: #212529;
}

.btn-warning:hover {
  background: #e0a800;
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

.btn-outline-warning {
  border: 2px solid #ffc107;
  color: #ffc107;
  background: transparent;
}

.btn-outline-warning:hover {
  background: #ffc107;
  color: #212529;
}

.btn-outline-danger {
  border: 2px solid #e74c3c;
  color: #e74c3c;
  background: transparent;
}

.btn-outline-danger:hover {
  background: #e74c3c;
  color: white;
}

.btn-outline-primary {
  border: 2px solid #42b883;
  color: #42b883;
  background: transparent;
}

.btn-outline-primary:hover {
  background: #42b883;
  color: white;
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.text-primary {
  color: #42b883 !important;
}

.card-subtitle {
  color: #42b883;
  font-weight: 600;
}

.border-top {
  border-top: 2px solid #e9ecef !important;
  padding-top: 2rem;
}

.spinner-border {
  color: #42b883;
}

.invalid-feedback {
  color: #e74c3c;
  font-size: 0.875rem;
  margin-top: 0.25rem;
  display: block;
}

.small {
  font-size: 0.875rem;
}

.card-text {
  word-wrap: break-word;
  overflow-wrap: break-word;
  white-space: pre-line;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }

  .news-detail {
    padding: 2rem 1.5rem;
  }

  .display-6 {
    font-size: 2rem;
  }

  .article-actions {
    justify-content: flex-start;
    margin-top: 1rem;
  }

  .btn {
    width: 100%;
    margin-right: 0;
  }
}

@media (max-width: 480px) {
  .news-detail {
    padding: 1.5rem 1rem;
  }

  .display-6 {
    font-size: 1.75rem;
  }

  .card-body {
    padding: 1.25rem;
  }

  .form-control {
    padding: 0.875rem;
  }

  .article-actions {
    flex-direction: column;
    width: 100%;
  }

  .article-actions .btn {
    width: 100%;
  }
}

.loading,
.error {
  text-align: center;
  padding: 3rem;
  font-size: 1.2rem;
  color: #666;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.new-badge {
  font-size: 0.8rem;
  padding: 0.25rem 0.5rem;
}

.flex-grow-1 {
  flex-grow: 1;
}
</style>
