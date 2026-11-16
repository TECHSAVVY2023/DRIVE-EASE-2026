<template>
    <div class="rounded-xl border border-[#222] bg-[#1a1a1a] p-6">
        <div class="mb-6">
            <h2 class="text-base font-bold text-white">Fleet status</h2>
            <p class="mt-1 text-xs text-gray-500">Current vehicle condition</p>
        </div>

        <div v-if="loading" class="flex h-36 items-center justify-center text-xs text-gray-500">
            Loading fleet status...
        </div>
        <div v-else-if="error" class="flex h-36 items-center justify-center text-xs text-red-400">
            {{ error }}
        </div>
        <div v-else-if="items.length" class="space-y-5">
            <div v-for="item in items" :key="item.label">
                <div class="mb-2 flex justify-between">
                    <span class="text-xs text-gray-400">{{ item.label }}</span>
                    <span class="text-xs font-semibold text-white">{{ item.value }}</span>
                </div>
                <div class="h-2 overflow-hidden rounded-full bg-[#292929]">
                    <div
                        class="h-full rounded-full bg-[#C1121F]"
                        :style="{ width: `${item.percentage}%` }"
                    />
                </div>
            </div>
        </div>
        <p v-else class="flex h-36 items-center justify-center text-xs text-gray-500">
            No vehicles in the fleet yet.
        </p>

        <NuxtLink
            to="/admin/admin-fleet"
            class="mt-7 block w-full rounded-lg border border-[#303030] py-2.5 text-center text-xs font-semibold text-gray-300 transition hover:bg-[#222]"
        >
            View fleet
        </NuxtLink>
    </div>
</template>

<script setup lang="ts">
import type { DashboardFleetStatusItem } from '~/utils/types/dashboard'

const { fetchFleetStatus } = useDashboard()
const items = ref<DashboardFleetStatusItem[]>([])
const loading = ref(false)
const error = ref('')

const loadFleetStatus = async () => {
    loading.value = true
    error.value = ''
    try {
        items.value = (await fetchFleetStatus()).items
    } catch (fetchError) {
        console.error('Failed to load fleet status:', fetchError)
        error.value = 'Unable to load fleet status.'
    } finally {
        loading.value = false
    }
}

onMounted(loadFleetStatus)
</script>
