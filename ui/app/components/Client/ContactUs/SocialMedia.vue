<template>
    <!-- Follow Us -->
    <div class="smoked-charcoal-panel rounded-xl p-6 flex flex-col gap-4">

        <h3 class="text-white font-bold text-sm">Follow us</h3>

        <div class="flex gap-3">

            <!-- Facebook -->
            <a :href="contact.facebook_url" class="w-9 h-9 rounded-lg bg-[#232323] hover:bg-[#C1121F] flex items-center justify-center transition-colors duration-200">
            <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z"/>
            </svg>
            </a>

            <!-- Instagram -->
            <a :href="contact.instagram_url" class="w-9 h-9 rounded-lg bg-[#232323] hover:bg-[#C1121F] flex items-center justify-center transition-colors duration-200">
            <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24">
                <rect x="2" y="2" width="20" height="20" rx="5" ry="5" fill="none" stroke="currentColor" stroke-width="2"/>
                <circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/>
                <circle cx="17.5" cy="6.5" r="1" fill="currentColor"/>
            </svg>
            </a>

            <!-- X / Twitter -->
            <a :href="contact.x_url" class="w-9 h-9 rounded-lg bg-[#232323] hover:bg-[#C1121F] flex items-center justify-center transition-colors duration-200">
            <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
            </svg>
            </a>

            <!-- TikTok -->
            <a :href="contact.tiktok_url" class="w-9 h-9 rounded-lg bg-[#232323] hover:bg-[#C1121F] flex items-center justify-center transition-colors duration-200">
            <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1V9.01a6.33 6.33 0 00-.79-.05 6.34 6.34 0 00-6.34 6.34 6.34 6.34 0 006.34 6.34 6.34 6.34 0 006.33-6.34V8.69a8.18 8.18 0 004.78 1.52V6.76a4.85 4.85 0 01-1.01-.07z"/>
            </svg>
            </a>

        </div>
    </div>
</template>

<script setup lang="ts">
import type { ContactPageContent } from '~/utils/types/content'

const props = defineProps<{
    contact: ContactPageContent
}>()
</script>