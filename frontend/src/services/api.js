import axios from 'axios'

const API_BASE = 'http://localhost:8000'

// create an axios instance pointing to our FastAPI backend
const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json'
  }
})

// automatically attach JWT token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const getGithubLoginUrl = () => api.get('/auth/github/login')
export const getRepos = () => api.get('/repos/')

export default api