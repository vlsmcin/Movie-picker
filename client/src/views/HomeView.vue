<script setup lang="ts">
    import HomeHeader from '@/components/HomeHeader.vue';
    import MovieCard from '@/components/MovieCard.vue';
    import movieService from '@/services/movieService';

    onload = async () => {
        const movies = await movieService.getMoviesForUser("userId");
        console.log(movies);
    }
</script>

<template>
    <HomeHeader />
    <h2 class="section-title">Thriller</h2>
    <MovieCard class="card" link="https://image.tmdb.org/t/p/w500/a26cQPRhJPX6GbWfQbvZdrrp9j9.jpg" moviename="Clube da Luta" />
</template>

<style>
    .card {
        margin: 2rem auto;
    }

    .section-title {
        margin: 2rem;
        border-bottom: 2px solid rgba(0, 128, 0, 0.2);
    }
</style>