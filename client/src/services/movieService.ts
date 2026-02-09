import type { Movie, UserMovie } from "@/types/movie";
import { api } from "./axios";

class movieService {
    public static async getMoviesForUser(): Promise<UserMovie[]> {
        try {
            const response = await api.get(`/users/me/movies/`);
            return response.data;
        } catch (error) {
            console.error("Error fetching movies for user:", error);
            throw error;
        }
    }

    public static async addMovieForUser(userMovie: UserMovie): Promise<UserMovie> {
        try {
            const response = await api.post(`/users/me/movies/`, {
                movie_id: userMovie.movie.id,
                watched: userMovie.watched,
                in_watchlist: userMovie.in_watchlist
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

    public static async updateUserMovie(userMovie: UserMovie): Promise<UserMovie> {
        try {
            const response = await api.patch(`/users/me/movies/`, {
                movie_id: userMovie.movie.id,
                watched: userMovie.watched,
                in_watchlist: userMovie.in_watchlist
            });
            
            return response.data;
        } catch (error) {
            console.error("Error updating user movie:", error);
            throw error;
        }
    }
}

export default movieService;