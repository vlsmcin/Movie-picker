import { defineStore } from "pinia";
import movieService from "@/services/movieService";
import type { Movie, UserMovie } from "@/types/movie";

export const useUserMoviesStore = defineStore("movies", {
  state: () => ({
    userMovies: [] as Array<UserMovie>,
    isLoaded: false,
    isLoading: false,
  }),

  getters: {
    getMovieById: (state) => {
      return (id: string): UserMovie | undefined => {
        return state.userMovies.find((um) => String(um.movie.id) === String(id));
      } ;
    },
  },

  actions: {
    async addMovie(userMovie: UserMovie) {
      await movieService.addMovieForUser(userMovie).then((addedMovie) => {
        this.userMovies.push(addedMovie);
      });
    },
    async fetchMoviesIfEmpty(force = false) {
      if (this.isLoading) {
        return;
      }

      if (this.userMovies.length === 0 || force) {
        this.isLoading = true;
        try {
          const movies = await movieService.getMoviesForUser();
          this.userMovies = movies;
          this.isLoaded = true;
        } catch (error) {
          console.error("Failed to fetch movies:", error);
        } finally {
          this.isLoading = false;
        }
      }
    }
  },
});