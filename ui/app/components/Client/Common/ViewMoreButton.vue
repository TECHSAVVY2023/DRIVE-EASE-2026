<template>
    <div class="flex flex-col items-center gap-2 mt-6">
        <button
            v-if="nextPage"
            @click="$emit('load-more')"
            class="flex items-center gap-2 bg-[#C1121F] hover:bg-[#9B0E18] text-white text-sm font-semibold px-8 py-3 rounded-lg transition-colors duration-200"
        >
            View more
            <svg
                class="w-4 h-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
            >
                <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 5l7 7-7 7"
                />
            </svg>
        </button>

        <span class="text-[#929292] text-xs">
            {{ displayedReviews }} out of {{ totalReviews }} reviews
        </span>
    </div>
</template>

<script setup lang="ts">
defineProps<{
    nextPage: string
    displayedReviews: number
    totalReviews: number
}>()

defineEmits<{
    (e: 'load-more'): void
}>()
</script>