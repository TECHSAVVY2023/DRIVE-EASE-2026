<template>
    <div class="flex flex-col items-center justify-center py-20 gap-3">

        <svg
        class="w-10 h-10 text-[#7E7E7E]"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        >
        <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
        />
        </svg>

        <p class="text-[#7E7E7E] text-sm text-center">
        {{ message }}
        </p>

        <button
        v-if="buttonText"
        @click="$emit('action')"
        class="text-[#C1121F] text-xs hover:underline"
        >
        {{ buttonText }}
        </button>

    </div>
</template>

<script setup lang="ts">
defineProps<{
    message: string
    buttonText?: string
}>()

defineEmits<{
    (e: 'action'): void
}>()
</script>