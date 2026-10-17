<template>
    <div
        v-for="card in cards"
        :key="card.label"
        class="bg-[#161616] border border-[#232323] rounded-xl p-5"
    >
        <div
            class="w-[38px] h-[38px] bg-[#c81e2c] rounded-lg flex items-center justify-center mb-[26px] [&>svg]:w-[18px] [&>svg]:h-[18px] [&>svg]:stroke-white [&>svg]:fill-none [&>svg]:stroke-[1.8]"
            v-html="card.icon"
        ></div>

        <div class="text-[#9b9b9b] text-[13px] mb-1.5">
            {{ card.label }}
        </div>

        <div class="text-[26px] font-extrabold">
            {{ card.value }}
        </div>
    </div>
</template>

<script setup lang="ts">

interface StatCard { 
    label: string 
    value: number | string 
    icon: string
} 

const props = defineProps<{
    cards: StatCard[]
}>()

</script>