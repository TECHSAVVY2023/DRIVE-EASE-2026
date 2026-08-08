<template>
    <div class="flex flex-col gap-4 w-full">
        <div class="flex flex-col gap-1.5">
            <label class="text-gray-400 text-xs">Pickup date</label>
            <VueDatePicker
                v-model="form.pickupDate"
                :min-date="today"
                :enable-time-picker="true"
                :flow="flow"
                :time-config="{ is24: false }"
                :disabled-dates="disabledDates"
                dark
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
                :disabled-dates="disabledDates"
                dark
            />
        </div>

        <div class="flex flex-col gap-1.5">
            <label class="text-gray-400 text-xs">Pickup location</label>
            <input
                v-model="form.location"
                type="text"
                required
                placeholder="e.g. Cagayan De Oro City"
                class="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg px-3 py-2.5 text-white text-sm placeholder-[#444] focus:outline-none focus:border-[#C1121F] transition-colors duration-200"
            />
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { VueDatePicker } from '@vuepic/vue-datepicker'
import type { FlowConfig } from '@vuepic/vue-datepicker'
import type { Car } from '~/utils/api/api'

const props = defineProps<{
    form: any
    car: Car
}>()

const flow = {
    steps: ['calendar', 'time'],
} as FlowConfig

// Today at 12:00 AM
const today = new Date()
today.setHours(0, 0, 0, 0)

// Return date cannot be before pickup date
const returnMinDate = computed(() => {
    if (!props.form.pickupDate) {
        return today
    }

    return new Date(props.form.pickupDate)
})

const disabledDates = (date: Date) => {
    return props.car.unavailable_periods.some(period => {
        const start = new Date(period.pickup_date)
        const end = new Date(period.return_date)

        start.setHours(0, 0, 0, 0)
        end.setHours(23, 59, 59, 999)

        return date >= start && date <= end
    })
}


</script>