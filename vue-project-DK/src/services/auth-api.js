import api from "./api";
import Cookies from "js-cookie";

export const authService = {
  async login(email, password) {
    const response = await api.post("/api/auth/login", {
      email,
      password,
    });
    return response.data;
  },

  async register(userData) {
    const response = await api.post("/api/auth/register", userData);
    return response.data;
  },

  async refreshToken() {
    const refreshToken = Cookies.get("refresh_token");
    const response = await api.post(
      "/api/auth/refresh",
      {},
      {
        headers: {
          Authorization: `Bearer ${refreshToken}`,
        },
      }
    );
    return response.data;
  },

  async verifyToken() {
    const response = await api.post("/api/auth/verify");
    return response.data;
  },

  async logout() {
    const response = await api.post("/api/auth/logout");
    return response.data;
  },
};
