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

  <div class="min-h-screen bg-[#0D0D0D] font-[poppins]">
    
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
                    v-if="user?.picture"
                    :src="user.picture"
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
                        Member since {{ user?.date_joined ? new Date(user?.date_joined).getFullYear() : '' }}
                    </p>
                </div>
                </div>
                <!-- Edit button -->
                <button 
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
                <h3 class="text-white font-bold text-sm">Personal information</h3>

                <div class="grid grid-cols-2 gap-4">
                <!-- First name -->
                <div class="flex flex-col gap-1">
                    <span class="text-gray-500 text-xs">First name</span>
                    <span class="text-white text-sm font-semibold">{{ user?.given_name }}</span>
                </div>
                <!-- Last name -->
                <div class="flex flex-col gap-1">
                    <span class="text-gray-500 text-xs">Last name</span>
                    <span class="text-white text-sm font-semibold">{{ user?.family_name }}</span>
                </div>
                <!-- Email -->
                <div class="flex flex-col gap-1">
                    <span class="text-gray-500 text-xs">Email address</span>
                    <span class="text-white text-sm font-semibold">{{ user?.email }}</span>
                </div>
                <!-- Contact -->
                <div class="flex flex-col gap-1">
                    <span class="text-gray-500 text-xs">Contact number</span>
                    <span class="text-white text-sm font-semibold">{{ user?.contact_number }}</span>
                </div>
                </div>

                <!-- Address (full width) -->
                <div class="flex flex-col gap-1">
                <span class="text-gray-500 text-xs">Address</span>
                <span class="text-white text-sm font-semibold">{{ user?.address }}</span>
                </div>
            </div>

            <!-- License & ID -->
            <div class="bg-[#1a1a1a] border border-[#222] rounded-xl p-5 flex flex-col gap-4">
                <h3 class="text-white font-bold text-sm">License & ID</h3>

                <div class="flex flex-col gap-3">
                    <div v-for="doc in documents" :key="doc.label" class="flex flex-col gap-1.5">
                        <span class="text-gray-500 text-xs">{{ doc.label }}</span>
                        <div class="flex items-center justify-between bg-[#111] border border-[#2a2a2a] rounded-lg px-4 py-3">
                        <div class="flex items-center gap-3">
                            <!-- File icon -->
                            <div class="w-8 h-8 bg-[#C1121F]/20 rounded-lg flex items-center justify-center flex-shrink-0">
                            <svg class="w-4 h-4 text-[#C1121F]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                            </svg>
                            </div>
                            <div>
                            <p class="text-white text-xs font-semibold">{{ doc.fileName }}</p>
                            <p class="text-gray-500 text-[10px]">{{ doc.fileSize }}</p>
                            </div>
                        </div>
                        <!-- Remove -->
                        <button class="text-gray-400 hover:text-white transition-colors duration-200">
                            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                            </svg>
                        </button>
                        </div>
                    </div>
                </div>
            </div>

        </div>
        
    </div>

    <Footer />

</template>

<script setup lang="ts">

const route = useRoute()
const { setAuth, user } = useAuth()

const { 
    menuOpen,
    toggleMenu,
    closeMenu,
    handleCloseSidebar,
    handleOpenSidebar
} = useNavbar()

if (route.query.token) {
    await setAuth(route.query.token as string)
}

interface Profile {
    firstName: string
    lastName: string
    email: string
    contact: string
    address: string
    memberSince: string
    avatar: string
}

interface Document {
    label: string
    fileName: string
    fileSize: string
}

const profile: Profile = {
    firstName: 'Aljubehr',
    lastName: 'Sahiol',
    email: 'Aljubehr',
    contact: 'Sahiol',
    address: 'Brgy. Nazareth, Cagayan de Oro City, Misamis Oriental',
    memberSince: '2020',
    avatar: '',
}

const documents: Document[] = [
  { label: 'License', fileName: 'License.jpg', fileSize: '10 mb' },
  { label: 'ID', fileName: 'ID.jpg', fileSize: '10 mb' },
]
</script>