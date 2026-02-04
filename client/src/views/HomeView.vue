<script setup lang="ts">
    import HomeHeader from '@/components/HomeHeader.vue';
    import MovieCard from '@/components/MovieCard.vue';
    import movieService from '@/services/movieService';
    import AddMovie from '@/components/AddMovie.vue';
    import type { Movie } from '@/types/movie';
    import { onMounted, ref, computed } from 'vue';
    import type { UserMovie } from '@/types/movie';
    import { useRoute } from 'vue-router';

    const userMovies = ref<Array<UserMovie>>([]);
    const genres = ref<Set<string>>(new Set());
    const route = useRoute();
    const inWatchListOption = computed(() => route.name === 'home' ? true : false);
    
    const filteredMovies = computed(() => {
        return userMovies.value.filter(um =>
            um.watched === !inWatchListOption.value &&
            um.in_watchlist === inWatchListOption.value
        );
    });

    console.log("In watchlist option:", inWatchListOption.value);
    
    function getGenresFromMovies(movies: Array<Movie>): Set<string> {
        const genresSet = new Set<string>();
        
        if (!inWatchListOption.value) {
            movies = movies.filter(movie => {
                return userMovies.value.some(um => um.movie.id === movie.id && um.watched);
            });
        }
        else {
            movies = movies.filter(movie => {
                return userMovies.value.some(um => um.movie.id === movie.id && um.in_watchlist);
            });
        }
        
        movies.forEach(movie => {
            movie.genres.forEach(genre => genresSet.add(genre));
        });
        return genresSet;
    }

    onMounted(async () => {
        const moviesData = await movieService.getMoviesForUser();
        userMovies.value = moviesData;
        genres.value = getGenresFromMovies(moviesData.map(m => m.movie));
    });
</script>

<template>
    <HomeHeader />
    <div v-for="genre in genres" :key="genre">
        <h2 class="section-title">{{ genre }}</h2>
        <div class="card">
            <MovieCard
                v-for="userMovie in filteredMovies.filter(
                    um => um.movie.genres.includes(genre)
                    )"
                :key="userMovie.movie.id"
                :link="`https://image.tmdb.org/t/p/w200${userMovie.movie.poster_path}`"
                :moviename="userMovie.movie.title"
                />
        </div>
    </div>
    <AddMovie/>
</template>

<style>
    .card {
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        gap: 1rem;
        padding: 1rem 2rem;
        overflow-x: auto;
    }

    .section-title {
        margin: 2rem;
        border-bottom: 2px solid rgba(0, 128, 0, 0.2);
    }
</style>