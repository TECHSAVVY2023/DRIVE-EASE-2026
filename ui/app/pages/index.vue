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
    <SigninBanner v-if="!isLoggedIn" />
    <Footer />

</template>

<script setup lang="ts">

const { isLoggedIn } = useAuth()

const { 
    menuOpen,
    toggleMenu,
    closeMenu,
    handleCloseSidebar,
    handleOpenSidebar
} = useNavbar()

</script>