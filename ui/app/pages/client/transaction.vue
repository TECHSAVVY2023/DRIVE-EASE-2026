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

    <div class="charcoal-blueprint-surface min-h-screen font-[poppins]">

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
            <div class="smoked-charcoal-panel rounded-xl overflow-hidden flex flex-col gap-4">

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
                    @select="viewTransaction"
                />

            </div>

        </div>

    </div>

    <Footer />

</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Transaction } from '~/utils/types/booking'

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

const viewTransaction = (transaction: Transaction) => {
    navigateTo(`/client/transaction-details/${transaction.booking_reference}`)
}

</script>
