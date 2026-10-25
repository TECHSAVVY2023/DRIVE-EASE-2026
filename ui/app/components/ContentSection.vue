<template>
    <section>
        <div class="mb-4">
            <h3 class="text-[13px] font-semibold text-white">{{ title }}</h3>
            <p class="mt-1 text-[10px] text-[#666]">{{ description }}</p>
        </div>

        <div class="rounded-xl border border-[#252525] bg-[#121212] p-4 sm:p-5">
            <slot />
        </div>
    </section>
</template>

<script setup lang="ts">
defineProps<{
    title: string
    description: string
}>()
</script>
