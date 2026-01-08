<script setup lang="ts">
    import HomeHeader from '@/components/HomeHeader.vue';
    import MovieCard from '@/components/MovieCard.vue';
</script>

<template>
    <HomeHeader />
    <MovieCard class="card" link="https://via.placeholder.com/150" moviename="Sample Movie" />
</template>

<style>
    .card {
        margin: 2rem auto;
    }
</style>