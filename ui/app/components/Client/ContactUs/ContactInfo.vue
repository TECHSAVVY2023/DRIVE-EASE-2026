<template>
    <!-- Contact Information -->
    <div class="smoked-charcoal-panel rounded-xl p-6 flex flex-col gap-4">
        
        <h3 class="text-white font-bold text-sm">Contact information</h3>

        <div class="flex flex-col gap-3">

            <div class="flex items-start gap-3">
                <div class="w-8 h-8 bg-[#C1121F] rounded-md flex items-center justify-center flex-shrink-0">
                    <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                    </svg>
                </div>
                <div>
                    <p class="text-[#9E9E9E] text-xs">Phone</p>
                    <p class="text-white text-sm font-medium">{{ props.contact.phone  }}</p>
                </div>
            </div>

            <div class="flex items-start gap-3">
                <div class="w-8 h-8 bg-[#C1121F] rounded-md flex items-center justify-center flex-shrink-0">
                    <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                    </svg>
                </div>
                <div>
                    <p class="text-[#9E9E9E] text-xs">Email</p>
                    <p class="text-white text-sm font-medium">{{ props.contact.email }}</p>
                </div>
            </div>
            
            <div class="flex items-start gap-3">
                <div class="w-8 h-8 bg-[#C1121F] rounded-md flex items-center justify-center flex-shrink-0">
                    <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                    </svg>
                </div>
                <div>
                    <p class="text-[#9E9E9E] text-xs">Address</p>
                    <p class="text-white text-sm font-medium">
                        {{ props.contact.address }}
                    </p>
                </div>
            </div>

        </div>

    </div>
</template>

<script setup lang="ts">
import type { ContactPageContent } from '~/utils/types/content'

const props = defineProps<{
    contact: ContactPageContent
}>()
</script>