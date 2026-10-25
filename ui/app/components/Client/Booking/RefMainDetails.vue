<template>
    <!-- MAIN CARD -->
    <div class="smoked-charcoal-panel lg:col-span-2 rounded-2xl p-5 sm:p-6">

        <!-- Header -->
        <div class="flex items-start justify-between gap-4">

            <div class="flex items-center gap-4">
                <img
                    :src="props.booking?.car.image"
                    :alt="`${props.booking?.car.brand} ${props.booking?.car.model}`"
                    class="h-16 w-20 sm:h-18 sm:w-22 rounded-xl object-cover shrink-0"
                />
                <div>
                    <h1 class="text-lg sm:text-xl font-semibold text-white">{{ props.booking?.car.brand }} {{ props.booking?.car.model }}</h1>
                    <p class="text-sm text-gray-400 mt-0.5">₱{{ props.booking?.daily_rate }} / day</p>
                </div>
            </div>

        </div>

        <div class="h-px bg-white/10 my-5"></div>

        <!-- Renter Information -->
        <section>
            <h2 class="text-xs font-semibold tracking-wider text-gray-500 uppercase">Renter Information</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-4 mt-4">
                <div>
                    <p class="text-xs text-gray-500">Name</p>
                    <p class="text-sm font-medium text-white mt-1">{{ props.booking?.user.first_name }} {{ props.booking?.user.last_name }}</p>
                </div>
                <div>
                    <p class="text-xs text-gray-500">Contact</p>
                    <p class="text-sm font-medium text-white mt-1">{{ props.booking?.user.contact_number }}</p>
                </div>
                <div>
                    <p class="text-xs text-gray-500">Address</p>
                    <p class="text-sm font-medium text-white mt-1">{{ props.booking?.user.address }}</p>
                </div>
                <div>
                    <p class="text-xs text-gray-500">Duration</p>
                    <p class="text-sm font-medium text-white mt-1">{{ props.booking?.number_of_days }} day(s)</p>
                </div>
            </div>
        </section>

        <div class="h-px bg-white/10 my-5"></div>

        <!-- Schedule -->
        <section>
            <h2 class="text-xs font-semibold tracking-wider text-gray-500 uppercase">Schedule</h2>
            <div class="mt-4 space-y-3">
                <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1">
                    <p class="text-xs text-gray-500 sm:w-20 shrink-0">Pickup</p>
                    <p class="text-sm font-medium text-white sm:text-right">
                        {{ formatDateTime(props.booking?.pickup_date) }} &middot; {{ props.booking?.pickup_location }}
                    </p>
                </div>
                <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1">
                    <p class="text-xs text-gray-500 sm:w-20 shrink-0">Return</p>
                    <p class="text-sm font-medium text-white sm:text-right">
                        {{ formatDateTime(props.booking?.return_date) }} &middot; {{ props.booking?.return_location }}
                    </p>
                </div>
            </div>
        </section>

        <div class="h-px bg-white/10 my-5"></div>

        <!-- Uploaded IDs -->
        <section>

            <h2 class="text-xs font-semibold tracking-wider text-gray-500 uppercase">Uploaded IDs</h2>
            
            <div class="flex flex-col gap-2 pt-4">
                <ClientProfileIDImageItems
                    v-for="(url, index) in props.booking?.user.id_images.images"
                    :key="'id-' + index"
                    :url="url"
                    :index="Number(index)"
                />
            </div>

        </section>
    </div>
</template>

<script setup lang="ts">
import type { Transaction } from '~/utils/types/booking'

const props = defineProps<{
    booking: Transaction | null
}>()

const formatDateTime = (date: string | null | undefined) => {
    if (!date) return null

    return new Date(date).toLocaleString('en-PH', {
        month: 'long',
        day: 'numeric',
        year: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true,
    })
}
</script>
