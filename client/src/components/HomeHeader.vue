<template>
    <header class="home-header">
        <a>Escolher filme</a>
        <a>Minha lista</a>
        <a>Filmes assistidos</a>
        <img alt="Avatar" class="profile-avatar"/>
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
        max-width: 1200px;
        border-bottom: 2px solid var(--color-text);
        border-radius: 10%;
    }

    a {
        font-size: 1.2rem;
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
</style>