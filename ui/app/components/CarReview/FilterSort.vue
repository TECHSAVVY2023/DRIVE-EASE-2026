<template>
    <!-- Filter + Sort Section -->
    <div class="flex flex-col lg:flex-row gap-4 justify-between mb-5">

        <!-- Rating Filters -->
        <div class="flex flex-wrap gap-2">
            <button
                @click="emit('update:selectedRating', 0)"
                class="px-4 py-2 rounded-lg border text-sm font-medium transition-colors duration-200"
                :class="
                    selectedRating === 0
                    ? 'bg-[#C1121F] border-[#C1121F] text-white'
                    : 'bg-white/[0.025] border-white/[0.08] text-[#a0a0a5] hover:bg-white/[0.06] hover:border-[#C1121F]'
                "
            >
                All
            </button>

            <button
                v-for="star in [5,4,3,2,1]"
                :key="star"
                @click="emit('update:selectedRating', star)"
                class="flex items-center gap-1 px-4 py-2 rounded-lg border text-sm font-medium transition-colors duration-200"
                :class="
                    selectedRating === star
                    ? 'bg-[#C1121F] border-[#C1121F] text-white'
                    : 'bg-white/[0.025] border-white/[0.08] text-[#a0a0a5] hover:bg-white/[0.06] hover:border-[#C1121F]'
                "
            >
                {{ star }}
                <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
            </button>
        </div>

        <!-- Sort -->
        <div class="relative flex-1 sm:flex-none">
            <select
                :value="sortBy"
                @change="emit(
                    'update:sortBy',
                    ($event.target as HTMLSelectElement).value as SortBy
                )"
                class="smoked-control w-full rounded-lg
                    text-sm px-4 py-2.5 pr-10
                    appearance-none cursor-pointer"
                >
                <option value="newest">Newest</option>
                <option value="oldest">Oldest</option>
                <option value="highest">Highest Likes</option>
                <option value="lowest">Lowest Likes</option>
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

    </div>
</template>

<script setup lang="ts">
type SortBy = "newest" | "oldest" | "highest" | "lowest"

defineProps<{
    selectedRating: number;
    sortBy: SortBy;
}>();

const emit = defineEmits<{
    (e: "update:selectedRating", value: number): void
    (e: "update:sortBy", value: SortBy): void
}>()
</script>
