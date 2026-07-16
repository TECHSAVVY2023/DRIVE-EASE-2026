<template>
    <div v-if="images.length" class="flex flex-col gap-2 mb-2">
        <div
            v-for="(url, index) in images"
            :key="'existing-' + index"
            class="flex items-center justify-between bg-[#0f0f0f] border border-white/10 hover:border-[#c1121f] rounded-lg px-3 py-2 transition-colors"
        >
            <div class="flex items-center gap-3">

                <div class="w-8 h-8 flex items-center justify-center bg-[#1a1a1a] rounded">
                    <svg class="w-4 h-4 text-[#c1121f]" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    </svg>
                </div>

                <a
                    :href="url"
                    target="_blank"
                    class="text-white text-xs hover:text-[#c1121f] transition-colors"
                >
                    View Image {{ index + 1 }}
                </a>

            </div>

            <button
                @click="$emit('remove', index, url)"
                class="text-white/40 hover:text-red-500"
            >
                ✕
            </button>

        </div>
    </div>
</template>

<script setup lang="ts">
defineProps<{
    images: string[]
}>()

defineEmits<{
    (e: 'remove', index: number, url: string): void
}>()
</script>