<script lang="ts" setup>
    import { ref, onMounted } from 'vue';

    defineProps<{ message: string; type: 'success' | 'error' }>();
    const emit = defineEmits(['close']);

    const visible = ref(true);

    onMounted(() => {
        setTimeout(() => {
            visible.value = false;
        }, 1200);
    });
</script>

<template>
    <Transition name="slide-fade" appear @after-leave="emit('close')">
        <div v-if="visible" :class="['toast', type]">
            {{ message }}
        </div>
    </Transition>
</template>

<style scoped>
    .toast {
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        color: white;
        font-weight: bold;
        text-align: center;
        position: fixed;
        top: 1rem;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1000;
    }

    .slide-fade-enter-active,
    .slide-fade-leave-active {
        transition: all 0.4s ease;
    }

    .slide-fade-enter-from,
    .slide-fade-leave-to {
        opacity: 0;
        transform: translateX(-50%) translateY(-20%);
    }

    .slide-fade-enter-to,
    .slide-fade-leave-from {
        opacity: 1;
        transform: translateX(-50%) translateY(0);
    }

    .success {
        background-color: #4caf50;
    }

    .error {
        background-color: #f44336;
    }
</style>