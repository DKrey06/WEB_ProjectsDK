import api from "./api";

export const articleService = {
  async getArticles() {
    const response = await api.get("/api/articles");
    return response.data;
  },

  async getArticle(id) {
    const response = await api.get(`/api/articles/${id}`);
    return response.data;
  },

  async createArticle(articleData) {
    const response = await api.post("/api/articles", articleData);
    return response.data;
  },

  async updateArticle(id, articleData) {
    const response = await api.put(`/api/articles/${id}`, articleData);
    return response.data;
  },

  async deleteArticle(id) {
    const response = await api.delete(`/api/articles/${id}`);
    return response.data;
  },

  async getArticlesByCategory(category) {
    const response = await api.get(`/api/articles/category/${category}`);
    return response.data;
  },

  async searchArticles(query) {
    const response = await api.get(
      `/api/articles/search?q=${encodeURIComponent(query)}`
    );
    return response.data;
  },

  async getArticlesSorted(sortType) {
    const response = await api.get(`/api/articles/sort/${sortType}`);
    return response.data;
  },

  async getCategories() {
    const response = await api.get("/api/categories");
    return response.data;
  },
  async updateArticle(id, articleData) {
    const response = await api.put(`/api/articles/${id}`, articleData);
    return response.data;
  },

  async deleteArticle(id) {
    const response = await api.delete(`/api/articles/${id}`);
    return response.data;
  },
};
