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
    <UserEditProfileModal 
        :user="user"
        v-model="showEditProfileModal"
        @updated="fetchUser"
    />

  <div class="h-fit bg-[#0D0D0D] font-[poppins]">
    
    <Banner 
        subtitle="Manage account"
        title="My Profile"
        :breadcrumbs="[
            { label: 'Home', to: '/' },
            { label: 'Profile' }
        ]"
    />

        <div class="max-w-lg mx-auto px-4 py-8 flex flex-col gap-4">

            <!-- Profile Card -->
            <div class="bg-[#1a1a1a] border border-[#222] rounded-xl p-5 flex items-center justify-between gap-4">
                <div class="flex items-center gap-4">
                <!-- Avatar -->
                <div class="w-16 h-16 rounded-full bg-[#C1121F] flex-shrink-0 overflow-hidden flex items-center justify-center">
                    <img
                    v-if="user?.profile_picture"
                    :src="user.profile_picture"
                    :alt="user.given_name + ' ' + user.family_name"
                    class="w-full h-full object-cover"
                    />
                    <span v-else class="text-white text-2xl font-extrabold">
                    {{ user?.given_name?.charAt(0) }}
                    </span>

                </div>
                <!-- Name + Member since -->
                <div>
                    <p class="text-white font-bold text-lg leading-tight">{{ user?.given_name }} {{ user?.family_name }}</p>
                    <p class="text-gray-400 text-xs mt-0.5">
                        Member since {{ user?.date_created ? new Date(user.date_created).getFullYear() : '' }}
                    </p>
                </div>
                </div>
                <!-- Edit button -->
                <button 
                    @click="showEditProfileModal = true"
                    class="
                        bg-[#C1121F] hover:bg-[#9B0E18] rounded-lg
                        text-white text-xs font-semibold px-4 py-2 
                        flex-shrink-0 
                        transition-colors duration-200
                    "
                >
                Edit profile
                </button>
            </div>

            <!-- Personal Information -->
            <div class="bg-[#1a1a1a] border border-[#222] rounded-xl p-5 flex flex-col gap-4">
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
            <div class="bg-[#1a1a1a] border border-[#222] rounded-xl p-5 flex flex-col gap-4">
                <h3 class="text-white font-bold text-sm">License & ID</h3>

                <div class="border-b border-[#323232] w-full"></div>

                <!-- Existing IDs from DB -->
                <div v-if="user?.id_images.images?.length" class="flex flex-row gap-2">
                    <a
                        v-for="(url, index) in user.id_images.images"
                        :key="'existing-' + index"
                        :href="url"
                        target="_blank"
                        class="group flex items-center justify-between bg-[#0f0f0f] border border-white/10 hover:border-[#c1121f] rounded-lg px-3 py-2 transition-colors cursor-pointer w-full"
                    >
                        <div class="flex items-center gap-3">
                            <div class="w-8 h-8 flex items-center justify-center bg-[#1a1a1a] rounded">
                                <svg class="w-4 h-4 text-[#c1121f]" fill="currentColor" viewBox="0 0 24 24">
                                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                                </svg>
                            </div>

                            <span
                                class="text-white text-xs transition-colors group-hover:text-[#c1121f]"
                            >
                                View ID {{ Number(index) + 1 }}
                            </span>
                        </div>
                    </a>
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

const { isLoggedIn } = useAuth()
const { apiFetch } = useApiFetch()

const user = ref<any>(null)

const fetchUser = async () => {
    if (!isLoggedIn.value) {
        user.value = null
        return
    }
    user.value = await apiFetch('/auth/me/')
}

watch(isLoggedIn, async (val) => {
    if (val) {
        await fetchUser()
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

</script>