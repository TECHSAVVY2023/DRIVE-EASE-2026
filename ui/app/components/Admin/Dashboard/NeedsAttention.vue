<template>
    <div class="rounded-xl border border-[#222] bg-[#1a1a1a] p-6">
        <div class="mb-5">
            <h2 class="text-base font-bold text-white">Needs attention</h2>
            <p class="mt-1 text-xs text-gray-500">Items requiring action</p>
        </div>

        <div v-if="loading" class="flex h-36 items-center justify-center text-xs text-gray-500">
            Loading items...
        </div>
        <div v-else-if="error" class="flex h-36 items-center justify-center text-xs text-red-400">
            {{ error }}
        </div>
        <div v-else class="space-y-3">
            <NuxtLink
                v-for="item in items"
                :key="item.label"
                :to="item.route"
                class="flex items-center gap-3 rounded-lg bg-[#222] p-3 transition hover:bg-[#292929]"
            >
                <div class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-lg bg-[#C1121F]/10">
                    <span class="text-sm text-[#C1121F]">!</span>
                </div>
                <div class="min-w-0 flex-1">
                    <p class="text-xs font-semibold text-white">{{ item.label }}</p>
                    <p class="mt-0.5 text-[10px] text-gray-500">{{ item.description }}</p>
                </div>
                <span class="text-xs font-bold text-white">{{ item.count }}</span>
            </NuxtLink>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { DashboardAttentionItem } from '~/utils/types/dashboard'

const emit = defineEmits<{
    loaded: [hasAttention: boolean]
}>()

const { fetchAttention } = useDashboard()
const items = ref<DashboardAttentionItem[]>([])
const loading = ref(false)
const error = ref('')

const loadAttention = async () => {
    loading.value = true
    error.value = ''
    try {
        const response = await fetchAttention()
        items.value = response.items.filter(item => item.count > 0)
        emit('loaded', items.value.length > 0)
    } catch (fetchError) {
        console.error('Failed to load attention items:', fetchError)
        error.value = 'Unable to load attention items.'
    } finally {
        loading.value = false
    }
}

onMounted(loadAttention)
</script>
