<template>
    <section class="grid grid-cols-1 md:grid-cols-2 gap-4 items-center">

        <!-- Who We Are -->
        <div class="smoked-charcoal-panel flex flex-col h-full justify-center gap-4 p-6 rounded-xl">
            <h2 class="text-white font-extrabold text-xl">
                {{ about.wwr_heading }}
            </h2>

            <p class="text-[#929292] text-sm leading-relaxed">
                {{ about.wwr_description }}
            </p>

            <!-- Stats -->
            <div class="flex gap-6 mt-2">
                <div
                    v-for="(stat, index) in about.wwr_stats"
                    :key="index"
                    class="flex flex-col"
                >
                    <span class="text-white font-extrabold text-2xl">
                        {{ stat.value }}
                    </span>

                    <span class="text-[#929292] text-xs mt-0.5">
                        {{ stat.stat }}
                    </span>
                </div>
            </div>
        </div>

        <!-- Image -->
        <div class="bg-[#1a1a1a] border border-[#2a2a2a] rounded-xl overflow-hidden h-full flex items-center justify-center">
            <img
                :src="about.wwr_image || 'Image1'"
                :alt="about?.wwr_image || ''"
                class="w-full h-full object-cover"
                @error="handleImageError"
            />
        </div>

    </section>
</template>

<script setup lang="ts">
import type { AboutUsPageContent } from '~/utils/types/content'

const props = defineProps<{
    about: AboutUsPageContent
}>()

function handleImageError(event: Event): void {
    const target = event.target as HTMLImageElement
    target.style.display = 'none'
}
</script>