<template>
    <div class="flex flex-col gap-4 w-full">
        <div class="flex flex-col">
            <label class="text-gray-400 text-xs">Pickup date</label>
            <VueDatePicker
                v-model="form.pickupDate"
                :min-date="today"
                :enable-time-picker="true"
                :flow="flow"
                :time-config="{ is24: false }"
                dark
            />
        </div>

        <div
            v-if="form.pickupDate && occupiedPeriods.length"
            class="rounded-lg border border-amber-500/20 bg-amber-500/5 p-3"
        >
            <div class="mb-2 flex items-center justify-between gap-3">
                <p class="text-xs font-semibold text-amber-300">
                    Unavailable around your selection
                </p>
                <span class="text-[10px] text-amber-200/70">
                    Includes 1-hour turnover
                </span>
            </div>

            <div class="space-y-1.5">
                <p
                    v-for="period in occupiedPeriods"
                    :key="`${period.pickup_date}-${period.return_date}`"
                    class="rounded-md bg-black/20 px-2 py-1.5 text-[11px] text-gray-200"
                >
                    {{ formatBookingRange(period) }}
                </p>
            </div>

            <p
                v-if="bookingConflict"
                class="mt-2 text-[11px] leading-4 text-red-300"
            >
                Your selected pickup or return time overlaps an unavailable period.
            </p>
        </div>

        <p
            v-else-if="form.pickupDate"
            class="text-green-400 text-xs"
        >
            No occupied times near this selection.
        </p>

        <div class="flex flex-col gap-1.5">
            <label class="text-gray-400 text-xs">Pickup location</label>
            <input
                v-model="form.pickupLocation"
                type="text"
                required
                placeholder="e.g. Cagayan De Oro City"
                class="
                    rounded-lg px-3 py-2.5 text-white text-sm 
                    bg-[#0f0f0f] border border-[#2a2a2a]
                    placeholder:text-neutral-600
                "
            />
        </div>

        <div class="flex flex-col gap-1.5">
            <label class="text-gray-400 text-xs">Return date</label>
            <VueDatePicker
                v-model="form.returnDate"
                :min-date="returnMinDate"
                :enable-time-picker="true"
                :flow="flow"
                :time-config="{ is24: false }"
                dark
            />
        </div>

        <div class="flex flex-col gap-1.5">
            <label class="text-gray-400 text-xs">Return location</label>
            <input
                v-model="form.returnLocation"
                type="text"
                required
                placeholder="e.g. Cagayan De Oro City"
                class="rounded-lg px-3 py-2.5 text-white text-sm bg-[#0f0f0f] border border-[#2a2a2a] placeholder:text-neutral-600"
            />
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { VueDatePicker } from '@vuepic/vue-datepicker'
import type { FlowConfig } from '@vuepic/vue-datepicker'
import type { Car, UnavailablePeriod } from '~/utils/types/fleet'
import { getBookingConflict } from '~/composables/car/useCarRental'

const props = defineProps<{
    form: any
    car: Car
}>()

const flow = {
    steps: ['calendar', 'time'],
} as FlowConfig

const today = new Date()
today.setHours(0, 0, 0, 0)

const returnMinDate = computed(() => {
    const minDate = props.form.pickupDate
        ? new Date(props.form.pickupDate)
        : new Date(today)

    minDate.setHours(0, 0, 0, 0)

    return minDate
})

const occupiedPeriods = computed(() => {
    if (!props.form.pickupDate) return []

    const selectedStart = new Date(props.form.pickupDate)
    const selectedEnd = props.form.returnDate
        ? new Date(props.form.returnDate)
        : new Date(selectedStart)

    if (!props.form.returnDate) {
        selectedEnd.setHours(23, 59, 59, 999)
    }

    const bufferMilliseconds =
        (props.car.availability_buffer_minutes ?? 60) * 60 * 1000

    return props.car.unavailable_periods.filter(period => {
        const pickup = new Date(period.pickup_date)
        const returnDate = period.is_overdue
            ? Infinity
            : new Date(period.return_date).getTime()

        if (period.is_overdue) {
            return pickup <= selectedEnd
        }

        return (
            pickup.getTime() - bufferMilliseconds < selectedEnd.getTime() &&
            returnDate + bufferMilliseconds > selectedStart.getTime()
        )
    })
})

const bookingConflict = computed(() => {
    if (!props.form.pickupDate || !props.form.returnDate) return null

    return getBookingConflict(
        new Date(props.form.pickupDate),
        new Date(props.form.returnDate),
        props.car.unavailable_periods,
        props.car.availability_buffer_minutes,
    )
})

const formatBookingRange = (period: UnavailablePeriod) => {
    if (period.is_overdue) return 'Currently overdue — unavailable until resolved'

    const formatOptions = {
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
    } as const

    return `${new Date(period.pickup_date).toLocaleString('en-PH', formatOptions)} – ${new Date(period.return_date).toLocaleString('en-PH', formatOptions)}`
}


</script>
