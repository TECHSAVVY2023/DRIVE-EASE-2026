<template>
    <button v-if="isLoggedIn"
        class="bg-[#C1121F] hover:bg-[#9B0E18] transition-colors duration-200 text-white text-xs px-4 py-2 rounded-lg flex items-center gap-2"
        @click="$emit('click')"
    >

        <svg
            xmlns="http://www.w3.org/2000/svg"
            class="w-5 h-5"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            stroke-width="2"
        >
            <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5M16.5 3.5a2.121 2.121 0 113 3L12 14l-4 1 1-4 7.5-7.5z"
            />
        </svg>
        Write a Review

    </button>
</template>

<script setup lang="ts">
defineProps<{
    isLoggedIn: boolean
}>()

defineEmits<{
    click: []
}>()
</script>