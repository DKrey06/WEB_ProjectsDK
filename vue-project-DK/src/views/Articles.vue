<template>
  <div class="articles-page">
    <div class="container">
      <h1>Все статьи</h1>
      <div class="filters-section">
        <div class="search-box">
          <div class="search-input-wrapper">
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Поиск по статьям..."
              class="search-input"
              @input="handleSearch"
            >
            <span class="search-icon">🔍</span>
          </div>
        </div>
        
        <div class="filters-row">
          <div class="filter-group">
            <label class="filter-label">Категория:</label>
            <select v-model="selectedCategory" @change="handleCategoryChange" class="filter-select">
              <option value="">Все категории</option>
              <option v-for="category in categories" :key="category" :value="category">
                {{ category }}
              </option>
            </select>
          </div>
          
          <div class="filter-group">
            <label class="filter-label">Сортировка:</label>
            <select v-model="sortBy" @change="handleSortChange" class="filter-select">
              <option value="newest">Сначала новые</option>
              <option value="oldest">Сначала старые</option>
            </select>
          </div>
          
          <button @click="clearFilters" class="btn-clear">
            Очистить фильтры
          </button>
        </div>
        
        <div v-if="searchQuery || selectedCategory" class="active-filters">
          <span class="active-filter" v-if="searchQuery">
            Поиск: "{{ searchQuery }}"
            <button @click="clearSearch" class="btn-remove-filter">×</button>
          </span>
          <span class="active-filter" v-if="selectedCategory">
            Категория: {{ selectedCategory }}
            <button @click="clearCategory" class="btn-remove-filter">×</button>
          </span>
        </div>
      </div>
      
      <div v-if="loading" class="loading">Загрузка...</div>
      
      <div v-else-if="articles.length === 0" class="no-articles">
        <p v-if="searchQuery || selectedCategory">Статьи по вашему запросу не найдены</p>
        <p v-else>Пока нет статей</p>
        <button @click="clearFilters" class="btn-primary" v-if="searchQuery || selectedCategory">
          Показать все статьи
        </button>
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
          <p class="article-preview">{{ getArticlePreview(article.text) }}</p>
          <div class="article-footer">
            <span class="article-author">Автор: {{ article.author }}</span>
            <router-link :to="`/articles/${article.id}`" class="btn-read">
              Читать далее →
            </router-link>
          </div>
        </div>
      </div>

      <div v-if="articles.length > 0 && !loading" class="pagination">
        <p class="results-count">Найдено статей: {{ articles.length }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { articleService } from '@/services/articles';
import { debounce } from '@/utils/helpers';

const articles = ref([]);
const categories = ref([]);
const loading = ref(true);
const searchQuery = ref('');
const selectedCategory = ref('');
const sortBy = ref('newest');

const isNewArticle = (article) => {
  const articleDate = new Date(article.created_date);
  const today = new Date();
  const diffTime = today - articleDate;
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
  return diffDays < 1;
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('ru-RU');
};

const getArticlePreview = (text) => {
  return text.slice(0, 150) + (text.length > 150 ? '...' : '');
};

const fetchCategories = async () => {
  try {
    const response = await articleService.getCategories();
    if (response.success) {
      categories.value = response.categories;
    }
  } catch (error) {
    console.error('Ошибка загрузки категорий:', error);
    try {
      const articlesResponse = await articleService.getArticles();
      if (articlesResponse.success) {
        const uniqueCategories = [...new Set(articlesResponse.articles.map(article => article.category))];
        categories.value = uniqueCategories;
      }
    } catch (fallbackError) {
      console.error('Ошибка fallback загрузки категорий:', fallbackError);
    }
  }
};

const fetchArticles = async () => {
  try {
    loading.value = true;
    let response;

    if (searchQuery.value) {
      response = await articleService.searchArticles(searchQuery.value);
    } else if (selectedCategory.value) {
      response = await articleService.getArticlesByCategory(selectedCategory.value);
    } else {
      response = await articleService.getArticles();
    }

    if (response.success) {
      let articlesData = response.articles || [];
      
      if (sortBy.value === 'oldest') {
        articlesData.sort((a, b) => new Date(a.created_date) - new Date(b.created_date));
      } else {
        articlesData.sort((a, b) => new Date(b.created_date) - new Date(a.created_date));
      }

      articles.value = articlesData;
    } else {
      articles.value = [];
    }
  } catch (error) {
    console.error('Ошибка загрузки статей:', error);
    articles.value = [];
  } finally {
    loading.value = false;
  }
};

const handleSearch = debounce(() => {
  fetchArticles();
}, 500);

const handleCategoryChange = () => {
  fetchArticles();
};

const handleSortChange = () => {
  fetchArticles();
};

const clearFilters = () => {
  searchQuery.value = '';
  selectedCategory.value = '';
  sortBy.value = 'newest';
  fetchArticles();
};

const clearSearch = () => {
  searchQuery.value = '';
  fetchArticles();
};

const clearCategory = () => {
  selectedCategory.value = '';
  fetchArticles();
};

onMounted(async () => {
  await fetchCategories();
  await fetchArticles();
});
</script>

<style scoped>
.articles-page {
  padding: 2rem 0;
  min-height: calc(100vh - 80px);
  background: #f8f9fa;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

h1 {
  color: #2c3e50;
  margin-bottom: 2rem;
  text-align: center;
  font-size: 2.5rem;
}

.filters-section {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

.search-box {
  margin-bottom: 1rem;
}

.search-input-wrapper {
  position: relative;
  max-width: 400px;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s;
}

.search-input:focus {
  border-color: #42b883;
  box-shadow: 0 0 0 3px rgba(66, 184, 131, 0.1);
  outline: none;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
}

.filters-row {
  display: flex;
  gap: 1rem;
  align-items: end;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-label {
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.9rem;
}

.filter-select {
  padding: 0.5rem;
  border: 2px solid #e9ecef;
  border-radius: 6px;
  font-size: 0.9rem;
  min-width: 150px;
  background: white;
}

.filter-select:focus {
  border-color: #42b883;
  outline: none;
}

.btn-clear {
  background: transparent;
  color: #666;
  border: 1px solid #ddd;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s;
  margin-left: auto;
}

.btn-clear:hover {
  background: #f8f9fa;
  color: #e74c3c;
  border-color: #e74c3c;
}

.active-filters {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #f0f0f0;
}

.active-filter {
  background: #42b883;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.btn-remove-filter {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 1rem;
  padding: 0;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.btn-remove-filter:hover {
  background: rgba(255,255,255,0.2);
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
  display: flex;
  flex-direction: column;
  height: 100%;
}

.article-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0,0,0,0.15);
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

.pagination {
  text-align: center;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #eee;
}

.results-count {
  color: #666;
  font-size: 0.9rem;
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
  border: none;
  cursor: pointer;
}

.btn-primary:hover {
  background: #369870;
}

@media (max-width: 768px) {
  .articles-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .article-card {
    padding: 1.25rem;
  }
  
  .filters-row {
    flex-direction: column;
    align-items: stretch;
  }
  
  .btn-clear {
    margin-left: 0;
    align-self: flex-start;
  }
  
  .search-input-wrapper {
    max-width: none;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 0 1rem;
  }
  
  .article-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .new-badge {
    align-self: flex-start;
  }
}
</style>