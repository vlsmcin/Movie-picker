<script lang="ts" setup>
    import { ref } from 'vue';
    import { useUserAuthStore } from '@/stores/user';
    import router from '@/router';
    import Toast from '@/components/Toast.vue';

    const userAuthStore = useUserAuthStore();
    const username = ref('');
    const password = ref('');
    const emptyUsername = ref(false);
    const emptyPassword = ref(false);
    const showToast = ref(false);
    const toastMessage = ref('');
    const type = ref<'success' | 'error'>('error');

    const login = async () => {
        try {
            await userAuthStore.login(username.value, password.value);
            showToast.value = true;
            toastMessage.value = 'Login bem-sucedido!';
            type.value = 'success';
        } catch (error) {
            console.error(error);
            showToast.value = true;
            type.value = 'error';
            toastMessage.value = 'Login falhou. Por favor, verifique suas credenciais e tente novamente.';
        }
    };

    const handleLogin = () => {
        if (!username.value) {
            emptyUsername.value = true;
        } else {
            emptyUsername.value = false;
        }

        if (!password.value) {
            emptyPassword.value = true;
        } else {
            emptyPassword.value = false;
        }

        if (emptyUsername.value || emptyPassword.value) {
            showToast.value = true;
            type.value = 'error';
            toastMessage.value = 'Por favor, preencha todos os campos obrigatórios.';
            return;
        }
        
        login();
    }

    const handleToastClose = () => {
        showToast.value = false;

        if (type.value === 'success') {
            router.push('/');
        }
    };
</script>

<template>
    <Toast v-if="showToast" :message="toastMessage" @close="handleToastClose" :type="type"/>
    <div class="login-view">
        <h1 class="title">Login</h1>
        <input :class="{'empty-username': emptyUsername}" type="text" placeholder="Usuário" v-model="username" />
        <input :class="{'empty-password': emptyPassword}" type="password" placeholder="Senha" v-model="password" />
        <button class="login-options" @click="handleLogin">Entrar</button>
        <button class="login-options" @click="() => router.push('/register')">Cadastrar-se</button>
    </div>
</template>

<style scoped>
    .login-view {
        display: flex;
        flex-direction: column;
        max-width: 400px;
        margin: 2rem auto;
        padding: 2rem;
        border: 1px solid var(--color-border);
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        position: relative;     
    }

    input {
        display: block;
        margin: 0.4rem 0;
        padding: 0.5rem;
        font-size: 1rem;
    }

    .login-options {
        padding: 0.5rem 1rem;
        margin: 0.25rem 0;
        font-size: 1rem;
        background-color: var(--color-primary);
        color: white;
        border: solid 1px #474745;
        border-radius: 5px;
        cursor: pointer;
    }

    .login-options:hover {
        background-color: #474745;
    }

    .empty-username, .empty-password {
        border: 1px solid red;
        border-radius: 5px;
    }

    .title {
        text-align: center;
        margin-bottom: 1rem;
    }

</style>