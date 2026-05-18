<template>
    <section 
    ref="sectionRef"
    class="relative overflow-hidden bg-[#111111] font-[poppins]">

        <!-- =========================
             Reviews Section
        ========================== -->
        <div 
            class="
                relative z-10
                flex flex-col
                px-8 py-16

                sm:gap-16
                md:flex-row md:gap-8
                lg:gap-32
            "
        >

                <!-- =========================
                    Left Content
                ========================== -->
                <Transition name="fade-left">

                    <div
                        v-if="isVisible" 
                        class="
                            flex flex-col justify-center
                            w-full gap-4 items-center text-center

                            sm:pl-4

                            md:w-2/5
                            md:items-start md:text-left
                            md:pl-8

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
                            What our customers<br />
                            say about us
                        </h2>

                        <!-- Rating -->
                        <div class="flex items-end gap-2 mt-4">

                            <span class="text-6xl font-extrabold leading-none text-[#C1121F]">
                                4.8
                            </span>

                            <span class="text-sm text-[#9E9E9E] mb-2">
                                out of 5
                            </span>
                        </div>

                        <!-- Stars -->
                        <div class="flex gap-1">
                            <span
                                v-for="i in 5"
                                :key="i"
                                class="text-3xl text-[#C1121F]"
                            >
                                ★
                            </span>
                        </div>

                        <p class="text-sm text-[#9E9E9E]">
                            Based on 2,400+ reviews
                        </p>

                        <!-- CTA -->
                        <button
                            class="
                                w-fit rounded bg-[#C1121F]
                                px-8 py-4 mt-4 mb-8
                                text-sm font-semibold text-white

                                hover:bg-[#6B0A10]
                                transition-colors duration-200
                            "
                        >
                            View all reviews
                        </button>
                    </div>

                </Transition>

                <!-- =========================
                    Review Cards
                ========================== -->
                <Transition name="fade-right">

                    <div 
                        v-if="isVisible"
                        class="flex flex-col w-full gap-4 md:w-3/5">

                        <div
                            v-for="(review, index) in reviews"
                            :key="index"
                            class="flex flex-col gap-3 p-5 rounded-xl bg-[#1a1a1a]"
                        >

                            <!-- Reviewer Info -->
                            <div class="flex items-center justify-between">

                                <div class="flex items-center gap-3">

                                    <div class="w-10 h-10 rounded-full flex-shrink-0 bg-[#C1121F]"></div>

                                    <span class="text-sm font-semibold text-white">
                                        {{ review.name }}
                                    </span>
                                </div>

                                <!-- Review Stars -->
                                <div class="flex gap-0.5">
                                    <span
                                        v-for="i in review.stars"
                                        :key="i"
                                        class="text-base text-[#C1121F]"
                                    >
                                        ★
                                    </span>
                                </div>
                            </div>

                            <!-- Review Text -->
                            <p class="text-sm leading-relaxed text-[#9E9E9E]">
                                {{ review.text }}
                            </p>

                            <!-- Car Info -->
                            <div class="flex justify-end pt-2 border-t border-[#2a2a2a]">

                                <span class="text-xs italic text-[#797979]">
                                    {{ review.car }}
                                </span>

                            </div>
                            
                        </div>
                    </div>

                </Transition>

            </div>



        <!-- Desktop Accent -->
        <div class="absolute top-0 right-0 hidden md:block w-[35%] h-full bg-[#C1121F]"></div>

        <!-- Mobile Accent -->
        <div class="absolute bottom-0 left-0 right-0 h-[192px] md:hidden bg-[#C1121F]"></div>

    </section>

</template>

<script setup>
/* =========================
   Reviews Data
========================= */
const { reviews } = useLandingPage()

const sectionRef = ref(null)
const isVisible = ref(false)

onMounted(() => {
    const observer = new IntersectionObserver(([entry]) => {
        if (entry.isIntersecting) {
            isVisible.value = true
            observer.disconnect()
        }
    }, { threshold: 0.2 })

    if (sectionRef.value) observer.observe(sectionRef.value)
})
</script>

<style scoped>

.fade-left-enter-active {
    transition: all 0.8s ease-out;
}

.fade-left-enter-from {
    opacity: 0;
    transform: translateX(-60px);
}

.fade-left-enter-to {
    opacity: 1;
    transform: translateX(0);
}

.fade-right-enter-active {
    transition: all 0.8s ease-out;
}

.fade-right-enter-from {
    opacity: 0;
    transform: translateX(60px);
}

.fade-right-enter-to {
    opacity: 1;
    transform: translateX(0);
}

</style>
