<template>
    <router-link
        :to="item.link"
        class="flex items-center justify-between gap-3 px-4 py-3 md:py-2.5 transition-colors duration-200"
        :class="active
            ? 'bg-[#252525] text-white font-semibold border-l-4 border-[#c1121f]'
            : 'text-[#7E7E7E] hover:text-white hover:bg-[#232323]'"
    >
        <div class="flex items-center gap-3 min-w-0">
            <div v-html="icon"></div>

            <span class="truncate">
                {{ item.label }}
            </span>
        </div>

        <span
            v-if="item.badge"
            class="bg-[#C1121F] text-white text-[9px] font-bold px-1.5 py-0.5 rounded-full"
        >
            {{ item.badge }}
        </span>
    </router-link>
</template>

<script setup lang="ts">
defineProps<{
    item: {
        key: string
        label: string
        link: string
        badge?: string | number
    }
    active: boolean
    icon: string
}>()
</script>