<template>
    <section class="relative overflow-hidden bg-[#111111] font-[poppins]">
        <div
            class="
                relative z-10
                flex flex-col
                px-8 pt-16 pb-32

                sm:gap-16
                md:flex-row md:gap-8 md:pb-16
                lg:gap-32
            "
        >
            <!-- =========================
                 Left Content
            ========================== -->
            <div
                class="
                    flex flex-col justify-center gap-4
                    items-center text-center
                    w-full

                    sm:pl-4

                    md:w-2/5 md:items-start 
                    md:text-left md:pl-8

                    lg:pl-16
                "
            >
                <!-- Heading -->
                <h2
                    class="
                        text-2xl md:text-3xl
                        font-extrabold
                        leading-tight tracking-wide
                        uppercase text-white
                    "
                >
                    Got Questions?<br />
                    <span class="text-[#C1121F]">We've Got Answers</span>
                </h2>

                <p class="text-[#9E9E9E] text-sm leading-relaxed">
                    Every question that is frequently asked by customers about Driveease
                </p>
                
                <button class="
                    mt-4 mb-8
                    bg-[#C1121F] hover:bg-red-700
                    text-white text-sm font-semibold
                    px-6 py-3 rounded
                    transition-colors duration-200
                ">
                    Ask more questions
                </button>
            </div>

            <!-- =========================
                 Right contents: FAQ Accordion
            ========================== -->
            <div class="flex flex-col w-full gap-4 md:w-3/5">

                <div
                    v-for="(faq, index) in faqs"
                    :key="index"
                    class="flex flex-col gap-3 p-5 rounded-md bg-[#1a1a1a]"
                >
                    <!-- Card -->
                    <div class="bg-[#1a1a1a] rounded-xl">

                        <button
                            @click="toggle(index)"
                            class="w-full flex items-center justify-between px-8 py-4 text-left gap-4"
                        >
                            <div class="flex items-center gap-4 ">
                                <span
                                    class="
                                        w-12 h-12 rounded-md flex-shrink-0
                                        flex items-center justify-center

                                        text-white text-xl font-medium
                                        transition-colors duration-200
                                    "
                                    :class="openIndex === index ? 'bg-[#C1121F]' : 'bg-[#2a2a2a]'"
                                >
                                    {{ index + 1 }}
                                </span>

                                <span class="text-white font-medium text-sm md:text-base">
                                    {{ faq.question }}
                                </span>
                            </div>

                            <!-- +/- icon -->
                            <span 
                                class="
                                    text-white text-2xl leading-none 
                                    transition-transform duration-300 flex-shrink-0
                                "
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
                            <p class="px-5 pb-5 text-[#9E9E9E] text-sm leading-relaxed">
                                {{ faq.answer }}
                            </p>
                        </div>

                    </div>    
                </div>

            </div>
        </div>

        <!-- Desktop Accent -->
        <div class="absolute top-0 right-0 hidden md:block w-[35%] h-full bg-[#C1121F]"></div>

        <!-- Mobile Accent -->
        <div class="absolute bottom-0 left-0 right-0 h-[192px] md:hidden bg-[#C1121F]"></div>

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