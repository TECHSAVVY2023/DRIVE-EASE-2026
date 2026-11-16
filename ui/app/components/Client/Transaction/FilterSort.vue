<template>
    <div class="px-5 flex flex-col sm:flex-row sm:items-center justify-between gap-3">

        <!-- Tabs -->
        <div class="flex flex-wrap gap-2">
            <button
                v-for="tab in tabs"
                :key="tab.value"
                @click="emit('update:activeTab', tab.value)"
                class="text-xs px-3 py-1.5 rounded-full border transition-colors duration-200 font-medium"
                :class="props.activeTab === tab.value
                    ? 'bg-[#C1121F] border-[#C1121F] text-white'
                    : 'border-[#2a2a2a] text-gray-400 hover:border-white hover:text-white'"
            >
                {{ tab.label }}
            </button>
        </div>

        <!-- Sort -->
        <div class="relative">
            <select
                :value="props.sortBy"
                @change="emit('update:sortBy', ($event.target as HTMLSelectElement).value)"
                class="smoked-control text-white text-xs px-4 py-2 pr-8 rounded-lg appearance-none cursor-pointer"
            >
                <option
                    v-for="option in sortOptions"
                    :key="option.value"
                    :value="option.value"
                >
                    {{ option.label }}
                </option>
            </select>

            <svg
                class="w-4 h-4 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none"
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
import type { Tab, SortOption } from '~/utils/types/booking'

const props = defineProps<{
    tabs: Tab[]
    activeTab: string
    sortBy: string
    sortOptions: SortOption[]
}>()

const emit = defineEmits<{
    (e: 'update:activeTab', value: string): void
    (e: 'update:sortBy', value: string): void
}>()

</script>
