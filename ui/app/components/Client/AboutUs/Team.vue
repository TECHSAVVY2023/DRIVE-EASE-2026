<template>
    <!-- Our Team -->
    <section class="smoked-charcoal-panel flex flex-col gap-5 rounded-xl px-6 pt-6 pb-10">
    
    <h2 class="text-white font-extrabold text-xl">Our team</h2>

    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">

        <div
            v-for="member in about.team"
            :key="member.id"
            class="group flex h-full flex-col items-center gap-4 rounded-xl border border-white/10 bg-white/[0.025] p-5 text-center transition duration-200 hover:-translate-y-0.5 hover:border-[#C1121F]/70 hover:bg-white/[0.04]"
        >

        <UserAvatar
                :src="member.user_profile_picture"
                :alt="member.user_name"
                class="h-20 w-20 ring-3 ring-white/10 ring-offset-2 ring-offset-[#171717] transition group-hover:ring-[#C1121F]/50"
        />

            <div>
                <p class="text-sm font-semibold text-white">{{ member.user_name }}</p>
                <p class="mt-1.5 inline-flex rounded-full bg-[#C1121F] px-2.5 py-1 text-[10px] font-semibold uppercase tracking-wide text-white">
                    {{ member.position }}
                </p>
            </div>

            <p class="text-xs leading-5 text-[#a3a3a3]">{{ member.description }}</p>

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
