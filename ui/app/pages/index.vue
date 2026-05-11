<template>
    <MobileDrawer
        :menu-open="menuOpen"
        @close-menu="closeMenu"
    />
    <Navbar
        :menu-open="menuOpen"
        @toggle-menu="toggleMenu"
    />
    <HeroSection />
    <HeroTrust />
    <LandingReviews />
    <Carcarousel />
    <FrequentlyQA />
    <SigninBanner />
    <Footer />
</template>

<script setup lang="ts">
import { ref } from 'vue'

const menuOpen = ref(false)

const toggleMenu = () => {
    menuOpen.value = !menuOpen.value
}

const closeMenu = () => {
    menuOpen.value = false
}
</script>