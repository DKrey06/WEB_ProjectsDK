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
        <router-link v-if="authStore.isAuthenticated" to="/create-article" class="btn-primary">
          Создать первую статью
        </router-link>
      </div>

      <div v-else class="articles-grid">
        <div v-for="article in articles" :key="article.id" class="article-card">
          <h3>{{ article.title }}</h3>
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
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { articleService } from '@/services/articles';

const articles = ref([]);
const loading = ref(true);
const authStore = useAuthStore();

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('ru-RU');
};

const fetchArticles = async () => {
  try {
    loading.value = true;
    const response = await articleService.getArticles();
    articles.value = response.articles.slice(0, 6);
  } catch (error) {
    console.error('Ошибка загрузки статей:', error);
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
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.article-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0,0,0,0.15);
}

.article-card h3 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
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
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
}

.article-author {
  color: #888;
  font-size: 0.9rem;
}

.btn-read {
  color: #42b883;
  text-decoration: none;
  font-weight: 500;
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
</style>