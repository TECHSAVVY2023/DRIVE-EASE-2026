<template>
    <Teleport to="body">
        <Transition
            enter-active-class="transition duration-150"
            leave-active-class="transition duration-100"
            enter-from-class="opacity-0"
            leave-to-class="opacity-0"
        >
        <div
            v-if="open && form"
            class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/70 p-4"
            @click.self="close"
        >
            <div
                class="
                    flex max-h-[90vh] w-full max-w-xl flex-col overflow-hidden 
                    rounded-2xl bg-[#111111] border-t-[#C1121F] border-t-5 shadow-2xl
                "
                role="dialog"
                aria-modal="true"
            >

                <!-- Header -->
                <header class="flex items-start justify-between px-4 sm:px-6 pt-5 sm:pt-4 pb-4 border-b border-white/10">
                    
                    <div>
                        
                        <p class="text-[15px] font-medium text-white">
                            {{ props.isEditing ? 'Edit a booking' : 'Add a booking' }}
                        </p>

                        <p class="mt-0.5 text-xs text-neutral-500">
                            Update the details of this booking
                        </p>

                    </div>

                    <button 
                        @click="close" 
                        class="text-white/40 hover:text-white transition-colors mt-0.5"
                    >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>

                </header>

            <!-- Body -->
            <div class="flex-1 overflow-y-auto px-5 py-5">

                <p :class="section">Booking</p>
                <div class="mb-5 grid grid-cols-1 gap-3 sm:grid-cols-2">
                    
                    <div class="relative">
                        <label :class="label" for="user-search">User</label>

                        <div class="relative">
                            <input
                                id="user-search"
                                v-model="userSearch"
                                :class="[field, 'pr-10']"
                                placeholder="Search user..."
                                @focus="showUserDropdown = true"
                                @blur="hideUserDropdown"
                            />

                            <svg
                                class="pointer-events-none absolute right-3 top-1/2 size-4 -translate-y-1/2 text-neutral-500"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2"
                            >
                                <path
                                    d="m6 9 6 6 6-6"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                />
                            </svg>
                        </div>

                        <div
                            v-if="showUserDropdown"
                            class="absolute left-0 right-0 z-20 mt-1 max-h-48 overflow-y-auto rounded-lg border border-neutral-700 bg-neutral-900 shadow-xl"
                        >
                            <button
                                v-for="user in filteredUsers"
                                :key="user.id"
                                type="button"
                                class="block w-full px-3 py-2 text-left text-sm text-white hover:bg-neutral-800"
                                @mousedown.prevent="selectUser(user)"
                            >
                                {{ user.given_name }} {{ user.family_name }}
                            </button>

                            <p
                                v-if="!filteredUsers.length"
                                class="px-3 py-2 text-xs text-neutral-500"
                            >
                                No users found.
                            </p>
                        </div>
                    </div>

                    <div class="relative">
                        <label :class="label" for="car-search">Car</label>

                        <div class="relative">
                            <input
                                id="car-search"
                                v-model="carSearch"
                                :class="[field, 'pr-10']"
                                placeholder="Search car..."
                                @focus="showCarDropdown = true"
                                @blur="hideCarDropdown"
                            />

                            <svg
                                class="pointer-events-none absolute right-3 top-1/2 size-4 -translate-y-1/2 text-neutral-500"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2"
                            >
                                <path
                                    d="m6 9 6 6 6-6"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                />
                            </svg>
                        </div>

                        <div
                            v-if="showCarDropdown"
                            class="absolute left-0 right-0 z-20 mt-1 max-h-48 overflow-y-auto rounded-lg border border-neutral-700 bg-neutral-900 shadow-xl"
                        >
                            <button
                                v-for="car in filteredCars"
                                :key="car.car_id"
                                type="button"
                                class="block w-full px-3 py-2 text-left text-sm text-white hover:bg-neutral-800"
                                @mousedown.prevent="selectCar(car)"
                            >
                                {{ car.brand }} {{ car.model }}
                            </button>

                            <p
                                v-if="!filteredCars.length"
                                class="px-3 py-2 text-xs text-neutral-500"
                            >
                                No cars found.
                            </p>
                        </div>
                    </div>
                </div>
                                

                <!-- Schedule -->
                <p :class="section">Schedule</p>

                <div class="mb-5 grid grid-cols-1 gap-4 sm:grid-cols-2">
                    <!-- Pickup date -->
                    <div class="flex flex-col gap-1.5">
                        <label class="text-gray-400 text-xs">Pickup date</label>

                        <div class="admin-date-picker">
                            <VueDatePicker
                                v-model="form.pickup_date"
                                :min-date="today"
                                :enable-time-picker="true"
                                :flow="flow"
                                :time-config="{ is24: false }"
                                :disabled-dates="disabledDates"
                                dark
                            />
                        </div>
                        
                    </div>

                    <!-- Pickup location -->
                    <div class="flex flex-col gap-1.5">
                        <label class="text-gray-400 text-xs">Pickup location</label>

                        <input
                            v-model="form.pickup_location"
                            type="text"
                            required
                            placeholder="e.g. Cagayan De Oro City"
                            :class="field"
                        />
                    </div>

                    <!-- Return date -->
                    <div class="flex flex-col gap-1.5">
                        <label class="text-gray-400 text-xs">Return date</label>

                        <div class="admin-date-picker">
                            <VueDatePicker
                                v-model="form.return_date"
                                :min-date="returnMinDate"
                                :enable-time-picker="true"
                                :flow="flow"
                                :time-config="{ is24: false }"
                                :disabled-dates="disabledDates"
                                dark
                            />
                        </div>
                    </div>

                    <!-- Return location -->
                    <div class="flex flex-col gap-1.5">
                        <label class="text-gray-400 text-xs">Return location</label>

                        <input
                            v-model="form.return_location"
                            type="text"
                            required
                            placeholder="e.g. Cagayan De Oro City"
                            :class="field"
                        />
                    </div>
                </div>

                <!-- Discount -->
                <p :class="section">Price</p>
                <div class="mb-5">
                    <label :class="label" for="discount">Discount</label>
                    <div class="relative">
                        <span class="absolute left-3 top-1/2 -translate-y-1/2 text-sm text-neutral-500">
                            ₱
                        </span>
                        <input
                            id="discount"
                            v-model.number="form.discount"
                            type="number"
                            min="0"
                            :max="form.subtotal"
                            :class="[field, 'pl-7']"
                            placeholder="0"
                        />
                    </div>
                </div>

                <!-- Price summary (computed) -->
                <div class="mb-5 rounded-xl border border-neutral-800 bg-[#0f0f0f] px-4 py-3">
                    <div class="flex items-center justify-between">
                        <span class="text-xs text-neutral-400">
                            {{ rentalDays }} day(s) × ₱{{ dailyRate.toLocaleString() }}
                        </span>

                        <span class="text-xs text-neutral-500">
                            ₱{{ subtotalPrice.toLocaleString() }}
                        </span>
                    </div>

                    <div class="mt-1 flex items-center justify-between">
                        <span class="text-xs text-neutral-500">
                            Discount
                        </span>

                        <span class="text-xs text-red-500">
                            -₱{{ Number(form.discount || 0).toLocaleString() }}
                        </span>
                    </div>

                    <div class="mt-2 flex items-center justify-between border-t border-neutral-800 pt-2">
                        <span class="text-sm text-neutral-400">
                            Total
                        </span>

                        <span class="text-base font-semibold text-white">
                            ₱{{ totalPrice.toLocaleString() }}
                        </span>
                    </div>
                </div>

                <!-- Status -->
                <p :class="section">Status</p>
                <div class="mb-3 grid grid-cols-2 gap-2 sm:grid-cols-4">

                    <button
                        v-for="option in STATUSES"
                        :key="option.value"
                        class="rounded-lg py-2 text-xs focus:outline-none focus-visible:ring-2 focus-visible:ring-red-600"
                        :class="
                        form.status === option.value
                            ? option.active
                            : 'border border-neutral-700 text-neutral-400 hover:text-white'
                        "
                        @click="form.status = option.value"
                    >
                        {{ option.label }}
                    </button>

                </div>

                <div v-if="form.status === 'cancelled'" class="mb-3">
                    <p :class="section">Cancel reason</p>

                    <textarea
                        v-model="form.cancel_reason"
                        rows="3"
                        placeholder="Enter cancellation reason"
                        class="
                            w-full rounded-lg border border-neutral-700
                            bg-[#0f0f0f] px-3 py-2 text-sm text-white
                            placeholder:text-neutral-500
                            outline-none focus:border-red-600
                            resize-none
                        "
                    />
                </div>
            </div>

            <!-- Footer -->
            <footer class="flex justify-end gap-2.5 border-t border-neutral-800 px-5 py-4">

                <button
                    class="rounded-lg border border-neutral-700 px-4 py-2 text-xs text-neutral-400 hover:text-white focus:outline-none focus-visible:ring-2 focus-visible:ring-red-600"
                    @click="close"
                    >
                    Cancel
                </button>
                
                <button
                    :disabled="!hasValidDates"
                    class="rounded-lg bg-[#c1121f] px-4 py-2 text-xs font-medium text-white hover:bg-[#b31a27] focus:outline-none focus-visible:ring-2 focus-visible:ring-red-400 disabled:cursor-not-allowed disabled:opacity-50"
                    @click="save"
                >
                    Save changes
                </button>

            </footer>
            </div>
        </div>
        </Transition>
    </Teleport>
</template>

<script setup lang="ts">
import type { BookingForm, Transaction } from '~/utils/types/booking'
import type { User } from '~/utils/types/accounts'
import type { Car } from '~/utils/types/fleet'
import { computed } from 'vue'
import { VueDatePicker } from '@vuepic/vue-datepicker'
import type { FlowConfig } from '@vuepic/vue-datepicker'

const open = defineModel<boolean>({ required: true })

const props = defineProps<{ 
    booking: Transaction | null,
    users: User[],
    cars: Car[],
    isEditing: boolean
}>()

const emit = defineEmits<{
    save: [booking: BookingForm, bookingId: string | null]
    close: []
}>()

// User search

const userSearch = ref('')
const showUserDropdown = ref(false)

const filteredUsers = computed(() => {
    const search = userSearch.value.toLowerCase().trim()

    if (!search) return props.users

    return props.users.filter(user =>
        `${user.given_name} ${user.family_name}`
            .toLowerCase()
            .includes(search)
    )
})

function selectUser(user: User) {
    form.value.user = user.id
    userSearch.value = `${user.given_name} ${user.family_name}`
    showUserDropdown.value = false
}

function hideUserDropdown() {
    setTimeout(() => {
        showUserDropdown.value = false
    }, 150)
}

// Car search

const carSearch = ref('')
const showCarDropdown = ref(false)

const filteredCars = computed(() => {
    const search = carSearch.value.toLowerCase().trim()

    if (!search) return props.cars

    return props.cars.filter(car =>
        `${car.brand} ${car.model}`
            .toLowerCase()
            .includes(search)
    )
})

function selectCar(car: Car) {
    form.value.car = car.car_id
    carSearch.value = `${car.brand} ${car.model}`
    showCarDropdown.value = false
}

function hideCarDropdown() {
    setTimeout(() => {
        showCarDropdown.value = false
    }, 150)
}

// for the date picker

const flow = {
    steps: ['calendar', 'time'],
} as FlowConfig

const today = new Date()
today.setHours(0, 0, 0, 0)

const returnMinDate = computed(() => {
    if (!form.value.pickup_date) {
        return today
    }

    return new Date(form.value.pickup_date)
})

const selectedCar = computed(() =>
    props.cars.find(car => car.car_id === form.value.car)
)

const disabledDates = (date: Date) => {
    return selectedCar.value?.unavailable_periods?.some(period => {
        const start = new Date(period.pickup_date)
        const end = new Date(period.return_date)

        start.setHours(0, 0, 0, 0)
        end.setHours(23, 59, 59, 999)

        return date >= start && date <= end
    }) ?? false
}

const STATUSES = [
    { value: 'pending_payment', label: 'Pending Payment', active: 'bg-[#c1121f] text-white' },
    { value: 'payment_failed', label: 'Pending Failed', active: 'bg-[#c1121f] text-white' },
    { value: 'pending_approval', label: 'Pending Approval', active: 'bg-[#c1121f] text-white' },
    { value: 'confirmed', label: 'Confirmed', active: 'bg-[#c1121f] text-white' },
    { value: 'rejected', label: 'Rejected', active: 'bg-[#c1121f] text-white' },
    { value: 'picked_up', label: 'Picked Up', active: 'bg-[#c1121f] text-white' },
    { value: 'returned', label: 'Returned', active: 'bg-[#c1121f] text-white' },
    { value: 'completed', label: 'Completed', active: 'bg-[#c1121f] text-white' },
    { value: 'cancelled', label: 'Cancelled', active: 'bg-[#c1121f] text-white' },
] as const

const form = ref<BookingForm>(blank())

watch(
    () => [open.value, props.booking] as const,
    ([isOpen, booking]) => {
        if (!isOpen) return

        if (booking) {
            form.value = {
                ...booking,
                user: booking.user.id,
                car: booking.car.car_id,
                cancel_reason: booking.cancel_reason || '',
            }

            const selectedUser = props.users.find(
                user => user.id === booking.user.id
            )

            userSearch.value = selectedUser
                ? `${selectedUser.given_name} ${selectedUser.family_name}`
                : ''

            const selectedCar = props.cars.find(
                car => car.car_id === booking.car.car_id
            )

            carSearch.value = selectedCar
                ? `${selectedCar.brand} ${selectedCar.model}`
                : ''
        } else {
            form.value = blank()
        }
    },
    { immediate: true },
)

const dailyRate = computed(() =>
    Number(selectedCar.value?.price_per_day ?? 0)
)

const rentalDays = computed(() => {
    if (!form.value.pickup_date || !form.value.return_date) return 0

    const ms =
        new Date(form.value.return_date).getTime() -
        new Date(form.value.pickup_date).getTime()

    return Number.isFinite(ms) && ms > 0
        ? Math.ceil(ms / 86_400_000)
        : 0
})

const subtotalPrice = computed(() =>
    rentalDays.value * dailyRate.value
)

const totalPrice = computed(() =>
    Math.max(0, subtotalPrice.value - Number(form.value.discount || 0))
)

const hasValidDates = computed(() => rentalDays.value > 0)

function blank(): BookingForm {
    return {
        booking_reference: '',
        car: '',
        user: 0,

        status: '',
        cancel_reason: '',
        total_price: 0,
        daily_rate: 0,
        number_of_days: 0,
        subtotal: 0,
        discount: 0,

        pickup_date: '',
        return_date: '',
        pickup_location: '',
        return_location: '',
    }
}

function close() {
    open.value = false
    emit('close')
}

function save() {
    const booking = toRaw(form.value)

    form.value.daily_rate = dailyRate.value
    form.value.number_of_days = rentalDays.value
    form.value.subtotal = subtotalPrice.value
    form.value.total_price = totalPrice.value

    emit('save', booking, props.booking?.booking_reference ?? null)
}

const field = `
    w-full rounded-lg
    border border-[#2a2a2a]
    pl-3.5 pr-9 py-2
    bg-[#0f0f0f]
    text-sm text-white
    placeholder:text-neutral-600
    focus:border-[#C1121F]
    focus:outline-none
    [appearance:textfield]
    [&::-webkit-inner-spin-button]:appearance-none
    [&::-webkit-outer-spin-button]:appearance-none
`
const label = 'mb-1.5 block text-[11px] text-neutral-400'
const section = 'mb-2.5 text-[11px] tracking-wide text-red-600'
</script>