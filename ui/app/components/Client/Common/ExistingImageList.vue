
<template>
    <div v-if="images.length" class="flex flex-col gap-2 mb-3">
        <div
            v-for="(url, index) in images"
            :key="url"
            class="group flex items-center gap-3 rounded-xl border border-white/10 bg-[#0f0f0f] p-2.5 transition-all duration-200 hover:border-[#c1121f]/60 hover:bg-[#151515]"
        >
            <!-- Image Preview -->
            <a
                :href="url"
                target="_blank"
                rel="noopener noreferrer"
                class="relative h-16 w-20 shrink-0 overflow-hidden rounded-lg border border-white/10 bg-[#1a1a1a]"
            >
                <img
                    :src="url"
                    :alt="`Review image ${index + 1}`"
                    class="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
                    loading="lazy"
                />

                <div
                    class="absolute inset-0 flex items-center justify-center bg-black/0 transition-colors group-hover:bg-black/20"
                >
                    <svg
                        class="h-5 w-5 text-white opacity-0 drop-shadow transition-opacity group-hover:opacity-100"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M15 3h6v6m-11 5L21 3M19 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2h6"
                        />
                    </svg>
                </div>
            </a>

            <!-- Image Details -->
            <div class="min-w-0 flex-1">
                <p class="text-sm font-medium text-white truncate" :title="getImageName(url)">
                    {{ getImageName(url) }}
                </p>

                <a
                    :href="url"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="mt-1 inline-block text-xs text-white/40 transition-colors hover:text-[#c1121f]"
                >
                    View full image
                </a>
            </div>

            <!-- Remove Button -->
            <button
                type="button"
                @click="$emit('remove', index, url)"
                :aria-label="`Remove image ${index + 1}`"
                class="flex h-9 w-9 shrink-0 items-center justify-center rounded-full text-white/40 transition-all hover:text-[#c1121f] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#c1121f]"
            >
                <svg
                    class="h-4 w-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M6 6l12 12M18 6L6 18"
                    />
                </svg>
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

const getImageName = (url: string): string => {
    return decodeURIComponent(url.split('/').pop()?.split('?')[0] || 'Unknown image')
}
</script>
