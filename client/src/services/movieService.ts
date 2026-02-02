import type { Movie } from "@/types/movie";
import api from "./axios";

class movieService {
    public static async getMoviesForUser(): Promise<Movie[]> {
        try {
            const response = await api.get(`/me/movies`)
            return response.data;
        } catch (error) {
            console.error("Error fetching movies for user:", error);
            throw error;
        }
    }

    public static async addMovieForUser(movie: Movie): Promise<Movie> {
        try {
            const response = await api.post(`/me/movies`, movie.id);
            return response.data;
        } catch (error) {
            console.error("Error adding movie for user:", error);
            throw error;
        }
    }

    public static async getMoviesByTitle(title: string): Promise<Movie[]> {
        try {
            const response = await api.get(`?title=${encodeURIComponent(title)}`);
            return response.data;
        } catch (error) {
            console.error("Error fetching movies by title:", error);
            throw error;
        }
    }
}

export default movieService;