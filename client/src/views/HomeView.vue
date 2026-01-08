<script setup lang="ts">
    import HomeHeader from '@/components/HomeHeader.vue';
    import MovieCard from '@/components/MovieCard.vue';
</script>

<template>
    <HomeHeader />
    <MovieCard class="card" link="https://image.tmdb.org/t/p/w500/a26cQPRhJPX6GbWfQbvZdrrp9j9.jpg" moviename="Clube da Luta" />
</template>

<style>
    .card {
        margin: 2rem auto;
    }
</style>