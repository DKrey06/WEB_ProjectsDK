<template>
  <div class="home">
    <div class="hero">
      <h1>Добро пожаловать в Новостной Блог!</h1>
      <p>Актуальные новости на различные темы</p>
    </div>

    <div class="container">
      <h2>Последние статьи</h2>

      <div v-if="loading" class="loading">Загрузка...</div>

      <div v-else-if="articles.length === 0" class="no-articles">
        <p>Пока нет статей</p>
        <router-link
          v-if="authStore.isAuthenticated"
          to="/create-article"
          class="btn-primary"
        >
          Создать первую статью
        </router-link>
      </div>

      <div v-else class="articles-grid">
        <div v-for="article in articles" :key="article.id" class="article-card">
          <div class="article-header">
            <h3>{{ article.title }}</h3>
            <span v-if="isNewArticle(article)" class="new-badge">НОВОЕ</span>
          </div>
          <p class="article-meta">
            {{ formatDate(article.created_date) }} • {{ article.category }}
          </p>
          <p class="article-preview">{{ article.text.slice(0, 150) }}...</p>
          <div class="article-footer">
            <span class="article-author">Автор: {{ article.author }}</span>
            <router-link :to="`/articles/${article.id}`" class="btn-read">
              Читать далее →
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
import { articleService } from "@/services/articles";

const articles = ref([]);
const loading = ref(true);
const authStore = useAuthStore();

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString("ru-RU");
};

const isNewArticle = (article) => {
  const articleDate = new Date(article.created_date);
  const today = new Date();
  const diffTime = today - articleDate;
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
  return diffDays < 1;
};

const fetchArticles = async () => {
  try {
    loading.value = true;
    const response = await articleService.getArticles();
    articles.value = response.articles.slice(0, 6);
  } catch (error) {
    console.error("Ошибка загрузки статей:", error);
    articles.value = [];
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchArticles();
});
</script>

<style scoped>
.home {
  min-height: calc(100vh - 80px);
  padding-bottom: 5rem;
}

.hero {
  background: linear-gradient(135deg, #42b883 0%, #35495e 100%);
  color: white;
  text-align: center;
  padding: 4rem 2rem;
  margin-bottom: 3rem;
}

.hero h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.hero p {
  font-size: 1.2rem;
  opacity: 0.9;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.article-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
}

.article-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
}

.article-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.article-card h3 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-size: 1.25rem;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

.new-badge {
  background: #42b883;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
  flex-shrink: 0;
  margin-top: 0.25rem;
}

.article-meta {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.article-preview {
  color: #555;
  line-height: 1.5;
  margin-bottom: 1rem;
  flex-grow: 1;
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 6em;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
  padding-top: 1rem;
  border-top: 1px solid #f0f0f0;
}

.article-author {
  color: #888;
  font-size: 0.9rem;
}

.btn-read {
  color: #42b883;
  text-decoration: none;
  font-weight: 500;
  white-space: nowrap;
}

.btn-read:hover {
  text-decoration: underline;
}

.loading {
  text-align: center;
  padding: 3rem;
  font-size: 1.2rem;
  color: #666;
}

.no-articles {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.btn-primary {
  display: inline-block;
  background: #42b883;
  color: white;
  padding: 0.75rem 1.5rem;
  text-decoration: none;
  border-radius: 6px;
  margin-top: 1rem;
  font-weight: 500;
}

.btn-primary:hover {
  background: #369870;
}

/* Адаптивность */
@media (max-width: 768px) {
  .articles-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .article-card {
    padding: 1.25rem;
  }

  .article-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .new-badge {
    align-self: flex-start;
  }

  .hero {
    padding: 3rem 1rem;
  }

  .hero h1 {
    font-size: 2rem;
  }

  .hero p {
    font-size: 1.1rem;
  }

  .home {
    padding-bottom: 2rem;
  }
}
</style>
