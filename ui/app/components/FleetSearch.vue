<template>

    <div class="relative w-full md:max-w-sm">

        <input
            :value="search"
            @input="emit('update:search', ($event.target as HTMLInputElement).value)"
            type="text"
            :placeholder="placeholder || 'Search'"
            class="
                w-full bg-[#262626] border border-[#2a2a2a]
                px-4 py-2.5 pr-10 rounded-lg
                text-white text-sm
                focus:outline-none focus:border-[#C1121F]
                placeholder-[#929292]
                transition-colors duration-200
            "
        />

        <svg
            class="w-4 h-4 text-[#929292] absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
        >
            <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
        </svg>

    </div>

</template>

<script setup lang="ts">
defineProps<{
    search: string
    placeholder?: string
}>()

const emit = defineEmits<{
    (e: 'update:search', value: string): void
}>()
</script>