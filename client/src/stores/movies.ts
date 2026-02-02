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
    getMovieByTitle: (state) => (title: string) =>
      state.movies.find((movie) => movie.title === title),
  },

  actions: {
    addMovie(movie: Movie) {
      movieService.addMovieForUser(movie).then((addedMovie) => {
        this.movies.push(addedMovie);
      });
    },

    //removeMovie(movieId: string) {
    //  
    //},

    async fetchMoviesForUser() {
      this.movies = await movieService.getMoviesForUser();
    }
  },
});