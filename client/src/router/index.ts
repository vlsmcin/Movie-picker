import { createRouter, createWebHistory } from 'vue-router'
import MovieListView from '@/views/MovieListView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/watchlist',
      name: 'watchlist',
      component: MovieListView,
      meta: { requiresAuth: true },
    },
    {
      path: '/watched',
      name: 'watched',
      component: MovieListView,
      meta: { requiresAuth: true },
    },
    {
      path: '/pickmovie',
      name: 'pickmovie',
      component: MovieListView,
      meta: { requiresAuth: true },
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
  ],
})

router.beforeEach((to, from, next) => {
  const isLogged = localStorage.getItem('refresh')

  if (to.meta.requiresAuth && !isLogged) {
    next('/login')
  } else if (to.path === '/login' && isLogged) {
    next('/watchlist')
  } else {
    next()
  }
})

export default router
