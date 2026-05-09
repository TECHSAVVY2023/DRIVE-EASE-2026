<template>
    <section class="relative bg-[#111111] overflow-hidden font-[poppins]">

        <!-- Red strip - desktop (right side) / mobile (bottom) -->
        <div class="
        hidden md:block
        absolute top-0 right-0 w-[35%] h-full bg-[#C1121F]
        "></div>
        <div class="
        md:hidden
        absolute bottom-0 left-0 right-0 h-[192px] bg-[#C1121F]
        "></div>

        <div class="flex justify-center">
            <!-- Content -->
            <div class="relative z-10 max-w-8xl px-8 py-16 flex flex-col md:flex-row lg:gap-32 md:gap-8 sm:gap-16">

                <div class="
                    flex flex-col justify-center 
                    sm:items-center sm:pl-4 
                    md:items-start md:pl-8 md:w-2/5
                    lg:pl-16 gap-4 w-full">
                    <h2 class="
                    text-white text-2xl sm:text-center 
                    md:text-start md:text-3xl 
                    font-extrabold uppercase leading-tight tracking-wide">
                        What our customers<br />say about us
                    </h2>

                    <div class="flex items-end gap-2 mt-4">
                    <span class="text-[#C1121F] text-6xl font-extrabold leading-none">4.8</span>
                    <span class="text-gray-400 text-sm mb-2">out of 5</span>
                    </div>

                    <!-- Stars -->
                    <div class="flex gap-1">
                    <span v-for="i in 5" :key="i" class="text-[#C1121F] text-2xl">★</span>
                    </div>

                    <p class="text-gray-400 text-sm">Based on 2,400+ reviews</p>

                    <button class="
                        mt-4
                        w-fit
                        bg-[#C1121F] hover:bg-red-700
                        text-white text-sm font-semibold
                        px-6 py-3 rounded
                        transition-colors duration-200
                    ">
                        View all reviews
                    </button>
                </div>

                <!-- Right: Review Cards -->
                <div class="flex flex-col gap-4 md:w-3/5 w-full">
                    <div
                    v-for="(review, index) in reviews"
                    :key="index"
                    class="bg-[#1a1a1a] rounded-xl p-5 flex flex-col gap-3"
                    >
                    <!-- Reviewer info + stars -->
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-full bg-[#C1121F] flex-shrink-0"></div>
                        <span class="text-white font-semibold text-sm">{{ review.name }}</span>
                        </div>
                        <div class="flex gap-0.5">
                        <span v-for="i in review.stars" :key="i" class="text-[#C1121F] text-base">★</span>
                        </div>
                    </div>

                    <!-- Review text -->
                    <p class="text-gray-400 text-sm leading-relaxed">{{ review.text }}</p>

                    <!-- Divider + Car rented -->
                    <div class="border-t border-[#2a2a2a] pt-2 flex justify-end">
                        <span class="text-gray-500 text-xs italic">{{ review.car }}</span>
                    </div>
                    </div>
                </div>

            </div>

        </div>
    </section>
</template>

<script setup>
const { reviews } = useLandingPage()
</script>