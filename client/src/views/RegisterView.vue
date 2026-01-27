<script lang="ts" setup>
    import { ref } from 'vue';
    import { useUserAuthStore } from '@/stores/user';
    import router from '@/router';
    import Toast from '@/components/Toast.vue';

    const userAuthStore = useUserAuthStore();
    const username = ref('');
    const email = ref('');
    const password = ref('');
    const passwordConfirm = ref('');
    const emptyUsername = ref(false);
    const emptyEmail = ref(false);
    const emptyPassword = ref(false);
    const emptyPasswordConfirm = ref(false);
    const showToast = ref(false);
    const toastMessage = ref('');
    const type = ref<'success' | 'error'>('error');

    const register = async () => {
        try {
            await userAuthStore.register(username.value, email.value, password.value);
            showToast.value = true;
            type.value = 'success';
            toastMessage.value = 'Registro bem-sucedido!';
            router.push('/login');
        } catch (error) {
            console.error(error);
            showToast.value = true;
            type.value = 'error';
            toastMessage.value = 'Falha no registro. Por favor, tente novamente.';
        }
    };

    const handleRegister = () => {
        if (!username.value) {
            emptyUsername.value = true;
        } else {
            emptyUsername.value = false;
        }

        if (!email.value) {
            emptyEmail.value = true;
        } else {
            emptyEmail.value = false;
        }

        if (!password.value) {
            emptyPassword.value = true;
        } else {
            emptyPassword.value = false;
        }

        if (!passwordConfirm.value) {
            emptyPasswordConfirm.value = true;
        } else {
            emptyPasswordConfirm.value = false;
        }

        if (emptyUsername.value || emptyEmail.value || emptyPassword.value || emptyPasswordConfirm.value) {
            showToast.value = true;
            type.value = 'error';
            toastMessage.value = 'Por favor, preencha todos os campos obrigatórios.';
            return;
        }

        if (password.value !== passwordConfirm.value) {
            showToast.value = true;
            type.value = 'error';
            toastMessage.value = 'As senhas não coincidem. Por favor, tente novamente.';
            return;
        }

        register();
    }
</script>

<template>
    <Toast v-if="showToast" :message="toastMessage" @close="showToast = false" :type="type"/>
    <div class="register-view">
        <h1 class="title">Registrar-se</h1>
        <input type="text" placeholder="Usuário" v-model="username" />
        <input type="email" placeholder="Email" v-model="email" />
        <input type="password" placeholder="Senha" v-model="password" />
        <input type="password" placeholder="Confirmar Senha" v-model="passwordConfirm" />
        <button class="register-options" @click="handleRegister">Cadastrar-se</button>
        <button class="register-options" @click="() => router.push('/login')">Já tenho uma conta</button>
    </div>
</template>

<style scoped>
    .register-view {
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

    .register-options {
        padding: 0.5rem 1rem;
        margin: 0.25rem 0;
        font-size: 1rem;
        background-color: var(--color-primary);
        color: white;
        border: solid 1px #474745;
        border-radius: 5px;
        cursor: pointer;
    }

    .register-options:hover {
        background-color: #474745;
    }

    .title {
        text-align: center;
        margin-bottom: 1rem;
    }
</style>