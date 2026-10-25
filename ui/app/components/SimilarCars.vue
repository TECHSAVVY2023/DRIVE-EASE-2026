<template>
    <div class="smoked-charcoal-panel font-[poppins] py-6 px-6 w-full rounded-lg">

        <!-- Header -->
        <div class="flex items-center justify-between mb-4">
            <h2 class="text-white font-extrabold text-lg">Similar cars you might like</h2>
            <NuxtLink to="/client/fleet" class="text-[#C1121F] text-xs font-semibold hover:underline flex items-center gap-1">
                View all
                <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                </svg>
            </NuxtLink>
        </div>

        <!-- Cars Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
            <a
                v-for="car in cars.slice(0, 3)"
                :key="car.id"
                :href="`/car-details/${car.id}`"
                class="
                    group flex flex-col
                    rounded-xl overflow-hidden border border-transparent hover:border-[#C1121F]
                    transition-colors duration-200 cursor-pointer
                "
            >
                <!-- Image -->
                <div class="h-20 bg-[##121212] overflow-hidden">
                    <img
                        :src="car.image"
                        :alt="car.name"
                        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                </div>

                <!-- Info -->
                <div class="px-4 py-3 bg-[#1a1a1a] flex flex-col gap-1">
                    <p class="text-white text-sm font-bold">{{ car.name }}</p>
                    <p class="text-gray-400 text-xs">₱{{ car.price }}/day</p>
                </div>
            </a>
        </div>

    </div>
</template>
