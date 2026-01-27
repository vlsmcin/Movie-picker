import { defineStore } from 'pinia'
import usersService from '@/services/usersService'

export const useUserAuthStore = defineStore('userAuth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    user: null as { name: string; email: string } | null,
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
  },

  actions: {
    async login(email: string, password: string) {
      try {
        const token = await usersService.login(email, password)
        this.token = token
        localStorage.setItem('token', token)
        this.user = { name: email, email }
      } catch (error) {
        throw new Error('Login failed')
      }
    },

    async register(name: string, email: string, password: string) {
      try {
        await usersService.register(name, email, password)
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