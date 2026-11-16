<template>
    <div>
        <label :for="id" class="mb-1.5 block text-[11px] text-neutral-400">{{ label }}</label>
        <input
            :id="id"
            v-model="model"
            :type="type"
            class="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3.5 py-2.5 text-[13px] text-[#d4d4d4] outline-none transition-colors placeholder:text-[#555] focus:border-[#C1121F]"
        >
    </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{ id: string; label: string; type?: string }>(), { type: 'text' })
const model = defineModel<string | null>({ required: true })
</script>
