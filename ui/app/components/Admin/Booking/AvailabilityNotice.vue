<template>
    <div
        v-if="selectedPeriods.length"
        class="mb-5 rounded-lg border border-amber-500/20 bg-amber-500/5 p-3"
    >
        <div class="mb-2 flex items-center justify-between gap-3">
            <p class="text-xs font-semibold text-amber-300">
                Unavailable around this schedule
            </p>
            <span class="text-[10px] text-amber-200/70">
                Includes 1-hour turnover
            </span>
        </div>

        <div class="space-y-1.5">
            <p
                v-for="period in selectedPeriods"
                :key="period.booking_reference"
                class="rounded-md bg-black/20 px-2 py-1.5 text-[11px] text-gray-200"
            >
                {{ formatPeriod(period) }}
            </p>
        </div>

        <p v-if="hasConflict" class="mt-2 text-[11px] leading-4 text-red-300">
            The selected times overlap an unavailable period.
        </p>
    </div>
</template>

<script setup lang="ts">
import type { Car, UnavailablePeriod } from '~/utils/types/fleet'
import { getBookingConflict } from '~/composables/car/useCarRental'

const props = defineProps<{
    car: Car | undefined
    pickupDate: string
    returnDate: string
    excludeBookingReference?: string
}>()

const periods = computed(() =>
    (props.car?.unavailable_periods ?? []).filter(
        period => period.booking_reference !== props.excludeBookingReference,
    ),
)

const selectedPeriods = computed(() => {
    if (!props.pickupDate) return []

    const selectedStart = new Date(props.pickupDate)
    const selectedEnd = props.returnDate
        ? new Date(props.returnDate)
        : new Date(selectedStart)

    if (!props.returnDate) {
        selectedEnd.setHours(23, 59, 59, 999)
    }

    const bufferMilliseconds =
        (props.car?.availability_buffer_minutes ?? 60) * 60 * 1000

    return periods.value.filter(period => {
        const pickup = new Date(period.pickup_date)
        const returnDate = period.is_overdue
            ? Infinity
            : new Date(period.return_date).getTime()

        return period.is_overdue
            ? pickup <= selectedEnd
            : pickup.getTime() - bufferMilliseconds < selectedEnd.getTime()
                && returnDate + bufferMilliseconds > selectedStart.getTime()
    })
})

const hasConflict = computed(() => {
    if (!props.pickupDate || !props.returnDate) return false

    return Boolean(getBookingConflict(
        new Date(props.pickupDate),
        new Date(props.returnDate),
        periods.value,
        props.car?.availability_buffer_minutes,
    ))
})

function formatPeriod(period: UnavailablePeriod): string {
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
