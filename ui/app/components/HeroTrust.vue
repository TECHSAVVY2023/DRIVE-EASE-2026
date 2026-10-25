<template>
    <section ref="sectionRef" class="landing-quiet-section relative font-[poppins] py-16 px-6 md:px-20 overflow-hidden">
            <Transition name="fade-only">
                <div v-if="isVisible" class="max-w-7xl mx-auto">

                    <!-- =========================
                        Trust section
                    ========================== -->
                    <h2 class="text-white text-2xl font-extrabold text-center uppercase mb-10 md:text-3xl">
                        Why Choose Us?
                    </h2>

                    <!-- =========================
                            Trusts cards
                    ========================== -->
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-px overflow-hidden rounded-xl border border-white/[0.07] bg-white/[0.07]">

                        <div
                            v-for="(stat, index) in stats"
                            :key="index"
                            class="
                                flex flex-col items-center 
                                justify-center text-center gap-1 
                                bg-[#19191b] px-6 py-8
                                transition-colors duration-200 hover:bg-[#1d1d20]
                            "
                        >
                            <span class="text-white text-2xl font-extrabold md:text-3xl">{{ stat.value }}</span>
                            <span class="text-[#a0a0a5] text-sm">{{ stat.label }}</span>
                        </div>

                    </div>

                </div>
            </Transition>
    </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'

/* =========================
   Trust data
========================= */
const { stats } = useLandingPage()

const sectionRef = ref(null)
const isVisible = ref(false)

onMounted(() => {
    const observer = new IntersectionObserver(
        ([entry]) => {
            if (entry.isIntersecting) {
                isVisible.value = true
                observer.disconnect()
            }
        },
        {
            threshold: 0.2
        }
    )

    if (sectionRef.value) {
        observer.observe(sectionRef.value)
    }
})
</script>

<style scoped>
.fade-only-enter-active {
    transition: opacity 0.8s ease;
}

.fade-only-enter-from {
    opacity: 0;
}

.fade-only-enter-to {
    opacity: 1;
}
</style>
