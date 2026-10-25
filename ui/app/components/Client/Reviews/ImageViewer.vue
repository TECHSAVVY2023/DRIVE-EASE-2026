<template>
    <Teleport to="body">
        <Transition
            enter-active-class="transition duration-200"
            leave-active-class="transition duration-150"
            enter-from-class="opacity-0"
            leave-to-class="opacity-0"
        >
            <div
                v-if="open"
                class="fixed inset-0 z-[10000] flex flex-col bg-black/95 p-3 sm:p-6"
                role="dialog"
                aria-modal="true"
                aria-label="Review image viewer"
                @click.self="close"
            >
                <div class="flex items-center justify-between pb-3 text-white">
                    <span class="text-sm font-medium text-white/70">
                        {{ activeIndex + 1 }} / {{ images.length }}
                    </span>

                    <button
                        type="button"
                        class="flex h-10 w-10 items-center justify-center rounded-full bg-white/10 transition hover:bg-white/20 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white"
                        aria-label="Close image viewer"
                        @click="close"
                    >
                        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" d="M6 6l12 12M18 6 6 18" />
                        </svg>
                    </button>
                </div>

                <div class="relative flex min-h-0 flex-1 items-center justify-center" @click.self="close">
                    <button
                        v-if="images.length > 1"
                        type="button"
                        class="absolute left-0 z-10 flex h-11 w-11 items-center justify-center rounded-full bg-black/60 text-white transition hover:bg-[#C1121F] sm:left-3"
                        aria-label="Previous image"
                        @click="showPrevious"
                    >
                        <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m15 18-6-6 6-6" />
                        </svg>
                    </button>

                    <img
                        :src="images[activeIndex]"
                        :alt="`Review image ${activeIndex + 1}`"
                        class="max-h-full max-w-full select-none object-contain"
                    />

                    <button
                        v-if="images.length > 1"
                        type="button"
                        class="absolute right-0 z-10 flex h-11 w-11 items-center justify-center rounded-full bg-black/60 text-white transition hover:bg-[#C1121F] sm:right-3"
                        aria-label="Next image"
                        @click="showNext"
                    >
                        <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m9 18 6-6-6-6" />
                        </svg>
                    </button>
                </div>

                <div v-if="images.length > 1" class="flex justify-center gap-2 overflow-x-auto pt-4">
                    <button
                        v-for="(image, index) in images"
                        :key="`thumbnail-${image}-${index}`"
                        type="button"
                        class="h-14 w-16 shrink-0 overflow-hidden rounded-md border-2 transition"
                        :class="index === activeIndex ? 'border-[#C1121F]' : 'border-transparent opacity-55 hover:opacity-100'"
                        :aria-label="`Show image ${index + 1}`"
                        @click="activeIndex = index"
                    >
                        <img :src="image" alt="" class="h-full w-full object-cover" />
                    </button>
                </div>
            </div>
        </Transition>
    </Teleport>
</template>

<script setup lang="ts">
const props = withDefaults(defineProps<{
    images: string[]
    initialIndex?: number
}>(), {
    initialIndex: 0,
})

const open = defineModel<boolean>({ required: true })
const activeIndex = ref(0)

const setInitialIndex = () => {
    activeIndex.value = Math.min(
        Math.max(props.initialIndex, 0),
        Math.max(props.images.length - 1, 0),
    )
}

const close = () => {
    open.value = false
}

const showPrevious = () => {
    if (!props.images.length) return
    activeIndex.value = (activeIndex.value - 1 + props.images.length) % props.images.length
}

const showNext = () => {
    if (!props.images.length) return
    activeIndex.value = (activeIndex.value + 1) % props.images.length
}

const handleKeydown = (event: KeyboardEvent) => {
    if (!open.value) return

    if (event.key === 'Escape') close()
    if (event.key === 'ArrowLeft') showPrevious()
    if (event.key === 'ArrowRight') showNext()
}

watch(open, (isOpen) => {
    if (!import.meta.client) return

    if (isOpen) setInitialIndex()
    document.documentElement.style.overflow = isOpen ? 'hidden' : ''
})

watch(() => props.initialIndex, () => {
    if (open.value) setInitialIndex()
})

onMounted(() => window.addEventListener('keydown', handleKeydown))

onBeforeUnmount(() => {
    window.removeEventListener('keydown', handleKeydown)
    if (open.value) document.documentElement.style.overflow = ''
})
</script>
