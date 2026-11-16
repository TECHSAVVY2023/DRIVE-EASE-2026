<template>
    <MobileDrawer
        :menu-open="menuOpen"
        @close-menu="closeMenu"
    />

    <Navbar
        :user="user"
        :is-logged-in="isLoggedIn"
        :auth-ready="authReady"
        :menu-open="menuOpen"
        @toggle-menu="toggleMenu"
        @open-sidebar="handleOpenSidebar" 
        @close-sidebar="handleCloseSidebar"
    />

    <div class="hero-shell font-sans">
        <section class="hero-backdrop relative flex items-center min-h-[700px] overflow-hidden">
            
            <ClientIndexHeroSection
                v-if="content"
                :content="content" 
            />

        </section>
    </div>

    <section ref="trustSectionRef" class="landing-quiet-section relative font-[poppins] py-16 px-6 md:px-20 overflow-hidden">
        <Transition name="fade-only">
            <div v-if="isTrustVisible" class="max-w-7xl mx-auto">

                <ClientIndexHeroTrust 
                    v-if="content"
                    :content="content" 
                />

            </div>
        </Transition>
    </section>

    <ClientIndexLandingReviews />
    
    <section 
        ref="carouselSectionRef"
        class="landing-quiet-section py-16 px-6 overflow-hidden font-[poppins]">

        <Transition name="fade-only">
            <div
                v-if="isCarouselVisible"
                class="max-w-5xl mx-auto"
            >    
                <ClientIndexCarCarousel 
                    v-if="content"
                    :content="content"
                />
                
            </div>
        </Transition>
    </section>

    <ClientIndexFrequentlyAQ
        v-if="content"
        :content="content"
    />

    
    <ClientIndexSigninBanner v-if="authReady && !isLoggedIn" />
    
    <Footer />

</template>

<script setup lang="ts">
import type { Ref } from 'vue'

const { isLoggedIn, authReady } = useAuth()
const { user } = useCurrentUser()

const { 
    menuOpen,
    toggleMenu,
    closeMenu,
    handleCloseSidebar,
    handleOpenSidebar
} = useNavbar()

const {
    home: content,
    loadHomepageContent
} = useHomepageContentLoader()

onMounted(() => {
    loadHomepageContent()
})

const trustSectionRef = ref<HTMLElement | null>(null)
const carouselSectionRef = ref<HTMLElement | null>(null)
const isTrustVisible = ref(false)
const isCarouselVisible = ref(false)
const visibilityObservers: IntersectionObserver[] = []

function revealWhenVisible(
    element: HTMLElement | null,
    visible: Ref<boolean>,
): void {
    if (!element) return

    const observer = new IntersectionObserver(
        ([entry]) => {
            if (!entry?.isIntersecting) return

            visible.value = true
            observer.disconnect()
        },
        { threshold: 0.2 }
    )

    visibilityObservers.push(observer)
    observer.observe(element)
}

onMounted(() => {
    revealWhenVisible(trustSectionRef.value, isTrustVisible)
    revealWhenVisible(carouselSectionRef.value, isCarouselVisible)
})

onBeforeUnmount(() => {
    visibilityObservers.forEach(observer => observer.disconnect())
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
