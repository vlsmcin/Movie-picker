import { createRouter, createWebHistory } from 'vue-router'
import MovieListView from '@/views/MovieListView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import MovieView from '@/views/MovieView.vue'
import { useUserMoviesStore } from '@/stores/movies'
import { useUserAuthStore } from '@/stores/user'

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
      path: '/movie/:movieId',
      name: 'movie',
      component: MovieView,
      meta: { requiresAuth: true },
      beforeEnter: async(to) => {
        const moviesStore = useUserMoviesStore();

        await moviesStore.fetchMoviesIfEmpty();
        console.log("Movies in store before entering movie route:", moviesStore.userMovies);

        const id = to.params.movieId as string;
        const movie = moviesStore.getMovieById(id);

        console.log("Before entering movie route, movie found:", movie);

        if (!movie) {
          return { name: 'not-found' };
        }
      }
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

router.beforeEach(async (to) => {
  const auth = useUserAuthStore();

  if (!auth.initialized) {
    await auth.tryRestoreSession();
  }

  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return '/login'
  } else if (to.path === '/login' && auth.isLoggedIn) {
    return '/watchlist'
  }
})

export default router
