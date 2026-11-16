<template>
    <div
        class="relative flex shrink-0 items-center justify-center overflow-hidden rounded-full bg-[#C1121F]"
    >
        <slot name="fallback">
            <svg
                class="h-1/2 w-1/2 text-white"
                fill="currentColor"
                viewBox="0 0 24 24"
                aria-hidden="true"
            >
                <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z" />
            </svg>
        </slot>

        <!-- Keep the fallback visible until the browser confirms the image loaded. -->
        <img
            v-if="src && !gaveUpLoading"
            :key="`${src}-${loadAttempt}`"
            :src="src"
            :alt="alt"
            referrerpolicy="no-referrer"
            class="absolute inset-0 h-full w-full object-cover transition-opacity duration-150"
            :class="imageLoaded ? 'opacity-100' : 'opacity-0'"
            @load="handleImageLoad"
            @error="handleImageError"
        />
    </div>
</template>

<script setup lang="ts">
const props = withDefaults(defineProps<{
    src?: string | null
    alt?: string
}>(), {
    src: null,
    alt: 'User profile picture',
})

const imageLoaded = ref(false)
const gaveUpLoading = ref(false)
const loadAttempt = ref(0)
let retryTimer: ReturnType<typeof setTimeout> | null = null

const clearRetryTimer = (): void => {
    if (retryTimer) {
        clearTimeout(retryTimer)
        retryTimer = null
    }
}

const resetImageState = (): void => {
    clearRetryTimer()
    imageLoaded.value = false
    gaveUpLoading.value = false
    loadAttempt.value = 0
}

const handleImageLoad = (): void => {
    clearRetryTimer()
    imageLoaded.value = true
}

const handleImageError = (): void => {
    imageLoaded.value = false

    // Retry short-lived Google/CDN failures twice, then keep the safe fallback.
    if (loadAttempt.value < 2) {
        retryTimer = setTimeout(() => {
            loadAttempt.value += 1
            retryTimer = null
        }, 1000)
        return
    }

    gaveUpLoading.value = true
}

watch(() => props.src, resetImageState)
onBeforeUnmount(clearRetryTimer)
</script>
