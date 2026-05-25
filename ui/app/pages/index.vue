<template>
    <MobileDrawer
        :menu-open="menuOpen"
        @close-menu="closeMenu"
    />
    <Navbar
        :menu-open="menuOpen"
        @toggle-menu="toggleMenu"
        @open-sidebar="handleOpenSidebar" 
        @close-sidebar="handleCloseSidebar"
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

//Navbar + User Profile + Working login

const { setAuth } = useAuth()
const route = useRoute()

const sidebarOpen = ref<boolean>(false)

const menuOpen = ref(false)

const toggleMenu = () => {
    menuOpen.value = !menuOpen.value
}

const closeMenu = () => {
    menuOpen.value = false
}

const handleCloseSidebar = (): void => {
    sidebarOpen.value = false
}

const handleOpenSidebar = (): void => {
    sidebarOpen.value = true
}

if (route.query.token) {
    await setAuth(route.query.token as string)
}
</script>