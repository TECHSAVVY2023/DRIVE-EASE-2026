<template>
        <!-- Mission + Vision -->
        <section class="grid grid-cols-1 md:grid-cols-2 gap-4">

        <div class="smoked-charcoal-panel rounded-xl p-6 flex flex-col gap-3">

            <div class="flex items-center gap-3">

                <!-- Icon goes here -->
                <div class="w-8 h-8 bg-[#C1121F] rounded-md flex items-center justify-center flex-shrink-0">
                    <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="w-4 h-4 text-white"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                    </svg>
                </div>

                <h3 class="text-white font-bold text-base">{{ about.mission_heading }}</h3>
                
            </div>
            
            <p class="text-[#929292] text-sm leading-relaxed">
                {{ about.mission_description }}
            </p>

        </div>

        <div class="smoked-charcoal-panel rounded-xl p-6 flex flex-col gap-3">

            <div class="flex items-center gap-3">

                <!-- Icon goes here -->
                <div class="w-8 h-8 bg-[#C1121F] rounded-md flex items-center justify-center flex-shrink-0">
                    <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="w-4 h-4 text-white"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                    />
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                    />
                    </svg>
                </div>
                <h3 class="text-white font-bold text-base">{{  about.vission_heading  }}</h3>

            </div>

            <p class="text-[#929292] text-sm leading-relaxed">
                {{ about.vission_description }}
            </p>

        </div>

        </section>
</template>

<script setup lang="ts">
import type { AboutUsPageContent } from '~/utils/types/content'

const props = defineProps<{
    about: AboutUsPageContent
}>()
</script>