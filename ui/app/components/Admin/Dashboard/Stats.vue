<template>
    <div class="grid grid-cols-2 xl:grid-cols-4 gap-4 mb-6">

        <div
            v-for="stat in statCards"
            :key="stat.label"
            class="bg-[#1a1a1a] rounded-xl p-5
                    border border-[#222]"
        >

            <div class="flex items-start justify-between">

                <div
                    class="w-9 h-9 rounded-lg
                            bg-[#C1121F]
                            flex items-center justify-center"
                >
                    <svg
                        class="w-5 h-5 text-white"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                    >
                        <path
                            :d="stat.icon"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                        />
                    </svg>
                </div>

                <span
                    :class="[
                        'text-[11px] font-semibold px-2 py-1 rounded-md',
                        stat.positive
                            ? 'text-green-400 bg-green-400/10'
                            : 'text-red-400 bg-red-400/10'
                    ]"
                >
                    {{ stat.change }}
                </span>

            </div>

            <p class="text-gray-400 text-xs mt-4">
                {{ stat.label }}
            </p>

            <p class="text-white text-2xl sm:text-3xl
                        font-extrabold mt-1">
                {{ stat.value }}
            </p>

        </div>

    </div>
</template>

<script setup lang="ts">
import type { StatCard } from '~/utils/types/dashboard'

const props = defineProps({
    statCards: Array as () => StatCard[]
})
</script>
