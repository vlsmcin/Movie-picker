<script setup lang="ts">
    import type { Movie } from '@/types/movie';

    defineProps<{
        link:string,
        movie: Movie
    }>()
</script>

<template>
    <RouterLink :to="`/movie/${movie.id}`" class="card">
        <img class="movie-image" :src="link"/>
        <p class="movie-text">{{ movie.title }}</p>
    </RouterLink>
</template>

<style scoped>
    .card {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 12.5rem;
        border: 2px solid var(--color-border);
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }

    .movie-image {
        width: 100%;
        height: 80%;
        border-radius: 5px;
        margin-bottom: 1rem;
        margin-top: 1rem;
    }

    .movie-text {
        margin-bottom: 1rem;
        font-size: 1rem;
        font-weight: bold;
        text-align: center;
        color: var(--color-text);
    }
</style>