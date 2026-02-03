<script lang="ts" setup>
    import router from '@/router';
    import { ref, watch } from 'vue';
    import type { Movie } from '@/types/movie';
    import { useMoviesStore } from '@/stores/movies';
    import Toast from './Toast.vue';

    const showMovieModal = ref(false);
    const actualPage = router.currentRoute.value.name;
    const selectedMovies = ref<Movie[]>([]);
    const moviesStore = useMoviesStore();
    const isMovieSelected = ref(false);
    const searchTitle = ref('');
    const searchResults = ref<Movie[]>([]);

    let timeout: ReturnType<typeof setTimeout>;

    const successFullAdd = ref(false);
    const failedAdd = ref(false);

    watch(searchTitle, (newTitle) => {
        clearTimeout(timeout);

        if (!newTitle.trim()) {
            searchResults.value = [];
            return;
        }

        timeout = setTimeout(async () => {
            await moviesStore.fetchMoviesByTitle(newTitle);
            searchResults.value = moviesStore.movies;
        }, 500);
    });
        
    if (actualPage === '/') {
        
    }

    const handleAddMovies = async () => {
        successFullAdd.value = false;
        failedAdd.value = false;

        for (const movie of selectedMovies.value) {
            try {
                const watched = router.currentRoute.value.name === 'home';
                const in_watchlist = router.currentRoute.value.name === 'watched';

                await moviesStore.addMovie(movie, watched, in_watchlist);
                successFullAdd.value = true;

            } catch (err) {
                failedAdd.value = true;
                console.error(err);
            }
        }

        showMovieModal.value = false;
        selectedMovies.value = [];
        isMovieSelected.value = false;
    };


    const handleMovieSelect = (movie: Movie) => {
        const alreadySelected = selectedMovies.value.find(m => m.id === movie.id);
        if (!alreadySelected) {
            selectedMovies.value.push(movie);
            isMovieSelected.value = true;
        }
        searchTitle.value = '';
        searchResults.value = [];
    }

    const removeMovie = (id: string) => {
        selectedMovies.value = selectedMovies.value.filter(movie => movie.id !== id);
        if (selectedMovies.value.length === 0) {
            isMovieSelected.value = false;
        }
    }
</script>

<template>
  <button class="modal-button" @click="showMovieModal = true">+</button>
  <div v-if="showMovieModal">
    <div class="modal-backdrop" @click="showMovieModal = false"></div>
    <div class="modal-content">
      <div class="modal-input">
        <h1>Adicionar Filme</h1>
        <div class="selected-movies">
            <div v-for="movie in selectedMovies" :key="movie.id" class="selected-movie">
                <img :src="`https://image.tmdb.org/t/p/w200${movie.poster_path}`" alt="Movie Poster" class="movie-poster" />
                <span>{{ movie.title }}</span>
                <button class="remove-movie-button" @click="removeMovie(movie.id)">x</button>
            </div>
        </div>
        <input type="text" placeholder="Título do Filme" v-model="searchTitle"/>
        <ul v-if="searchResults.length" class="dropdown-results">
          <li v-for="movie in searchResults" :key="movie.id" @click="handleMovieSelect(movie)" class="movie-item">
            <img :src="`https://image.tmdb.org/t/p/w200${movie.poster_path}`" alt="Movie Poster" class="movie-poster" />
            <span>{{ movie.title }}</span>
          </li>
        </ul>
      </div>
      <button class="handleAddMovie" :disabled="!isMovieSelected" @click="handleAddMovies">Adicionar</button>
    </div>
  </div>
  <Toast v-if="successFullAdd" message="Filme(s) adicionado(s) com sucesso!" @close="successFullAdd = false" type="success"/>
</template>

<style scoped>
    .modal-button {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        width: 6rem;
        height: 6rem;
        border-radius: 50%;
        background-color: #00ff007e;
        color: white;
        font-size: 2rem;
        border: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        cursor: pointer;
        transition: background-color 0.3s ease;
        text-align: center;
        font-size: 3rem;
    }

    .modal-button:hover {
        background-color: #00ff00;
        transition: transform 0.3s ease;
        transform: scale(1.05);
    }

    button:active {
        transform: scale(0.95);
    }

    .modal-backdrop {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 999;
    }

    .modal-content {
        position: fixed;
        top: 50%;
        left: 50%;
        height: 30rem;
        transform: translate(-50%, -50%);
        background-color: var(--color-background);
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        width: 25rem;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .handleAddMovie {
        padding: 0.5rem 1rem;
        font-size: 1rem;
        background-color: var(--color-primary);
        color: white;
        border: solid 1px #474745;
        border-radius: 5px;
        cursor: pointer;
    }

    .handleAddMovie:disabled {
        background-color: grey;
        cursor: not-allowed;
    }

    .handleAddMovie:not(:disabled):hover {
        background-color: #474745;
    }

    .modal-input input {
        width: 100%;
        padding: 0.5rem;
        font-size: 1rem;
        margin-top: 1rem;
        border: 1px solid var(--color-border);
        border-radius: 5px;
    }

    .dropdown-results {
        list-style: none;
        padding: 0;
        margin: 0.5rem 0 0 0;
        max-height: 10rem;
        overflow-y: auto;
        border: 1px solid var(--color-border);
        border-radius: 5px;
        background-color: var(--color-background);
    }

    .dropdown-results li {
        padding: 0.5rem;
        cursor: pointer;
    }

    .dropdown-results li:hover {
        background-color: var(--color-primary);
        color: white;
    }

    .movie-item {
        display: flex;
        align-items: center;
    }

    .movie-poster {
        width: 1rem;
        height: 1.5rem;
        object-fit: cover;
        margin-right: 1rem;
        border-radius: 3px;
    }

    .selected-movies {
        display: flex;
        flex-wrap: wrap;
        margin-bottom: 1rem;
        justify-content: center;
    }

    .selected-movie {
        display: flex;
        align-items: center;
        margin: 0.25rem;
        padding: 0.25rem 0.5rem;
        border: 1px solid var(--color-border);
        border-radius: 5px;
        background-color: var(--color-secondary);
    }

    .remove-movie-button {
        margin-left: 0.5rem;
        background-color: red;
        color: white;
        border: none;
        border-radius: 50%;
        width: 1.2rem;
        height: 1.2rem;
        cursor: pointer;
        font-size: 0.8rem;
        line-height: 1rem;
        text-align: center;
        padding: 0;
    }

    .remove-movie-button:hover {
        background-color: darkred;
    }
</style>