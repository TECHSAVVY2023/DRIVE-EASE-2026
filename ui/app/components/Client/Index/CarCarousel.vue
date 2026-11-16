<template>
    <div class="mb-10 text-center">
        <h2 class="text-2xl font-extrabold uppercase tracking-wide text-white md:text-3xl">
            {{ content.fleet_heading }}
        </h2>

        <p class="mt-2 text-sm text-[#9E9E9E]">
            {{ content.fleet_description }}
        </p>
    </div>

    <div
        ref="sectionRef"
        class="relative mx-auto flex max-w-4xl items-center justify-center"
    >
        <button
            type="button"
            aria-label="Previous featured car"
            :disabled="cars.length <= 1"
            class="absolute left-0 z-10 flex h-10 w-10 items-center justify-center rounded-full border border-white/10 bg-[#0b0b0d]/90 text-white shadow-lg transition-colors duration-200 hover:border-[#C1121F] hover:bg-[#C1121F] disabled:cursor-not-allowed disabled:opacity-40"
            @click="prev"
        >
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
        </button>

        <div class="flex w-full flex-col items-center px-16 text-center">
            <Transition
                enter-active-class="transition-all duration-300 ease-in-out"
                leave-active-class="transition-all duration-300 ease-in-out"
                :enter-from-class="transitionEnterFrom"
                :leave-to-class="transitionLeaveTo"
                mode="out-in"
            >
                <div
                    v-if="currentCar"
                    :key="currentCar.id"
                    class="flex flex-col items-center"
                >
                    <img
                        v-if="currentCar.featured_image"
                        :src="currentCar.featured_image"
                        :alt="currentCar.car_name"
                        class="h-[260px] w-full max-w-sm object-contain drop-shadow-2xl md:h-[320px] md:max-w-md"
                    >

                    <div
                        v-else
                        class="flex h-[260px] w-full max-w-sm items-center justify-center text-sm text-[#777] md:h-[320px] md:max-w-md"
                    >
                        Image unavailable
                    </div>

                    <h3 class="mt-6 text-xl font-extrabold uppercase tracking-wide text-white">
                        {{ currentCar.car_name }}
                    </h3>

                    <p class="mt-1 text-sm text-[#9E9E9E]">
                        from
                        <span class="font-semibold text-white">
                            {{ formatPrice(currentCar.price_per_day) }}
                        </span>/day
                    </p>
                </div>

                <p v-else key="empty" class="py-24 text-sm text-[#9E9E9E]">
                    No featured vehicles are available yet.
                </p>
            </Transition>

            <button
                type="button"
                class="mt-6 rounded bg-[#C1121F] px-8 py-3 text-sm font-semibold text-white transition-colors duration-200 hover:bg-[#9B0E18]"
                @click="router.push('/client/fleet')"
            >
                View all cars
            </button>
        </div>

        <button
            type="button"
            aria-label="Next featured car"
            :disabled="cars.length <= 1"
            class="absolute right-0 z-10 flex h-10 w-10 items-center justify-center rounded-full border border-white/10 bg-[#0b0b0d]/90 text-white shadow-lg transition-colors duration-200 hover:border-[#C1121F] hover:bg-[#C1121F] disabled:cursor-not-allowed disabled:opacity-40"
            @click="next"
        >
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
        </button>
    </div>

    <div v-if="cars.length > 1" class="mt-8 flex justify-center gap-2">
        <button
            v-for="(car, index) in cars"
            :key="car.id"
            type="button"
            :aria-label="`Show ${car.car_name}`"
            :aria-current="index === current ? 'true' : undefined"
            class="h-2 w-2 rounded-full transition-colors duration-200"
            :class="index === current ? 'bg-[#C1121F]' : 'bg-[#3C3C3C]'"
            @click="goTo(index)"
        />
    </div>
</template>

<script setup lang="ts">
import type { HomePageFeaturedCar, HomepageContent } from '~/utils/types/content'

const props = defineProps<{
    content: HomepageContent
}>()

const router = useRouter()
const cars = computed<HomePageFeaturedCar[]>(() => props.content.featured_cars)
const current = ref<number>(0)
const currentCar = computed<HomePageFeaturedCar | null>(
    () => cars.value[current.value] ?? null
)
const transitionDirection = ref<'left' | 'right'>('left')
const sectionRef = ref<HTMLElement | null>(null)
const isVisible = ref<boolean>(false)

const transitionEnterFrom = computed<string>(() =>
    transitionDirection.value === 'left'
        ? 'opacity-0 translate-x-15'
        : 'opacity-0 -translate-x-15'
)

const transitionLeaveTo = computed<string>(() =>
    transitionDirection.value === 'left'
        ? 'opacity-0 -translate-x-15'
        : 'opacity-0 translate-x-15'
)

const formatPrice = (price: string): string =>
    new Intl.NumberFormat('en-PH', {
        style: 'currency',
        currency: 'PHP',
        minimumFractionDigits: 0,
        maximumFractionDigits: 2,
    }).format(Number(price) || 0)

let autoSlideInterval: ReturnType<typeof setInterval> | null = null
let interactionTimeout: ReturnType<typeof setTimeout> | null = null
let observer: IntersectionObserver | null = null

function next(): void {
    if (cars.value.length <= 1) return

    transitionDirection.value = 'left'
    current.value = (current.value + 1) % cars.value.length
    resetAutoSlideDelay()
}

function prev(): void {
    if (cars.value.length <= 1) return

    transitionDirection.value = 'right'
    current.value = (current.value - 1 + cars.value.length) % cars.value.length
    resetAutoSlideDelay()
}

function goTo(index: number): void {
    if (index < 0 || index >= cars.value.length || index === current.value) return

    transitionDirection.value = index > current.value ? 'left' : 'right'
    current.value = index
    resetAutoSlideDelay()
}

function startAutoSlide(): void {
    if (autoSlideInterval || cars.value.length <= 1) return

    autoSlideInterval = setInterval(() => {
        transitionDirection.value = 'left'
        current.value = (current.value + 1) % cars.value.length
    }, 3000)
}

function stopAutoSlide(): void {
    if (!autoSlideInterval) return

    clearInterval(autoSlideInterval)
    autoSlideInterval = null
}

function resetAutoSlideDelay(): void {
    stopAutoSlide()

    if (interactionTimeout) clearTimeout(interactionTimeout)

    interactionTimeout = setTimeout(() => {
        if (isVisible.value) startAutoSlide()
    }, 5000)
}

watch(
    () => cars.value.length,
    (length) => {
        if (length === 0 || current.value >= length) current.value = 0

        stopAutoSlide()
        if (isVisible.value) startAutoSlide()
    }
)

onMounted(() => {
    observer = new IntersectionObserver(
        ([entry]) => {
            isVisible.value = Boolean(entry?.isIntersecting)

            if (isVisible.value) startAutoSlide()
            else stopAutoSlide()
        },
        { threshold: 0.5 }
    )

    if (sectionRef.value) observer.observe(sectionRef.value)
})

onBeforeUnmount(() => {
    stopAutoSlide()
    if (interactionTimeout) clearTimeout(interactionTimeout)
    observer?.disconnect()
})
</script>
