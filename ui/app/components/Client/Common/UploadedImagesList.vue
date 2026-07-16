<template>
    <div v-if="images.length" class="flex flex-col gap-2 mb-3">
        <div
            v-for="(file, index) in images"
            :key="index"
            class="flex items-center justify-between bg-[#121212] border border-[#333] rounded-lg px-3 py-2"
        >
            <div class="flex items-center gap-3">

                <div class="w-8 h-8 flex shrink-0 items-center justify-center bg-[#1a1a1a] rounded">
                    <svg
                        class="w-4 h-4 text-[#C1121F]"
                        fill="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path d="M19 3H5a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2V5a2 2 0 00-2-2zm0 16H5V5h14v14zm-4-7-2.5 3.01L11 13l-3 4h8z"/>
                    </svg>
                </div>

                <div>
                    <p class="text-white text-xs font-medium">
                        {{ file.name }}
                    </p>

                    <p class="text-gray-500 text-[10px]">
                        {{ (file.size / 1024).toFixed(1) }} KB
                    </p>
                </div>

            </div>

            <button
                @click="$emit('remove', index)"
                class="text-gray-500 hover:text-red-500 transition"
            >
                ✕
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
defineProps<{
    images: File[]
}>()

defineEmits<{
    (e: 'remove', index: number): void
}>()
</script>