<template>
    <section class="h-full rounded-xl border border-[#222] bg-[#1a1a1a] p-6">
        <div class="mb-5">
            <h2 class="text-base font-bold text-white">Quick actions</h2>
            <p class="mt-1 text-xs text-gray-500">Common administrative tasks</p>
        </div>

        <div
            class="grid gap-3"
            :class="compact ? 'grid-cols-1' : 'grid-cols-1 sm:grid-cols-3'"
        >
            <button
                v-for="action in quickActions"
                :key="action.key"
                type="button"
                class="flex items-center gap-3 rounded-lg border border-[#292929] bg-[#222] p-4 text-left transition hover:border-[#C1121F] hover:bg-[#252525]"
                @click="emit('select', action.key)"
            >
                <div class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-[#C1121F]">
                    <span class="text-sm text-white">+</span>
                </div>

                <div class="min-w-0">
                    <p class="text-xs font-semibold text-white">{{ action.label }}</p>
                    <p class="mt-1 text-[10px] text-gray-500">{{ action.description }}</p>
                </div>
            </button>
        </div>
    </section>
</template>

<script setup lang="ts">
type DashboardQuickAction = 'car' | 'booking' | 'user'

withDefaults(defineProps<{ compact?: boolean }>(), {
    compact: false,
})

const emit = defineEmits<{
    select: [action: DashboardQuickAction]
}>()

const quickActions: Array<{
    key: DashboardQuickAction
    label: string
    description: string
}> = [
    {
        key: 'car',
        label: 'Add car',
        description: 'Add a vehicle to your fleet',
    },
    {
        key: 'booking',
        label: 'Add booking',
        description: 'Add a booking for your customer',
    },
    {
        key: 'user',
        label: 'Add user',
        description: 'Create a new customer account',
    },
]
</script>
