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
                    : 'bg-[#1a1a1a] border-[#222] text-[#929292] hover:border-[#C1121F]'
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
                    : 'bg-[#1a1a1a] border-[#222] text-[#929292] hover:border-[#C1121F]'
                "
            >
                {{ star }}
                <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
            </button>
        </div>

        <!-- Sort -->
        <select
            :value="sortBy"
            @change="emit(
                'update:sortBy',
                ($event.target as HTMLSelectElement).value as SortBy
            )"
            class="bg-[#1a1a1a] border border-[#222] text-white text-sm rounded-lg px-4 py-2 outline-none hover:border-[#C1121F] transition-colors duration-200"
            >
            <option value="newest">Newest</option>
            <option value="oldest">Oldest</option>
            <option value="highest">Highest Likes</option>
            <option value="lowest">Lowest Likes</option>
        </select>

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