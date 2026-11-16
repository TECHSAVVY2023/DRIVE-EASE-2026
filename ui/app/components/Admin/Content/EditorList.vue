<template>
    <div class="border-t border-[#262626] pt-5">
        <div class="mb-3 flex items-center justify-between gap-3">
            <h3 class="text-xs font-semibold text-white">{{ title }}</h3>
            <button type="button" :class="secondaryButtonClass" @click="$emit('add')">{{ addLabel }}</button>
        </div>
        <div class="space-y-3"><slot /></div>
    </div>
</template>

<script setup lang="ts">
defineProps<{ title: string; addLabel: string }>()
defineEmits<{ add: [] }>()
const secondaryButtonClass = 'shrink-0 rounded-lg border border-[#343434] bg-[#1b1b1b] px-3 py-2 text-[10px] font-semibold text-[#bbb] transition hover:border-[#C1121F] hover:text-white'
</script>
