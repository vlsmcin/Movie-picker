import { defineStore } from "pinia";
import movieService from "@/services/movieService";
import type { Movie } from "@/types/movie";

export const useMoviesStore = defineStore("movies", {
  state: () => ({
    movies: [] as Array<Movie>,
  }),

  getters: {
    getAllMovies: (state) => state.movies,
    getMoviesByGenre: (state) => (genre: string) =>
      state.movies.filter((movie) => movie.genres.includes(genre)),
  },

  actions: {
    async addMovie(movie: Movie): Promise<any> {
      const response = await movieService.addMovieForUser(movie).then((addedMovie) => {
        this.movies.push(addedMovie);
      });
      return response;
    },

    async fetchMoviesByTitle(title: string) {
      this.movies = await movieService.getMoviesByTitle(title);
    }
  },
});