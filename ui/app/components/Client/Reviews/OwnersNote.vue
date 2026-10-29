<template>
    <div
        id="owner-note"
        class="scroll-mt-62 bg-[#2A1616] border-l-4 border-[#C1121F] rounded-xl overflow-hidden w-full"
    >
        <div class="flex items-center gap-2 px-5 py-5 border-b border-[#C1121F]/20">

            <svg class="w-4 h-4 text-[#FF6161]" fill="currentColor" viewBox="0 0 24 24">
                <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/>
            </svg>

            <span class="text-[#FF6161] text-xs font-semibold">
                Owner's note
            </span>

        </div>

        <div class="px-6 py-5">
            <svg class="w-5 h-5 text-[#FF6161] mb-3" fill="currentColor" viewBox="0 0 24 24">
                <path d="M6 17h3l2-4V7H5v6h3zm8 0h3l2-4V7h-6v6h3z" />
            </svg>

            <p class="text-[#FF6161] text-sm">
                {{ note }}
            </p>

            <svg
                class="w-5 h-5 text-[#FF6161] mt-3 ml-auto block"
                fill="currentColor"
                viewBox="0 0 24 24"
                style="transform: rotate(180deg)"
            >
                <path d="M6 17h3l2-4V7H5v6h3zm8 0h3l2-4V7h-6v6h3z" />
            </svg>
        </div>
    </div>
</template>

<script setup lang="ts">
defineProps<{
  note: string | null
}>()

</script>