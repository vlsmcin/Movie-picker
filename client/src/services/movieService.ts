import type { Movie } from "@/types/movie";

class movieService {
    private static apiUrl = 'http://localhost:8000/api/movies'

    public static getMoviesForUser(userId: string): Promise<Movie[]> {
        return fetch(`${this.apiUrl}/user/${userId}`).then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch movies');
            }
            return response.json();
        });
    }
}

export default movieService;