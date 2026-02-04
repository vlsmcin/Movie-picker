import { defineStore } from "pinia";
import movieService from "@/services/movieService";
import type { Movie, UserMovie } from "@/types/movie";

export const useUserMoviesStore = defineStore("movies", {
  state: () => ({
    userMovies: [] as Array<UserMovie>,
    isLoaded: false,
    isLoading: false,
  }),

  actions: {
    async addMovie(userMovie: UserMovie) {
      await movieService.addMovieForUser(userMovie).then((addedMovie) => {
        this.userMovies.push(addedMovie);
      });
    },
    async fetchMoviesIfEmpty(force = false) {
      if (this.userMovies.length === 0 || force) {
        try {
          const movies = await movieService.getMoviesForUser();
          this.userMovies = movies;
        } catch (error) {
          console.error("Failed to fetch movies:", error);
        }
      }
    }
  },
});