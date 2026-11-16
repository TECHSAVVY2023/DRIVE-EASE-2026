<template>
    <!-- Opening Hours -->
    <div class="smoked-charcoal-panel rounded-xl p-6 flex flex-col gap-4">

        <h3 class="text-white font-bold text-sm">Opening hours</h3>

        <div class="flex flex-col gap-2">

            <div v-for="(schedule, i) in contact.opening_hours" :key="i" class="flex items-center justify-between">
                
                <span class="text-[#9E9E9E] text-xs">{{ schedule.day }}</span>
                <span class="text-white text-xs font-medium" :class="schedule.is_closed ? 'text-[#C1121F]' : ''">
                    {{ schedule.time }}
                </span>

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
