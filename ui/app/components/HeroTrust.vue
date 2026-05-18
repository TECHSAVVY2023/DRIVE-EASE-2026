<template>
    <section ref="sectionRef" class="relative bg-[#1A1A1A] font-[poppins] py-16 px-20 overflow-hidden">
            <Transition name="fade-only">
                <div v-if="isVisible">

                    <!-- =========================
                        Trust section
                    ========================== -->
                    <h2 class="text-white text-2xl font-extrabold text-center uppercase mb-10 md:text-3xl">
                        Why Choose Us?
                    </h2>

                    <!-- =========================
                            Trusts cards
                    ========================== -->
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">

                        <div
                            v-for="(stat, index) in stats"
                            :key="index"
                            class="
                                flex flex-col items-center 
                                justify-center text-center gap-1 
                                bg-[#222222] rounded-xl px-8 py-8
                            "
                        >
                            <span class="text-white text-2xl font-extrabold md:text-3xl">{{ stat.value }}</span>
                            <span class="text-white text-sm">{{ stat.label }}</span>
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
