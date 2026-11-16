<template>
    <!-- Our Journey -->
    <section class="smoked-charcoal-panel flex flex-col gap-5 rounded-xl px-6 pt-6 pb-10">

        <h2 class="text-white font-extrabold text-xl">Our journey</h2>

        <div class="flex flex-col gap-3">
            <div
                v-for="(milestone, i) in about.journey"
                :key="milestone.year + i"
                class="flex items-center gap-4 bg-[#111113]/95 border border-white/[0.07] rounded-xl px-6 py-5"
            >
                <!-- Year -->
                <span class="text-white font-extrabold text-xl w-14 flex-shrink-0">{{ milestone.year }}</span>

                <!-- Dot -->
                <div class="w-3 h-3 rounded-full bg-[#C1121F] flex-shrink-0 ring-4 ring-[#C1121F]/20"></div>

                <!-- Content -->
                <div class="flex flex-col gap-1 flex-1 min-w-0">
                    <p class="text-white font-bold text-sm">{{ milestone.title }}</p>
                    <p class="text-[#929292] text-xs leading-relaxed">{{ milestone.description }}</p>
                </div>
            </div>
        </div>

    </section>
</template>

<script setup lang="ts">
import type { AboutUsPageContent } from '~/utils/types/content'

const props = defineProps<{
    about: AboutUsPageContent
}>()
</script>
