<template>
    <section class="relative bg-[#1A1A1A] font-[poppins] py-16 px-20 overflow-hidden">

            <!-- Title -->
            <h2 class="text-white text-2xl md:text-3xl font-extrabold text-center uppercase tracking-wide mb-10">
                Why Choose Us?
            </h2>

            <!-- Stats Grid -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div
                v-for="(stat, index) in stats"
                :key="index"
                class="bg-[#222222] rounded-xl px-8 py-8 flex flex-col items-center justify-center text-center gap-1"
                >
                    <span class="text-white text-2xl md:text-3xl font-extrabold">{{ stat.value }}</span>
                    <span class="text-white text-sm">{{ stat.label }}</span>
                </div>
            </div>

    </section>
</template>

<script setup>
    const { stats } = useLandingPage()
</script>