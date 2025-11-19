import api from "./api";

export const commentService = {
  async getComments() {
    const response = await api.get("/api/comment");
    return response.data;
  },

  async createComment(commentData) {
    const response = await api.post("/api/comment", commentData);
    return response.data;
  },

  async updateComment(id, commentData) {
    const response = await api.put(`/api/comment/${id}`, commentData);
    return response.data;
  },

  async deleteComment(id) {
    const response = await api.delete(`/api/comment/${id}`);
    return response.data;
  },
};
