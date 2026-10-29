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

    <ClientProfileEditModal
        :user="user"
        v-model="showEditProfileModal"
        @updated="fetchUser"
    />

  <div class="charcoal-blueprint-surface min-h-screen font-[poppins]">
    
    <Banner 
        subtitle="Manage account"
        title="My Profile"
        :breadcrumbs="[
            { label: 'Home', to: '/' },
            { label: 'Profile' }
        ]"
    />

        <AuthLoading
            v-if="authLoading"
            message="Loading your profile..."
        />

        <div v-else class="max-w-lg mx-auto px-4 py-8 flex flex-col gap-4">

            <!-- Profile Card -->
            <ClientProfileCard 
                :user="user" 
                @edit="showEditProfileModal = true"
            />

            <!-- Personal Information -->
            <div class="smoked-charcoal-panel rounded-xl p-5 flex flex-col gap-4">
                <h3 class="text-white font-bold text-base">Personal information</h3>

                <div class="border-b border-[#323232] w-full"></div>

                <div class="grid grid-cols-2 gap-4">
                <!-- First name -->
                <div class="flex flex-col gap-1">
                    <span class="text-[#9E9E9E] text-xs">First name</span>
                    <span class="text-white text-sm">{{ user?.given_name }}</span>
                </div>
                <!-- Last name -->
                <div class="flex flex-col gap-1">
                    <span class="text-[#9E9E9E] text-xs">Last name</span>
                    <span class="text-white text-sm">{{ user?.family_name || '—' }}</span>
                </div>
                <!-- Email -->
                <div class="flex flex-col gap-1">
                    <span class="text-[#9E9E9E] text-xs">Email address</span>
                    <span class="text-white text-sm">{{ user?.email || '—' }}</span>
                </div>
                <!-- Contact -->
                <div class="flex flex-col gap-1">
                    <span class="text-[#9E9E9E] text-xs">Contact number</span>
                    <span class="text-white text-sm">{{ user?.contact_number || '—' }}</span>
                </div>
                </div>

                <!-- Address (full width) -->
                <div class="flex flex-col gap-1">
                <span class="text-gray-500 text-xs">Address</span>
                <span class="text-white text-sm">{{ user?.address || '—' }}</span>
                </div>
            </div>

            <!-- License & ID -->
            <div class="smoked-charcoal-panel rounded-xl p-5 flex flex-col gap-4">
                <h3 class="text-white font-bold text-sm">License & ID</h3>

                <div class="border-b border-[#323232] w-full"></div>

                <!-- Existing IDs from DB -->
                <div v-if="user?.id_images.images?.length" class="flex flex-col gap-2">

                    <ClientProfileIDImageItems
                        v-for="(url, index) in user.id_images.images"
                        :key="'id-' + index"
                        :url="url"
                        :index="Number(index)"
                    />

                </div>

                <!-- Empty State -->
                <div
                    v-else
                    class="flex flex-col items-center justify-center rounded-lg border border-dashed border-white/10 bg-[#0f0f0f] py-6 px-4 text-center"
                >
                    <svg
                        class="w-8 h-8 text-white/20 mb-2"
                        fill="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    </svg>

                    <p class="text-sm text-white/60">
                        No ID images uploaded.
                    </p>

                    <p class="text-xs text-white/40 mt-1">
                        Upload your identification documents to get started.
                    </p>
                </div>


            </div>

        </div>
    
    </div>

    <Footer />

</template>

<script setup lang="ts">
import { ref } from 'vue'

const showEditProfileModal = ref(false)

const { isLoggedIn, authReady } = useAuth()
const { user, authLoading, refreshUser: fetchUser } = useCurrentUser()

const { 
    menuOpen,
    toggleMenu,
    closeMenu,
    handleCloseSidebar,
    handleOpenSidebar
} = useNavbar()

</script>
