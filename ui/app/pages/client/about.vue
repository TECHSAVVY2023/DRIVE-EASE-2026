<template>

   <MobileDrawer
      :menu-open="menuOpen"
      @close-menu="closeMenu"
   />

   <Navbar
      :user="user"
      :auth-ready="authReady"
      :is-logged-in="isLoggedIn"
      :menu-open="menuOpen"
      @toggle-menu="toggleMenu"
      @open-sidebar="handleOpenSidebar" 
      @close-sidebar="handleCloseSidebar"
   />

   <Banner 
      subtitle="About Us"
      title="About Drive Ease"
      :breadcrumbs="[
         { label: 'Home', to: '/' },
         { label: 'About' }
      ]"
   />

   <div class="charcoal-blueprint-surface min-h-screen font-[poppins]">

      <div class="max-w-5xl mx-auto px-6 py-10 flex flex-col gap-5">

         <ClientAboutUsWhoWeAre 
            v-if="about"
            :about="about"
         />

         <ClientAboutUsMissionVision 
            v-if="about"
            :about="about"
         />

         <ClientAboutUsTeam
            v-if="about"
            :about="about"
         />

         <ClientAboutUsJourney
            v-if="about"
            :about="about"
         />

      </div>
   </div>

   <Footer />
   
</template>

<script setup lang="ts">

//Navbar + User Profile + Working login
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
   loadAboutUsPageContent,
   about
} = useAboutUsPageContentLoad()

onMounted(() => {
    loadAboutUsPageContent()
})

</script>
