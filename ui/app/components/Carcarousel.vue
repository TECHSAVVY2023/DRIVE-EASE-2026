<template>
    <section 
        ref="sectionRef"
        class="bg-[#1A1A1A] py-16 px-6 overflow-hidden font-[poppins]">

        <!-- Title -->
        <div class="text-center mb-10">

            <h2 class="text-white text-2xl md:text-3xl font-extrabold uppercase tracking-wide">
                Find the Right Car for Your Trip
            </h2>

            <p class="text-[#9E9E9E] text-sm mt-2">From budget-friendly to premium — we have it all</p>
        </div>

        <!-- Carousel -->
        <div class="relative flex items-center justify-center max-w-4xl mx-auto">

            <!-- Prev Button -->
            <button
                @click="prev"
                class="
                absolute left-0 z-10
                w-10 h-10 rounded-full
                bg-[#121212] hover:bg-[#C1121F]
                text-white flex items-center justify-center
                transition-colors duration-200
                shadow-lg
                "
            >
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
            </button>

        <!-- Car Display -->
        <div class="flex flex-col items-center text-center px-16 w-full">
            <Transition
                enter-active-class="transition-all duration-300 ease-in-out"
                leave-active-class="transition-all duration-300 ease-in-out"
                :enter-from-class="transitionEnterFrom"
                :leave-to-class="transitionLeaveTo"
                mode="out-in"
            >
            <div :key="current" class="flex flex-col items-center">
                <!-- Car Image -->
                <img
                :src="cars[current].image"
                :alt="cars[current].name"
                class="w-full max-w-sm md:max-w-md object-contain drop-shadow-2xl"
                />

                <!-- Car Info -->
                <h3 class="text-white text-xl font-extrabold uppercase tracking-wide mt-6">
                {{ cars[current].name }}
                </h3>
                <p class="text-[#9E9E9E] text-sm mt-1">
                from <span class="text-white font-semibold">{{ cars[current].price }}</span>/day
                </p>
            </div>
            </Transition>
            <!-- CTA -->
            <button class="
                mt-6 bg-[#C1121F] hover:bg-red-700
                text-white text-sm font-semibold
                px-8 py-3 rounded
                transition-colors duration-200
                ">
                View all cars
            </button>
        </div>

        <!-- Next Button -->
        <button
            @click="next"
            class="
            absolute right-0 z-10
            w-10 h-10 rounded-full
            bg-[#121212] hover:bg-[#C1121F]
            text-white flex items-center justify-center
            transition-colors duration-200
            shadow-lg
            "
        >
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
        </button>
        </div>

        <!-- Dots -->
        <div class="flex justify-center gap-2 mt-8">
        <button
            v-for="(car, index) in cars"
            :key="index"
            @click="goTo(index)"
            class="w-2 h-2 rounded-full transition-colors duration-200"
            :class="index === current ? 'bg-[#C1121F]' : 'bg-[#3C3C3C]'"
        ></button>
        </div>

    </section>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

const { cars } = useLandingPage()

const current = ref(0)
const transitionName = ref('slide-left')

// Computed transition classes
const transitionEnterFrom = computed(() => 
    transitionName.value === 'slide-left' 
        ? 'opacity-0 translate-x-15' 
        : 'opacity-0 -translate-x-15'
)

const transitionLeaveTo = computed(() => 
    transitionName.value === 'slide-left' 
        ? 'opacity-0 -translate-x-15' 
        : 'opacity-0 translate-x-15'
)

const sectionRef = ref(null)

let autoSlideInterval = null
let interactionTimeout = null
let observer = null

function next() {
    transitionName.value = 'slide-left'
    current.value = (current.value + 1) % cars.length

    resetAutoSlideDelay()
}

function prev() {
    transitionName.value = 'slide-right'
    current.value = (current.value - 1 + cars.length) % cars.length

    resetAutoSlideDelay()
}

function goTo(index) {
    transitionName.value =
        index > current.value ? 'slide-left' : 'slide-right'

    current.value = index

    resetAutoSlideDelay()
}

function startAutoSlide() {
    if (autoSlideInterval) return

    autoSlideInterval = setInterval(() => {
        transitionName.value = 'slide-left'
        current.value = (current.value + 1) % cars.length
    }, 3000)
}

function stopAutoSlide() {
    clearInterval(autoSlideInterval)
    autoSlideInterval = null
}

function resetAutoSlideDelay() {
    stopAutoSlide()

    clearTimeout(interactionTimeout)

    interactionTimeout = setTimeout(() => {
        startAutoSlide()
    }, 5000)
}

onMounted(() => {
    observer = new IntersectionObserver(
        ([entry]) => {
            if (entry.isIntersecting) {
                startAutoSlide()
            } else {
                stopAutoSlide()
            }
        },
        {
            threshold: 0.5
        }
    )

    if (sectionRef.value) {
        observer.observe(sectionRef.value)
    }
})

onBeforeUnmount(() => {
    stopAutoSlide()

    clearTimeout(interactionTimeout)

    if (observer && sectionRef.value) {
        observer.unobserve(sectionRef.value)
    }
})
</script>

