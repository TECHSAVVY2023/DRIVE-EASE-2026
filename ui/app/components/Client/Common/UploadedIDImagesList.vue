<template>
    <div v-if="images.length" class="flex flex-col gap-2 mb-2">
        <div
            v-for="(file, index) in images"
            :key="index"
            class="flex items-center justify-between bg-[#0f0f0f] border border-white/10 hover:border-[#c1121f] transition-colors rounded-lg px-3 py-2"
        >
            <!-- Left: file info -->
            <div class="flex items-center gap-3">
                
                <!-- File icon -->
                <div class="w-8 h-8 flex items-center justify-center bg-[#1a1a1a] rounded">
                    <svg class="w-4 h-4 text-[#c1121f]" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    </svg>
                </div>

                <!-- File details -->
                <div class="flex flex-col">
                    <p  @click="openImage(file)" 
                        class="text-white text-xs font-medium truncate max-w-[180px] hover:text-[#c1121f] transition-colors cursor-pointer">
                        {{ file.name }}
                    </p>
                    <p class="text-white/40 text-[10px]">
                        {{ formatFileSize(file.size) }}
                    </p>
                </div>

            </div>

            <!-- Remove button -->
            <button
                @click="$emit('remove-uploaded-id', index)"
                class="text-white/40 hover:text-red-500 transition-colors"
            >
                ✕
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
const props = defineProps<{
    images: File[]
}>()

function openImage(file: File) {
    const url = URL.createObjectURL(file)
    window.open(url, '_blank')

    // Release the object URL after a short delay
    setTimeout(() => URL.revokeObjectURL(url), 1000)
}

defineEmits<{
    (e: 'remove-uploaded-id', index: number): void
}>()

function formatFileSize(bytes: number) {
    if (bytes < 1024 * 1024) {
        return `${(bytes / 1024).toFixed(1)} KB`
    }

    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`
}
</script>