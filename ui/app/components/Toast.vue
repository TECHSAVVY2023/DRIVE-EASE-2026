<template>
    <div
        v-if="visible"
        class="
            fixed z-500 top-5 right-5
            w-80 rounded-xl border border-[#c1121f] bg-[#0D0D0D]/80 backdrop-blur-md shadow-lg shadow-black/50 
            text-white overflow-hidden
        "
    >

        <div class="flex items-start gap-3 p-4">
        <!-- icon -->
        <div
            class="mt-0.5 flex h-8 w-8 items-center justify-center rounded-full"
            :class="type === 'success' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'"
        >
            <span v-if="type === 'success'">✔</span>
            <span v-else>⚠</span>
        </div>

        <!-- text -->
        <div class="flex-1">
            <p class="text-sm font-semibold">
                {{ type === 'success' ? 'Success' : 'Error' }}
            </p>
            <p class="text-xs text-gray-300">
                {{ message }}
            </p>
        </div>
        </div>
    </div>
</template>

<script setup>
defineProps({
  message: String,
  type: {
    type: String,
    default: "success",
  },
  visible: Boolean,
})
</script>