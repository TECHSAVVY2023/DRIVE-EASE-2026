<template>
    <a
        :href="props.url"
        target="_blank"
        rel="noopener noreferrer"
        class="group flex items-center gap-3 bg-[#0f0f0f] border border-white/10 hover:border-[#C1121F] rounded-lg px-3 py-2 transition-colors cursor-pointer"
    >
        <!-- Icon -->
        <div
            class="flex-shrink-0 flex items-center justify-center w-13 h-10 rounded bg-[#1a1a1a] text-white/30 group-hover:text-[#C1121F] transition-colors"
        >
            <svg
                class="w-5 h-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="1.5"
                stroke-linecap="round"
                stroke-linejoin="round"
            >
                <path d="M4 4a2 2 0 0 1 2-2h8l6 6v12a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V4z"/>
                <path d="M14 2v6h6"/>
                <path d="M8 13h8"/>
                <path d="M8 17h5"/>
            </svg>
        </div>

        <!-- Info -->
        <div class="flex-1 min-w-0">
            <p class="text-white text-xs font-medium group-hover:text-[#C1121F] transition-colors">
                ID {{ props.index + 1 }}
            </p>

            <p class="text-white/40 text-xs mt-0.5">
                {{ getExtension(props.url) }} · Tap to open
            </p>
        </div>

        <!-- Arrow -->
        <svg
            class="w-3.5 h-3.5 text-white/20 group-hover:text-[#C1121F] transition-colors flex-shrink-0"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
        >
            <line x1="7" y1="17" x2="17" y2="7"/>
            <polyline points="7 7 17 7 17 17"/>
        </svg>
    </a>
</template>

<script setup lang="ts">
const props = defineProps<{
    url: string
    index: number
}>()

const getExtension = (url: string) => {
  const match = url.split('?')[0].split('.').pop()
  return match ? match.toUpperCase() : 'FILE'
}
</script>