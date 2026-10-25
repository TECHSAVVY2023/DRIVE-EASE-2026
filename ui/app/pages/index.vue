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
    
    <HeroSection />
    <HeroTrust />
    <LandingReviews />
    <Carcarousel />
    <FrequentlyQA />
    <SigninBanner v-if="!isLoggedIn" />
    <Footer />

</template>

<script setup lang="ts">

const { isLoggedIn, authReady } = useAuth()
const { user } = useCurrentUser()

const { 
    menuOpen,
    toggleMenu,
    closeMenu,
    handleCloseSidebar,
    handleOpenSidebar
} = useNavbar()

</script>
