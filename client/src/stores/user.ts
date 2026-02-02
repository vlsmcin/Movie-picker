import { defineStore } from 'pinia'
import usersService from '@/services/usersService'

export const useUserAuthStore = defineStore('userAuth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    user: null as { username: string; email: string } | null,
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
  },

  actions: {
    async login(username: string, password: string) {
      try {
        const token = await usersService.login(username, password)
        this.token = token
        localStorage.setItem('token', token)
        this.user = { username, email: '' }
      } catch (error) {
        throw new Error('Login failed')
      }
    },

    async register(username: string, email: string, password: string) {
      try {
        await usersService.register(username, email, password)
      } catch (error) {
        throw new Error('Registration failed')
      }
    },

    logout() {
      this.token = ''
      this.user = null
      localStorage.removeItem('token')
    },
  },
})