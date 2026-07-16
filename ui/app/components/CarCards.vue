<template>
    <NuxtLink
        v-for="car in paginatedCars"
        :key="car.car_id"
        :to="`/client/car-details/${car.car_id}`"
        class="
            bg-[#1a1a1a] rounded-xl border border-[#222] hover:border-[#C1121F]
            transition-colors duration-200 flex flex-col overflow-hidden"
    >
        <!-- Car Image -->
        <div class="bg-[#141414] h-40 flex items-center justify-center overflow-hidden">
            <img
                :src="car.meta.primary_image || ''"
                class="w-full h-full object-cover"
            />
        </div>

        <!-- Info -->
        <div class="p-4 flex flex-col gap-3 flex-1">

            <div>
                <h3 class="text-white font-bold text-sm">{{ car.brand }} {{ car.model }}</h3>
                <p class="text-[#7E7E7E] text-xs mt-0.5">{{ car.seats }} seats · {{ car.transmission }}</p>
            </div>

            <p class="text-white font-bold text-sm">₱{{ car.price_per_day.toLocaleString() }}/day</p>

            <div class="flex flex-col gap-2 mt-auto">

                <button 
                    @click.stop.prevent="openBookingModal(car)"
                    class="
                        w-full bg-[#C1121F] hover:bg-[#9B0E18] py-2 
                        text-white text-xs font-semibold
                        rounded-lg transition-colors duration-200
                    "
                >
                    Book
                </button>

                <button class="
                    w-full border border-white hover:bg-white rounded-lg
                    text-white text-xs font-semibold hover:text-[#C1121F] py-2
                    transition-colors duration-200
                    "
                >
                    View
                </button>

            </div>

        </div>
    </NuxtLink>
</template>

<script setup lang="ts">
import type { Car } from '~/utils/api/api.ts'

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