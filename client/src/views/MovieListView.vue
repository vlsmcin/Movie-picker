<script setup lang="ts">
    import HomeHeader from '@/components/HomeHeader.vue';
    import MovieCard from '@/components/MovieCard.vue';
    import AddMovie from '@/components/AddMovie.vue';
    import type { Movie } from '@/types/movie';
    import { onMounted, computed } from 'vue';
    import { useUserMoviesStore } from '@/stores/movies';
    import { useRoute } from 'vue-router';

    const userMoviesStore = useUserMoviesStore();
    const userMovies = computed(() => userMoviesStore.userMovies);
    const genres = computed(() => 
        getGenresFromMovies(userMovies.value.map(um => um.movie))
    );
    const route = useRoute();
    const inWatchListOption = computed(() => route.name === 'watchlist' ? true : false);
    
    const filteredMovies = computed(() => {
        return userMovies.value.filter(um =>
            inWatchListOption.value ? um.in_watchlist : um.watched
        );
    });

    const emptyMessage = computed(() => {
        return inWatchListOption.value ? "Nenhum filme na lista de desejos" : "Nenhum filme assistido";
    });

    
    function getGenresFromMovies(movies: Array<Movie>): Set<string> {
        const genresSet = new Set<string>();
        
        filteredMovies.value.forEach(um => {
            um.movie.genres.forEach(genre => genresSet.add(genre));
        });

        return genresSet;
    }

    onMounted(async () => {
        await userMoviesStore.fetchMoviesIfEmpty();
    });
</script>

<template>
    <HomeHeader />
    <h2 id="Central" v-if="filteredMovies.length === 0">{{ emptyMessage }}</h2>
    <div v-for="genre in genres" :key="genre">
        <h2 class="section-title">{{ genre }}</h2>
        <div class="cards">
            <MovieCard
                v-for="userMovie in filteredMovies.filter(
                    um => um.movie.genres.includes(genre)
                    )"
                :key="userMovie.movie.id"
                :link="`https://image.tmdb.org/t/p/w200${userMovie.movie.poster_path}`"
                :movie="userMovie.movie"
                />
        </div>
    </div>
    <AddMovie/>
</template>

<style scoped>
    .cards {
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

    #Central {
        text-align: center;
        margin-top: 3rem;
        color: gray;
    }
</style>