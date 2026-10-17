<script setup lang="ts">
import { computed } from 'vue'

interface StatCard {
    label: string
    value: string
    icon: 'bookings' | 'revenue' | 'rentals' | 'customers'
}

interface FleetRow {
    category: string
    inUse: number
    total: number
}

const today = new Date()
const formattedDate = computed(() =>
    today.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
)

const stats: StatCard[] = [
    { label: 'Bookings', value: '20', icon: 'bookings' },
    { label: 'Revenue', value: '₱184K', icon: 'revenue' },
    { label: 'Active rentals', value: '18', icon: 'rentals' },
    { label: 'Customers', value: '67', icon: 'customers' },
]

const fleet: FleetRow[] = [
    { category: 'Economy', inUse: 8, total: 10 },
    { category: 'Compact', inUse: 6, total: 10 },
    { category: 'SUV', inUse: 9, total: 10 },
    { category: 'Luxury', inUse: 5, total: 10 },
]

const navMain = [
    { label: 'Dashboard', active: true },
    { label: 'Notifications', badge: 67 },
    { label: 'Bookings' },
    { label: 'Fleet' },
    { label: 'Users' },
]

const navReport = [
  { label: 'Analytics' },
  { label: 'Activity logs' },
]

const quickActions = ['Add users', 'Add cars', 'Add rental']
</script>

<template>
    <div class="flex min-h-screen bg-neutral-950 text-neutral-100">
        <!-- Sidebar -->
        <aside class="hidden w-60 shrink-0 border-r border-white/5 bg-black md:flex md:flex-col">
        <div class="flex items-center gap-2 px-5 py-5">
            <div class="flex h-8 w-8 items-center justify-center rounded-full bg-red-700 text-xs font-bold">
            DE
            </div>
            <span class="text-sm font-bold tracking-wide">DRIVEEASE</span>
        </div>

        <nav class="flex flex-1 flex-col gap-6 px-3 pt-2">
            <div>
            <p class="px-2 pb-2 text-[11px] font-medium text-neutral-500">Main</p>
            <ul class="space-y-0.5">
                <li v-for="item in navMain" :key="item.label">
                <a
                    href="#"
                    class="flex items-center justify-between rounded-md px-3 py-2 text-sm transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-red-600"
                    :class="item.active
                    ? 'bg-red-700 font-semibold text-white'
                    : 'text-neutral-400 hover:bg-white/5 hover:text-neutral-200'"
                >
                    <span>{{ item.label }}</span>
                    <span
                    v-if="item.badge"
                    class="rounded-full bg-red-600 px-1.5 py-0.5 text-[11px] font-semibold leading-none text-white"
                    >
                    {{ item.badge }}
                    </span>
                </a>
                </li>
            </ul>
            </div>

            <div>
            <p class="px-2 pb-2 text-[11px] font-medium text-neutral-500">Report</p>
            <ul class="space-y-0.5">
                <li v-for="item in navReport" :key="item.label">
                <a
                    href="#"
                    class="flex items-center rounded-md px-3 py-2 text-sm text-neutral-400 transition-colors hover:bg-white/5 hover:text-neutral-200 focus-visible:outline focus-visible:outline-2 focus-visible:outline-red-600"
                >
                    {{ item.label }}
                </a>
                </li>
            </ul>
            </div>
        </nav>
        </aside>

        <!-- Main -->
        <div class="flex min-w-0 flex-1 flex-col">
        <!-- Topbar -->
        <header class="flex flex-wrap items-center justify-between gap-3 border-b border-white/5 bg-black px-6 py-5">
            <div>
            <h1 class="text-xl font-bold text-white">Dashboard</h1>
            <p class="text-sm text-neutral-400">{{ formattedDate }}</p>
            </div>
            <button
            type="button"
            class="flex items-center gap-2 rounded-full border border-white/10 py-1 pl-1 pr-3 text-sm transition-colors hover:bg-white/5 focus-visible:outline focus-visible:outline-2 focus-visible:outline-red-600"
            >
            <span class="flex h-7 w-7 items-center justify-center rounded-full bg-neutral-700 text-xs font-semibold">
                Z
            </span>
            <span>Hi, Zen</span>
            </button>
        </header>

        <main class="flex-1 space-y-6 p-6">
            <!-- Summary -->
            <section>
            <div class="mb-4 flex items-end justify-between gap-3">
                <div>
                <h2 class="text-lg font-bold text-white">Summary</h2>
                <p class="text-sm text-neutral-400">Overview for this month</p>
                </div>
                <button
                type="button"
                class="rounded-md border border-white/10 px-3 py-1.5 text-sm text-neutral-300 transition-colors hover:bg-white/5 focus-visible:outline focus-visible:outline-2 focus-visible:outline-red-600"
                >
                This month
                </button>
            </div>

            <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
                <div
                v-for="stat in stats"
                :key="stat.label"
                class="rounded-xl border border-white/5 bg-neutral-900 p-5"
                >
                <div class="mb-4 flex h-10 w-10 items-center justify-center rounded-lg bg-red-700/90">
                    <!-- bookings -->
                    <svg v-if="stat.icon === 'bookings'" class="h-5 w-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="6" y="4" width="12" height="17" rx="1.5" />
                    <path d="M9 4V3a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v1" />
                    <path d="M9 11h6M9 15h4" />
                    </svg>
                    <!-- revenue -->
                    <svg v-else-if="stat.icon === 'revenue'" class="h-5 w-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="9" />
                    <path d="M9.5 9.5c0-1 1-1.8 2.5-1.8s2.5.8 2.5 1.8-1 1.5-2.5 1.8-2.5.8-2.5 1.9 1 1.8 2.5 1.8 2.5-.8 2.5-1.8" />
                    </svg>
                    <!-- rentals -->
                    <svg v-else-if="stat.icon === 'rentals'" class="h-5 w-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M13 2 4 14h6l-1 8 9-12h-6l1-8Z" />
                    </svg>
                    <!-- customers -->
                    <svg v-else class="h-5 w-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="9" cy="8" r="3" />
                    <path d="M2 20c0-3.3 3.1-5.5 7-5.5s7 2.2 7 5.5" />
                    <path d="M16 8.5a3 3 0 1 1 3.5 2.96" />
                    <path d="M17 14.6c2.4.5 4 2.2 4 4.4" />
                    </svg>
                </div>
                <p class="text-sm text-neutral-400">{{ stat.label }}</p>
                <p class="mt-1 text-2xl font-bold text-white">{{ stat.value }}</p>
                </div>
            </div>
            </section>

            <!-- Fleet + Quick actions -->
            <section class="grid grid-cols-1 gap-6 xl:grid-cols-2">
            <div class="rounded-xl border border-white/5 bg-neutral-900 p-5">
                <h3 class="mb-4 text-base font-bold text-white">Fleet overview</h3>
                <ul class="space-y-4">
                <li v-for="row in fleet" :key="row.category" class="flex items-center gap-4">
                    <span class="w-20 shrink-0 text-sm text-neutral-300">{{ row.category }}</span>
                    <div
                    class="h-2 flex-1 overflow-hidden rounded-full bg-white/10"
                    role="progressbar"
                    :aria-valuenow="row.inUse"
                    aria-valuemin="0"
                    :aria-valuemax="row.total"
                    :aria-label="`${row.category} in use`"
                    >
                    <div
                        class="h-full rounded-full bg-red-600"
                        :style="{ width: `${(row.inUse / row.total) * 100}%` }"
                    />
                    </div>
                    <span class="w-12 shrink-0 text-right text-sm text-neutral-400">{{ row.inUse }}/{{ row.total }}</span>
                </li>
                </ul>
            </div>

            <div class="rounded-xl border border-white/5 bg-neutral-900 p-5">
                <h3 class="mb-4 text-base font-bold text-white">Quick actions</h3>
                <div class="space-y-3">
                <button
                    v-for="action in quickActions"
                    :key="action"
                    type="button"
                    class="w-full rounded-lg bg-red-700 py-3 text-sm font-semibold text-white transition-colors hover:bg-red-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-400"
                >
                    {{ action }}
                </button>
                </div>
            </div>
            </section>
        </main>
        </div>
    </div>
</template>