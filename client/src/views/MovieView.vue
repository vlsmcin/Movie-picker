<script setup lang="ts">
    import { computed, ref } from 'vue';
    import type { Movie } from '@/types/movie';
    import { useUserMoviesStore } from '@/stores/movies';
    import { useRoute } from 'vue-router';

    const moviesStore = useUserMoviesStore();
    const route = useRoute();
    const userMovie = computed(() => 
            moviesStore.getMovieById(String(route.params.movieId))
        )

    const handleWatchlist = (option: boolean) => {
        if (userMovie.value) {
            const tempUserMovie = {
                movie: userMovie.value.movie,
                in_watchlist: option,
                watched: userMovie.value.watched
            }
            moviesStore.updateUserMovie(tempUserMovie);
        }
    };

    const handleWatched = (option: boolean) => {
        if (userMovie.value) {
            const tempUserMovie = {
                movie: userMovie.value.movie,
                in_watchlist: userMovie.value.in_watchlist,
                watched: option
            }
            moviesStore.updateUserMovie(tempUserMovie);
        }
    };
</script>

<template>
    <div class="Movie-view">
        <img :src="`https://image.tmdb.org/t/p/w1280/${userMovie?.movie?.backdrop_path}`" />
        <div class="movie-meta">
            <span id="grade">Nota: {{ userMovie?.movie?.vote_average.toFixed(1) }}/10⭐</span>
            <p>Ano de lançamento: {{ userMovie?.movie?.release_date.substring(0, 4) }}</p>
        </div>
        <div class="genres-names">
            <p>Gêneros:</p>
            <span class="genre" v-for="(genre, i) in userMovie?.movie?.genres" :key="genre">
                <span>{{ genre }}<span class="commas" v-if="i < userMovie!.movie!.genres.length - 1">, </span></span>
            </span>
        </div>
        <div class="action-button">
            <button v-if="!userMovie?.in_watchlist" :class="'add-button'" @click="() => handleWatchlist(true)">Adicionar à lista de desejos</button>
            <button v-if="userMovie?.in_watchlist" :class="'remove-button'" @click="() => handleWatchlist(false)">Remover da lista de desejos</button>
            <button v-if="!userMovie?.watched" class="add-button" @click="() => handleWatched(true)">Marcar como assistido</button>
            <button v-if="userMovie?.watched" class="remove-button" @click="() => handleWatched(false)">Desmarcar como assistido</button>
        </div>
        <h1>{{ userMovie?.movie?.title }}</h1>
        <p>{{ userMovie?.movie?.overview }}</p>
    </div>
</template>

<style scoped>
    .Movie-view {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 80%;
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
    }

    .movie-meta {
        display: flex;
        flex-direction: row;
        justify-content: center;
        gap: 2rem;
    }

    img {
        width: 100%;
        height: auto;
        border-radius: 10px;
        margin-bottom: 1rem;
    }

    span {
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }

    #grade {
        color: #0c8006;
    }

    .genres-names {
        display: flex;
        flex-direction: row;
        gap: 0.5rem;
        margin-bottom: 0.25rem;
    }

    .genre {
        color: #d1be12;
    }

    .commas {
        color: var(--color-text);
    }

    .action-button {
        display: flex;
        flex-direction: row;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    h1 {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        font-weight: bold;
    }

    p {
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
        text-align: justify;
    }

    .add-button {
        background-color: #0c8006;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
    }

    .remove-button {
        background-color: #c91414;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
    }
</style>