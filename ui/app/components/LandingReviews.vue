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
                            @click="$router.push('/reviews')"
                            class="
                                w-fit rounded
                                px-8 py-4 mt-4 mb-8
                                text-sm font-semibold text-white

                                bg-[#C1121F] hover:bg-[#9B0E18] 
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
                        class="flex flex-col w-full gap-4 md:w-3/5"
                    >
                        <div
                            v-for="(review, index) in LandingVisibleReviews"
                            :key="index"
                            class="flex flex-col gap-3 p-5 rounded-xl bg-[#1a1a1a]"
                        >
                            
                            <!-- Reviewer Info -->
                            <div class="flex items-start justify-between">

                                <div class="flex items-center gap-3">

                                    <div class="w-10 h-10 rounded-full bg-[#C1121F] flex-shrink-0 overflow-hidden flex items-center justify-center">
                                        <img
                                            v-if="review.avatar"
                                            :src="review.avatar"
                                            :alt="review.name"
                                            class="w-full h-full object-cover"
                                        />

                                        <span v-else class="text-white text-sm font-bold">
                                            {{ review.name.charAt(0) }}
                                        </span>
                                    </div>

                                    <div>
                                        <p class="text-white text-sm font-semibold"> {{ review.name }} </p>
                                        <p class="text-[#929292] text-xs"> {{ review.date }} </p>
                                    </div>

                                </div>

                                <!-- Stars -->
                                <div class="flex gap-0.5 flex-shrink-0">
                                    
                                    <svg
                                        v-for="s in 5"
                                        :key="s"
                                        class="w-4 h-4"
                                        :class="s <= review.rating ? 'text-[#C1121F]' : 'text-[#333]'"
                                        fill="currentColor"
                                        viewBox="0 0 24 24"
                                    >
                                        <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                                    </svg>

                                </div>
                            </div>

                            <!-- Review text -->
                            <p class="text-white text-sm leading-relaxed"> {{ review.text }} </p>

                            <div
                                v-if="review.images && review.images.length"
                                class="flex gap-2 flex-wrap"
                            >
                                <div
                                    v-for="(img, j) in review.images"
                                    :key="j"
                                    class="w-16 h-12 rounded-lg bg-[#111] border border-[#2a2a2a] overflow-hidden flex-shrink-0"
                                >
                                    <img
                                        :src="img"
                                        :alt="'Review image ' + (Number(j) + 1)"
                                        class="w-full h-full object-cover"
                                    />
                                </div>
                            </div>

                            <!-- Helpful -->
                            <div class="flex justify-end">

                                <button
                                    @click="review.helpfulClicked = !review.helpfulClicked"
                                    class="flex items-center gap-1.5 text-xs transition-colors duration-200"
                                    :class="
                                    review.helpfulClicked
                                        ? 'text-[#C1121F]'
                                        : 'text-gray-400 hover:text-[#C1121F]'
                                    "
                                >

                                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        stroke-width="2"
                                        d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5"
                                    />
                                    </svg>

                                    Helpful ({{ review.helpfulCount }})

                                </button>

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
const { reviews, LandingVisibleReviews } = useReviews()

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
