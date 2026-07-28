<template>

   <MobileDrawer
      :menu-open="menuOpen"
      @close-menu="closeMenu"
   />

   <Navbar
      :user="user"
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

   <div class="min-h-screen bg-[#121212] font-[poppins]">

      <div class="max-w-5xl mx-auto px-6 py-10 flex flex-col gap-5">

         <!-- Who We Are -->
         <section class="grid grid-cols-1 md:grid-cols-2 gap-4 items-center">

            <div class="flex flex-col h-full justify-center gap-4 bg-[#1B1B1B] p-6 rounded-xl">
               <h2 class="text-white font-extrabold text-xl">Who we are</h2>
               <p class="text-[#929292] text-sm leading-relaxed">
                  Drive Ease is a trusted car rental service based in Cagayan De Oro City, Philippines.
                  We provide affordable, reliable, and well-maintained vehicles for individuals and businesses
                  across the region. Whether you need a compact city car or a spacious family vehicle,
                  we have the right car for every trip.
               </p>

               <!-- Stats -->
               <div class="flex gap-6 mt-2">
                  <div v-for="stat in stats" :key="stat.label" class="flex flex-col">
                  <span class="text-white font-extrabold text-2xl">{{ stat.value }}</span>
                  <span class="text-[#929292] text-xs mt-0.5">{{ stat.label }}</span>
                  </div>
               </div>

            </div>

            <!-- Image placeholder -->
            <div class="bg-[#1a1a1a] border border-[#2a2a2a] rounded-xl overflow-hidden h-full flex items-center justify-center">
               <img
                  src="~/assets/images/login-bg.png"
                  alt="About Drive Ease"
                  class="w-full h-full object-cover"
                  @error="(e) => (e.target as HTMLImageElement).style.display = 'none'"
               />
            </div>

         </section>

         <!-- Mission + Vision -->
         <section class="grid grid-cols-1 md:grid-cols-2 gap-4">

            <div class="bg-[#1B1B1B] rounded-xl p-6 flex flex-col gap-3">

               <div class="flex items-center gap-3">

                  <!-- Icon goes here -->
                  <div class="w-8 h-8 bg-[#C1121F] rounded-md flex items-center justify-center flex-shrink-0">
                     <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="w-4 h-4 text-white"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                     >
                        <path
                           stroke-linecap="round"
                           stroke-linejoin="round"
                           stroke-width="2"
                           d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                        />
                     </svg>
                  </div>

                  <h3 class="text-white font-bold text-base">Our mission</h3>
                  
               </div>
               
               <p class="text-[#929292] text-sm leading-relaxed">
                  To provide every customer with a seamless, affordable, and comfortable car rental
                  experience — making transportation accessible for everyone, wherever the road takes them.
               </p>

            </div>

            <div class="bg-[#1B1B1B] rounded-xl p-6 flex flex-col gap-3">

               <div class="flex items-center gap-3">

                  <!-- Icon goes here -->
                  <div class="w-8 h-8 bg-[#C1121F] rounded-md flex items-center justify-center flex-shrink-0">
                     <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="w-4 h-4 text-white"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                     >
                        <path
                           stroke-linecap="round"
                           stroke-linejoin="round"
                           stroke-width="2"
                           d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                        />
                        <path
                           stroke-linecap="round"
                           stroke-linejoin="round"
                           stroke-width="2"
                           d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                        />
                     </svg>
                  </div>
                  <h3 class="text-white font-bold text-base">Our vision</h3>

               </div>

               <p class="text-[#929292] text-sm leading-relaxed">
                  To become the leading car rental brand in Mindanao, recognized for our commitment
                  to quality, safety, and customer satisfaction across 15+ locations nationwide.
               </p>

            </div>

         </section>

         <!-- Our Team -->
         <section class="flex flex-col gap-5 bg-[#1B1B1B] rounded-xl px-6 pt-6 pb-10">
            
            <h2 class="text-white font-extrabold text-xl">Our team</h2>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">

               <div
                  v-for="member in team"
                  :key="member.name"
                  class="rounded-xl p-4 flex flex-col items-center gap-3 border border-[#C1121F] transition-colors duration-200"
               >

               <div class="w-16 h-16 rounded-full bg-[#C1121F] overflow-hidden flex-shrink-0 flex items-center justify-center">
                  
                  <!-- Image -->
                  <img
                     v-if="member.image"
                     :src="member.image"
                     :alt="member.name"
                     class="w-full h-full object-cover"
                  />

                  <!-- Default User Icon -->
                  <svg
                     v-else
                     xmlns="http://www.w3.org/2000/svg"
                     class="w-8 h-8 text-white"
                     fill="currentColor"
                     viewBox="0 0 640 640"
                  >
                     <path
                           d="M320 312C386.3 312 440 258.3 440 192C440 125.7 386.3 72 320 72C253.7 72 200 125.7 200 192C200 258.3 253.7 312 320 312zM290.3 368C191.8 368 112 447.8 112 546.3C112 562.7 125.3 576 141.7 576L498.3 576C514.7 576 528 562.7 528 546.3C528 447.8 448.2 368 349.7 368L290.3 368z"
                     />
                  </svg>

               </div>

                  <div class="text-center">
                     <p class="text-white text-sm font-semibold">{{ member.name }}</p>
                     <p class="text-[#c1121f] text-xs mt-0.5">{{ member.role }}</p>
                  </div>

                  <div class="w-full flex flex-col gap-1.5">
                     <p class="text-[#929292] text-xs">{{ member.description }}</p>
                  </div>

               </div>

            </div>

         </section>

         <!-- Our Journey -->
         <section class="flex flex-col gap-5 bg-[#1B1B1B] rounded-xl px-6 pt-6 pb-10">

            <h2 class="text-white font-extrabold text-xl">Our journey</h2>

            <div class="flex flex-col gap-3">
               <div
                  v-for="(milestone, i) in journey"
                  :key="milestone.year + i"
                  class="flex items-center gap-4 bg-[#1a1a1a] border border-[#222] rounded-xl px-6 py-5"
               >
                  <!-- Year -->
                  <span class="text-white font-extrabold text-xl w-14 flex-shrink-0">{{ milestone.year }}</span>

                  <!-- Dot -->
                  <div class="w-3 h-3 rounded-full bg-[#C1121F] flex-shrink-0 ring-4 ring-[#C1121F]/20"></div>

                  <!-- Content -->
                  <div class="flex flex-col gap-1 flex-1 min-w-0">
                  <p class="text-white font-bold text-sm">{{ milestone.title }}</p>
                  <p class="text-[#929292] text-xs leading-relaxed">{{ milestone.description }}</p>
                  </div>
               </div>
            </div>

         </section>

      </div>
   </div>

   <Footer />
   
</template>

<script setup lang="ts">

//Navbar + User Profile + Working login
const { isLoggedIn } = useAuth()
const { apiFetch } = useApiFetch()

const user = ref<any>(null)

watch(isLoggedIn, async (val) => {
    if (val) {
        user.value = await apiFetch('/auth/me/')
    } else {
        user.value = null
    }
}, { immediate: true })

const { 
    menuOpen,
    toggleMenu,
    closeMenu,
    handleCloseSidebar,
    handleOpenSidebar
} = useNavbar()

const {  
         stats,
         team,
         journey,
      } = useAboutPage();

</script>