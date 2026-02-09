import { defineStore } from 'pinia'
import usersService from '@/services/usersService'

export const useUserAuthStore = defineStore('userAuth', {
  state: () => ({
    token: localStorage.getItem('access') || '',
    user: null as { username: string; email: string } | null,
    initialized: false,
  }),

  getters: {
    isLoggedIn: (state) => {
      return !!state.token || !!localStorage.getItem('refresh');
    },
  },

  actions: {
    async login(username: string, password: string) {
      try {
        const token = await usersService.login(username, password)
        this.token = token.access
        localStorage.setItem('access', token.access)
        localStorage.setItem('refresh', token.refresh)
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

    async tryRestoreSession() {
      const refresh = localStorage.getItem('refresh')
      if (!refresh) {
        this.initialized = true
        return
      }

      try {
        const res = await usersService.refresh(refresh)
        this.token = res.access
        localStorage.setItem('access', res.access)
      } catch (error) {
        this.logout()
      } finally {
        this.initialized = true
      }
    },

    logout() {
      this.token = ''
      this.user = null
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      localStorage.clear()
    },
  },
})