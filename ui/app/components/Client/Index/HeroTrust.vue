<template>
    <!-- =========================
        Trust section
    ========================== -->
    <h2 class="text-white text-2xl font-extrabold text-center uppercase mb-10 md:text-3xl">
        Why Choose Us?
    </h2>

    <!-- =========================
            Trusts cards
    ========================== -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-px overflow-hidden rounded-xl border border-white/[0.07] bg-white/[0.07]">

        <div
            v-for="(stat, index) in props.content.trust_items"
            :key="stat.id || `new-${index}`"
            class="
                flex flex-col items-center 
                justify-center text-center gap-1 
                bg-[#19191b] px-6 py-8
                transition-colors duration-200 hover:bg-[#1d1d20]
            "
        >
            <span class="text-white text-2xl font-extrabold md:text-3xl">{{ stat.value }}</span>
            <span class="text-[#a0a0a5] text-sm">{{ stat.label }}</span>
        </div>

    </div>
</template>

<script setup lang="ts">
import type { HomepageContent } from '~/utils/types/content'

/* =========================
   Trust data
========================= */
const props = defineProps<{
    content: HomepageContent
}>()
</script>
