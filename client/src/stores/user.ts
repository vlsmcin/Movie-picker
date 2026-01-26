import { defineStore } from 'pinia'
import authService from '@/services/authService'

export const useUserAuthStore = defineStore('userAuth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    user: null as { name: string; email: string } | null,
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
  },

  actions: {
    async login(username: string, email: string, password: string) {
      try {
        const token = await authService.login(username, email, password)
        this.token = token
        localStorage.setItem('token', token)
        this.user = { name: username, email }
      } catch (error) {
        throw new Error('Login failed')
      }
    },

    logout() {
      this.token = ''
      this.user = null
      localStorage.removeItem('token')
    },
  },
})