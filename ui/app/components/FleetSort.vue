<template>

    <div class="flex flex-col sm:flex-row gap-3 w-full">

        <!-- Sort -->
        <div class="relative w-full md:w-54">

            <select
                :value="sortBy"
                @change="emit('update:sortBy', ($event.target as HTMLSelectElement).value)"
                class="
                    smoked-control w-full rounded-lg
                    text-sm px-4 py-2.5 pr-10
                    appearance-none cursor-pointer
                "
            >
                <option value="">Sort: None</option>
                <option value="price-asc">Price: Low to High</option>
                <option value="price-desc">Price: High to Low</option>
                <option value="name">Name A–Z</option>
            </select>

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
                    d="M19 9l-7 7-7-7"
                />
            </svg>

        </div>

        <!-- Mobile Filter Toggle -->
        <div class="md:hidden w-full">

            <button
                @click="emit('toggleFilters')"
                class="
                    flex items-center justify-center gap-2
                    smoked-control w-full rounded-lg
                    text-white text-sm px-4 py-2.5
                "
            >
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
                        d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2a1 1 0 01-.293.707L13 13.414V19a1 1 0 01-.553.894l-4 2A1 0 017 21v-7.586L3.293 6.707A1 0 013 6V4z"
                    />
                </svg>

                {{ showFilters ? 'Hide Filters' : 'Show Filters' }}

            </button>

        </div>

    </div>

</template>

<script setup lang="ts">
defineProps<{
    sortBy: string
    showFilters: boolean
}>()

const emit = defineEmits<{
    (e: 'update:sortBy', value: string): void
    (e: 'toggleFilters'): void
}>()
</script>
