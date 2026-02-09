<script lang="ts" setup>
    import { ref, computed } from 'vue';
    import { useRoute } from 'vue-router';

    const dropdownUserVisible = ref(false);
    const route = useRoute();
    const currentRoute = computed(() => route.name);

    function toggleDropdownUser() {
        dropdownUserVisible.value = !dropdownUserVisible.value;
    }
</script>

<template>
    <header class="home-header">
        <RouterLink to="/pickmovie" :class="{ 'option-selected': currentRoute === 'pickmovie' }">Escolher filme</RouterLink>
        <RouterLink to="/watchlist" :class="{ 'option-selected': currentRoute === 'watchlist' }">Minha lista</RouterLink>
        <RouterLink to="/watched" :class="{ 'option-selected': currentRoute === 'watched' }">Filmes assistidos</RouterLink>
        <img src="@/assets/empty_user.svg" alt="Avatar" class="profile-avatar" @click="toggleDropdownUser"/>

        <div v-if="dropdownUserVisible" class="dropdownUserMenu">
            <p>Entrar</p>
            <p>Criar conta</p>
        </div>
    </header>
</template>

<style scoped>
    .home-header {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        max-height: 100px;
        padding: 1rem 2rem;
        border-bottom: 2px solid rgba(0, 128, 0, 0.2);
        border-radius: 10%;
    }

    a {
        font-size: 1.5rem;
        font-weight: bold;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    a:hover {
        color: var(--color-primary);
    }

    .profile-avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background-color: var(--color-border);
    }

    .profile-avatar:hover {
        cursor: pointer;
    }

    .dropdownUserMenu {
        position: absolute;
        top: 7rem;
        right: 4rem;
        background-color: var(--color-background);
        border: 1px solid var(--color-border);
        border-radius: 5px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        padding: 1rem;
        display: flex;
        flex-direction: column;
    }

    .option-selected {
        color: var(--color-primary);
    }
</style>