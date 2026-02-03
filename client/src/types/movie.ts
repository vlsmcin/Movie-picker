export type Movie = {
    id: string;
    title: string;
    overview: string;
    vote_average: number;
    release_date: string;
    poster_path: string;
    genres: string[];
    watched: boolean;
    in_watchlist: boolean;
}