<template>
  <div class="articles-page">
    <div class="container">
      <h1>Все статьи</h1>
      
      <div v-if="loading" class="loading">Загрузка...</div>
      
      <div v-else-if="articles.length === 0" class="no-articles">
        <p>Пока нет статей</p>
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
import { articleService } from '@/services/articles';

const articles = ref([]);
const loading = ref(true);

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('ru-RU');
};

const fetchArticles = async () => {
  try {
    loading.value = true;
    const response = await articleService.getArticles();
    articles.value = response.articles;
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
.articles-page {
  padding: 2rem 0;
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
</style>