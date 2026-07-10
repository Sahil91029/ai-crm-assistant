import axios from "axios";

const api = axios.create({
  baseURL: "https://ai-crm-assistant-vrp7.onrender.com",
});

export default api;