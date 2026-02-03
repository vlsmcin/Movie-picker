import type { Movie } from "@/types/movie";
import api from "./axios";

class movieService {
    public static async getMoviesForUser(): Promise<Movie[]> {
        try {
            const response = await api.get(`/users/me/movies/`);
            return response.data;
        } catch (error) {
            console.error("Error fetching movies for user:", error);
            throw error;
        }
    }

    public static async addMovieForUser(movie: Movie, watched: boolean, in_watchlist: boolean): Promise<Movie> {
        try {
            const response = await api.post(`/users/me/movies/`, {
                movie_id: movie.id,
                watched: watched,
                in_watchlist: in_watchlist
            });
            
            return response.data;
        } catch (error) {
            console.error("Error adding movie for user:", error);
            throw error;
        }
    }

    public static async getMoviesByTitle(title: string): Promise<Movie[]> {
        try {
            const response = await api.get(`/movies/${encodeURIComponent(title)}`);
            return response.data;
        } catch (error) {
            console.error("Error fetching movies by title:", error);
            throw error;
        }
    }
}

export default movieService;