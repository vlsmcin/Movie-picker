<script setup lang="ts">
    import { onMounted, ref } from 'vue';
    import { useRoute } from 'vue-router';
    import type { Movie } from '@/types/movie';
    import { useUserMoviesStore } from '@/stores/movies';
    import router from '@/router';

    const movie = ref<Movie>()
    const moviesStore = useUserMoviesStore();

    onMounted(async () => {
        const route = useRoute();
        const movieId = route.params.movieId as string;

        await moviesStore.fetchMoviesIfEmpty();

        const moviesFetched = moviesStore.getMovieById(movieId);

        if (!moviesFetched) {
            router.replace({name: 'not found'});
            return;
        }

        movie.value = moviesFetched.movie;
    });
</script>

<template>
    <image-viewer v-if="movie" :image-url="`https://image.tmdb.org/t/p/w1280/${movie.backdrop_path}`" />
    <span>{{ movie?.vote_average }}</span>
    <h1>{{ movie?.title }}</h1>
    <p>{{ movie?.overview }}</p>
    <p>Release Date: {{ movie?.release_date }}</p>
</template>

<style scoped>

</style>