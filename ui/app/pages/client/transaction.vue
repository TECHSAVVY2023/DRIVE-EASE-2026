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

    <div class="min-h-screen bg-[#0D0D0D] font-[poppins]">

        <Banner 
            subtitle="View transactions"
            title="My Transactions"
            :breadcrumbs="[
                { label: 'Home', to: '/' },
                { label: 'Transactions' }
            ]"
        />

        <div class="max-w-2xl mx-auto px-4 py-8 flex flex-col gap-5">

            <!-- Transactions Table Card -->
            <div class="bg-[#1a1a1a] border border-[#222] rounded-xl overflow-hidden flex flex-col gap-4">

                <!-- Header -->
                <div class="px-5 pt-5">
                    <h2 class="text-white font-extrabold text-base">All transactions</h2>
                </div>

                <!-- Filters + Sort -->
                <TransactionFilterSort
                    :tabs="tabs"
                    :sort-options="sortOptions"
                    v-model:activeTab="activeTab"
                    v-model:sortBy="sortBy"
                />

                <TransactionTable
                    :transactions="transactions"
                    :current-page="currentPage"
                    :total-pages="totalPages"
                    @update:current-page="currentPage = $event"
                />

            </div>

        </div>

    </div>

    <Footer />

</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

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
    tabs,
    sortOptions,
    activeTab,
    sortBy,
    transactions,
    currentPage,
    totalPages,
    count,
    loading,
} = useTransactionsList()

</script>