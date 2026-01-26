<script lang="ts" setup>
    import { ref } from 'vue';
    import { useUserAuthStore } from '@/stores/user';

    const userAuthStore = useUserAuthStore();
    const username = ref('');
    const email = ref('');
    const password = ref('');

    const login = async () => {
        try {
            await userAuthStore.login(username.value, email.value, password.value);
            // Redirect or show success message
        } catch (error) {
            // Handle login error
            console.error(error);
        }
    };
</script>

<template>
    <input type="text" placeholder="Username" v-model="username" />
    <input type="email" placeholder="Email" v-model="email" />
    <input type="password" placeholder="Password" v-model="password" />
    <button @click="login">Login</button>
</template>