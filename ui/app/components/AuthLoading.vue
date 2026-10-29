<template>
    <div
        class="flex items-center justify-center text-[#9E9E9E]"
        :class="compact ? 'min-h-10 gap-2 px-3' : 'min-h-56 flex-col gap-4 px-6 py-12'"
        role="status"
        aria-live="polite"
    >
        <span
            class="block animate-spin rounded-full border-[#C1121F] border-t-transparent"
            :class="compact ? 'h-5 w-5 border-2' : 'h-10 w-10 border-[3px]'"
            aria-hidden="true"
        ></span>

        <span :class="compact ? 'sr-only' : 'text-sm font-medium'">
            {{ message }}
        </span>
    </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
    message?: string
    compact?: boolean
}>(), {
    message: 'Loading your account...',
    compact: false,
})
</script>
