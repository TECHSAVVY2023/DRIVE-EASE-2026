<template>
    <div class="smoked-charcoal-panel w-full rounded-lg px-6 py-6 font-[poppins]">
        <div class="mb-4 flex items-center justify-between gap-4">
            <h2 class="text-lg font-extrabold text-white">
                Similar cars you might like
            </h2>

            <NuxtLink
                to="/client/fleet"
                class="flex shrink-0 items-center gap-1 text-xs font-semibold text-[#C1121F] hover:underline"
            >
                View all
                <svg class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
            </NuxtLink>
        </div>

        <div
            v-if="loading"
            class="flex min-h-32 items-center justify-center text-xs text-gray-500"
        >
            Loading similar cars...
        </div>

        <div
            v-else-if="error"
            class="flex min-h-32 items-center justify-center text-center text-xs text-red-400"
        >
            {{ error }}
        </div>

        <div
            v-else-if="similarCars.length"
            class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3"
        >
            <NuxtLink
                v-for="similarCar in similarCars"
                :key="similarCar.car_reference"
                :to="`/client/car-details/${similarCar.car_reference}`"
                class="group flex flex-col overflow-hidden rounded-xl border border-transparent transition-colors duration-200 hover:border-[#C1121F]"
            >
                <div class="h-28 overflow-hidden bg-[#121212]">
                    <img
                        v-if="similarCar.meta.primary_image"
                        :src="similarCar.meta.primary_image"
                        :alt="`${similarCar.brand} ${similarCar.model}`"
                        class="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
                    />

                    <div
                        v-else
                        class="flex h-full items-center justify-center text-xs text-gray-600"
                    >
                        No image available
                    </div>
                </div>

                <div class="flex flex-1 flex-col gap-1 bg-[#1a1a1a] px-4 py-3">
                    <p class="text-sm font-bold text-white">
                        {{ similarCar.brand }} {{ similarCar.model }}
                    </p>
                    <p class="text-xs text-gray-500">
                        {{ similarCar.car_type }} · {{ similarCar.seats }} seats
                    </p>
                    <p class="mt-1 text-xs font-semibold text-gray-300">
                        ₱{{ Number(similarCar.price_per_day).toLocaleString() }}/day
                    </p>
                </div>
            </NuxtLink>
        </div>

        <div
            v-else
            class="flex min-h-32 items-center justify-center text-center text-xs text-gray-500"
        >
            No similar cars are available right now.
        </div>
    </div>
</template>

<script setup lang="ts">
const props = defineProps<{
    carReference: string
}>()

const {
    similarCars,
    loading,
    error,
    fetchSimilarCars,
} = useSimilarCars()

watch(
    () => props.carReference,
    carReference => fetchSimilarCars(carReference),
    { immediate: true }
)
</script>
