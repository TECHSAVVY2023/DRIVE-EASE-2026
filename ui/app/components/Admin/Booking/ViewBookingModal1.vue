<script setup lang="ts">
export interface BookingDetails {
    id: string // e.g. 'BKG-89213BE203'
    created_at: string
    status: 'pending' | 'active' | 'completed' | 'cancelled'
    user: { name: string; email: string; contact?: string }
    car: { brand: string; model: string; year: number; price_per_day: number; image?: string }
    pickup_date: string
    pickup_location: string
    return_date: string
    return_location: string
    discount: number
    number_of_days: number
    subtotal: number
    total_price: number
    id_images?: string[]
}

const open = defineModel<boolean>({ required: true })

defineProps<{ booking: BookingDetails | null }>()
const emit = defineEmits<{ edit: [booking: BookingDetails] }>()

const STATUS_STYLES: Record<BookingDetails['status'], string> = {
    pending: 'text-amber-400 bg-amber-500/10 border-amber-500/20',
    active: 'text-blue-400 bg-blue-500/10 border-blue-500/20',
    completed: 'text-green-400 bg-green-500/10 border-green-500/20',
    cancelled: 'text-red-400 bg-red-500/10 border-red-500/20',
}

const peso = (n: number) => `₱${n.toLocaleString()}`
const fmtDateTime = (d: string) =>
    new Date(d).toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
})

function close() {
    open.value = false
}

const section = 'mb-3 text-xs text-[#C1121F]'
const label = 'mb-1.5 block text-xs text-[#929292]'
const value = 'text-sm font-medium text-white'
</script>

<template>
    <Teleport to="body">
        <Transition
        enter-active-class="transition-opacity duration-200"
        leave-active-class="transition-opacity duration-200"
        enter-from-class="opacity-0"
        leave-to-class="opacity-0"
        >
        <div
            v-if="open && booking"
            class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/70 p-0 sm:p-4"
            @click.self="close"
        >
            <div
            class="flex h-[100dvh] w-full max-w-xl flex-col overflow-hidden rounded-none border-t-[5px] border-t-[#C1121F] bg-[#111111] sm:h-auto sm:max-h-[90dvh] sm:rounded-xl"
            role="dialog"
            aria-modal="true"
            >
            <!-- Header -->
            <header
                class="flex shrink-0 items-start justify-between border-b border-[#222] px-6 pb-4 pt-6"
            >
                <div>
                <h2 class="text-lg font-extrabold text-white">Booking details</h2>
                <p class="mt-1 text-xs text-[#929292]">Review the details of this booking</p>
                </div>
                <button
                class="rounded-md p-1 text-[#929292] transition-colors hover:text-white focus:outline-none focus-visible:ring-2 focus-visible:ring-[#C1121F]"
                aria-label="Close"
                @click="close"
                >
                <Icon name="tabler:x" class="size-5" />
                </button>
            </header>

            <!-- Body -->
            <div class="scroll-container flex-1 overflow-y-auto px-6 py-5">
                <!-- Reference + status -->
                <div class="mb-6 flex items-start justify-between gap-3">
                <div class="min-w-0">
                    <p class="truncate text-base font-bold text-white">{{ booking.id }}</p>
                    <p class="mt-0.5 text-xs text-[#929292]">
                    Booked on {{ fmtDateTime(booking.created_at) }}
                    </p>
                </div>
                <span
                    class="shrink-0 rounded-md border px-2.5 py-1 text-xs font-medium capitalize"
                    :class="STATUS_STYLES[booking.status]"
                >
                    {{ booking.status }}
                </span>
                </div>

                <!-- Booking -->
                <p :class="section">Booking</p>
                <div class="mb-6 grid grid-cols-1 gap-5 sm:grid-cols-2">
                    <div>
                        <span :class="label">User</span>
                        <div class="flex items-center gap-3">
                        <div
                            class="flex size-9 shrink-0 items-center justify-center rounded-full bg-[#C1121F] text-sm font-bold text-white"
                        >
                            {{ booking.user.name.charAt(0) }}
                        </div>
                        <div class="min-w-0">
                            <p :class="[value, 'truncate']">{{ booking.user.name }}</p>
                            <p class="truncate text-xs text-[#929292]">{{ booking.user.email }}</p>
                            <p v-if="booking.user.contact" class="truncate text-xs text-[#929292]">
                            {{ booking.user.contact }}
                            </p>
                        </div>
                        </div>
                    </div>

                    <div>
                        <span :class="label">Car</span>
                        <div class="flex items-center gap-3">
                        <div
                            class="flex size-9 w-12 shrink-0 items-center justify-center overflow-hidden rounded bg-[#1a1a1a]"
                        >
                            <img
                            v-if="booking.car.image"
                            :src="booking.car.image"
                            :alt="`${booking.car.brand} ${booking.car.model}`"
                            class="size-full object-cover"
                            />
                            <Icon v-else name="tabler:car" class="size-4 text-[#3a3a3a]" />
                        </div>
                        <div class="min-w-0">
                            <p :class="[value, 'truncate']">
                            {{ booking.car.brand }} {{ booking.car.model }}
                            </p>
                            <p class="text-xs text-[#929292]">{{ booking.car.year }}</p>
                        </div>
                        </div>
                    </div>
                </div>

                <!-- Schedule -->
                <p :class="section">Schedule</p>
                <div class="mb-6 grid grid-cols-1 gap-5 sm:grid-cols-2">
                <div>
                    <span :class="label">Pickup date</span>
                    <p :class="value">{{ fmtDateTime(booking.pickup_date) }}</p>
                </div>
                <div>
                    <span :class="label">Pickup location</span>
                    <p :class="value">{{ booking.pickup_location }}</p>
                </div>
                <div>
                    <span :class="label">Return date</span>
                    <p :class="value">{{ fmtDateTime(booking.return_date) }}</p>
                </div>
                <div>
                    <span :class="label">Return location</span>
                    <p :class="value">{{ booking.return_location }}</p>
                </div>
                </div>

                <!-- Price -->
                <p :class="section">Price</p>
                <div class="mb-6 rounded-xl border border-[#222] px-5 py-4">
                <div class="flex justify-between gap-3 text-sm text-[#929292]">
                    <span>{{ booking.number_of_days }} day(s) × {{ peso(booking.car.price_per_day) }}</span>
                    <span>{{ peso(booking.subtotal) }}</span>
                </div>
                <div class="mt-2 flex justify-between gap-3 text-sm">
                    <span class="text-[#929292]">Discount</span>
                    <span class="text-[#C1121F]">-{{ peso(booking.discount) }}</span>
                </div>
                <div class="mt-3 flex items-center justify-between gap-3 border-t border-[#222] pt-3">
                    <span class="text-sm text-white">Total</span>
                    <span class="text-lg font-bold text-white">{{ peso(booking.total_price) }}</span>
                </div>
                </div>

                <!-- Valid IDs -->
                <p :class="section">Valid IDs</p>
                <div v-if="booking.id_images?.length" class="grid grid-cols-1 gap-3 sm:grid-cols-2">
                <a
                    v-for="(url, index) in booking.id_images"
                    :key="url"
                    :href="url"
                    target="_blank"
                    class="group relative aspect-[16/10] overflow-hidden rounded-lg border border-[#222] bg-[#0f0f0f]"
                >
                    <img :src="url" :alt="`Valid ID ${index + 1}`" class="size-full object-cover" />
                    <span
                    class="absolute inset-x-0 bottom-0 bg-black/70 px-3 py-1.5 text-xs text-white transition-colors group-hover:text-[#C1121F]"
                    >
                    Valid ID {{ index + 1 }}
                    </span>
                </a>
                </div>
                <p v-else class="text-sm text-[#929292]">No IDs uploaded.</p>
            </div>

            <!-- Footer -->
            <footer class="flex shrink-0 justify-end gap-3 border-t border-[#222] px-6 py-4">
                <button
                class="rounded-lg border border-[#2a2a2a] px-5 py-2.5 text-sm font-semibold text-white transition-colors hover:border-white"
                @click="close"
                >
                Close
                </button>
                <button
                class="rounded-lg bg-[#C1121F] px-5 py-2.5 text-sm font-bold text-white transition-colors hover:bg-red-700"
                @click="emit('edit', booking)"
                >
                Edit booking
                </button>
            </footer>
            </div>
        </div>
        </Transition>
    </Teleport>
</template>