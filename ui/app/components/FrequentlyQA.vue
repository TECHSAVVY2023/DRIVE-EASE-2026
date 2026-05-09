<template>
    <section class="relative bg-[#111111] overflow-hidden font-[poppins]">

        <!-- Red strip - desktop (right side) / mobile (bottom) -->
        <div class="hidden md:block absolute top-0 right-0 w-[35%] h-full bg-[#C1121F]"></div>
        <div class="md:hidden absolute bottom-0 left-0 right-0 h-[192px] bg-[#C1121F]"></div>

        <div class="flex justify-center">
        <div class="relative z-10 max-w-6xl w-full px-8 py-16 flex flex-col md:flex-row lg:gap-32 md:gap-8 gap-10">

            <!-- Left: Summary -->
            <div class="
                flex flex-col justify-center gap-4 w-full 
                sm:items-center md:w-2/5 md:flex-shrink-0">
                <h2 class="text-white text-2xl md:text-3xl font-extrabold uppercase leading-tight tracking-wide">
                    Got Questions?<br />
                    <span class="text-[#C1121F]">We've Got Answers</span>
                </h2>
                <p class="text-gray-400 text-sm leading-relaxed">
                    Every question that is frequently asked by customers about Driveease
                </p>
                <button class="
                    mt-4
                    bg-[#C1121F] hover:bg-red-700
                    text-white text-sm font-semibold
                    px-6 py-3 rounded
                    transition-colors duration-200
                ">
                    Ask more questions
                </button>
            </div>

            <!-- Right: FAQ Accordion -->
            <div class="flex flex-col w-full md:w-3/5 min-w-0 gap-4">
            <div
                v-for="(faq, index) in faqs"
                :key="index"
                class="rounded-xl overflow-hidden"
            >
                <!-- Card -->
                <div class="bg-[#1a1a1a] rounded-xl overflow-hidden">
                <!-- Header -->
                <button
                    @click="toggle(index)"
                    class="w-full flex items-center justify-between px-8 py-4 text-left gap-4"
                >
                    <div class="flex items-center gap-4">
                    <!-- Number badge -->
                    <span class="
                            w-8 h-8 flex-shrink-0 rounded-md flex items-center justify-center
                            text-white text-sm font-bold
                            transition-colors duration-200
                        "
                        :class="openIndex === index ? 'bg-[#C1121F]' : 'bg-[#2a2a2a]'"
                        >
                            {{ index + 1 }}
                    </span>
                    <span class="text-white font-semibold text-sm md:text-base">
                        {{ faq.question }}
                    </span>
                    </div>

                    <!-- +/- icon -->
                    <span class="text-white text-2xl leading-none transition-transform duration-300 flex-shrink-0"
                    :class="openIndex === index ? 'rotate-45' : ''"
                    >
                    +
                    </span>
                </button>

                <!-- Answer -->
                <div
                    class="overflow-hidden transition-all duration-300 ease-in-out"
                    :class="openIndex === index ? 'max-h-40 opacity-100' : 'max-h-0 opacity-0'"
                >
                    <p class="px-5 pb-5 text-gray-400 text-sm leading-relaxed">
                    {{ faq.answer }}
                    </p>
                </div>
                </div>

            </div>
            </div>

        </div>
        </div>
    </section>
</template>

<script setup>
import { ref } from 'vue'

const { faqs } = useLandingPage()

const openIndex = ref(null)

function toggle(index) {
  openIndex.value = openIndex.value === index ? null : index
}
</script>