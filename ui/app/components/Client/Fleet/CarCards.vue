<template>
    <div
        v-for="car in paginatedCars"
        :key="car.car_id"
        class="
            bg-[#1a1a1a] rounded-xl border border-[#222] hover:border-[#C1121F]
            transition-colors duration-200 flex flex-col overflow-hidden
        "
    >
        <!-- Clickable Car Content -->
        <NuxtLink
            :to="`/client/car-details/${car.car_id}`"
            class="flex flex-col flex-1"
        >
            <!-- Car Image -->
            <div class="bg-[#141414] h-40 flex items-center justify-center overflow-hidden">
                <img
                    :src="car.meta.primary_image || ''"
                    class="w-full h-full object-cover"
                />
            </div>

            <!-- Info -->
            <div class="p-4 flex flex-col gap-3">
                <div>
                    <h3 class="text-white font-bold text-sm">
                        {{ car.brand }} {{ car.model }}
                    </h3>

                    <p class="text-[#7E7E7E] text-xs mt-0.5">
                        {{ car.seats }} seats · {{ car.transmission }}
                    </p>
                </div>

                <p class="text-white font-bold text-sm">
                    ₱{{ car.price_per_day.toLocaleString() }}/day
                </p>
            </div>
        </NuxtLink>

        <!-- Buttons -->
        <div class="px-4 pb-4 flex flex-col gap-2">

            <!-- Available -->
            <button
                v-if="!useCurrentRental(car)"
                @click="emit('book', car)"
                class="
                    w-full bg-[#C1121F] hover:bg-[#9B0E18]
                    py-2 cursor-pointer text-white 
                    text-xs font-semibold rounded-lg
                    transition-colors duration-200
                "
            >
                Book Now
            </button>

            <!-- Currently rented -->
            <button
                v-else
                @click="emit('book', car)"
                class="
                    w-full bg-[#333] text-[#9E9090]
                    hover:shadow-md hover:shadow-[#333]/50
                    py-2 text-xs font-semibold rounded-lg
                    transition-all duration-200
                "
            >
                Reserve in Advance
            </button>

            <!-- View Details -->
            <NuxtLink
                :to="`/client/car-details/${car.car_id}`"
                class="
                    w-full border border-[#2a2a2a]
                    hover:border-white rounded-lg
                    text-white text-xs font-semibold
                    py-2 transition-all duration-200 text-center
                "
            >
                View Details
            </NuxtLink>

        </div>
    </div>
</template>

<script setup lang="ts">
import type { Car } from '~/utils/api/api'

defineProps<{
    paginatedCars: Car[]
}>()

const emit = defineEmits<{
    book: [car: Car]
}>()

const openBookingModal = (car: Car) => {
    emit('book', car)
}
</script>