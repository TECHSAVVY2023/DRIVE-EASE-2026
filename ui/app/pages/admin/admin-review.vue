<template>
    <div class="flex h-screen bg-[#0D0D0D] font-[poppins] overflow-hidden text-white">

        <!-- Sidebar -->
        <AdminCommonSidebarNav
            :sidebarOpen="sidebarOpen"
            @close-sidebar="sidebarOpen = false"
        />
        <!-- Main -->
        <div class="flex-1 flex flex-col overflow-hidden">

            <!-- Topbar -->
            <AdminCommonTopbarNav
                :user="user"
                @open-sidebar="handleOpenSidebar"
                @close-sidebar="handleCloseSidebar"
                title="Reviews"
                :isLoggedIn="isLoggedIn"
            />

            <main class="flex-1 overflow-y-auto px-8 py-8">

                <!-- Page heading -->
                <div class="flex justify-between items-end mb-[22px]">
                    <div>
                        <h2 class="text-[22px] font-extrabold">
                            Reviews
                        </h2>

                        <div class="text-[#8a8a8a] text-[13px] mt-1">
                            Manage customer reviews and ratings
                        </div>
                    </div>

                </div>

                <!-- Stats -->
                <AdminCommonStatsCards :cards="statCards"/>

                <AdminReviewTable
                    :reviews="reviews"

                    :search="search"
                    :current-page="currentPage"
                    :count="count"
                    :page-size="pageSize"
                    :total-pages="totalPages"
                    :next-page="nextPage"
                    :previous-page="previousPage"

                    :selected-rating="selectedRating"
                    :selected-status="selectedStatus"

                    @update:search="search = $event"
                    @update:page="currentPage = $event"

                    @update:selected-rating="selectedRating = $event"
                    @update:selected-status="selectedStatus = $event"

                    @approve="(review) => handleStatus(review, 'approved')"
                    @reject="(review) => handleStatus(review, 'rejected')"
                    @delete="handleDelete"
                />

            </main>

        </div>
    </div>

</template>

<script setup lang="ts">
import { type AdminReview } from '~/utils/api/api'

const { isLoggedIn, authReady } = useAuth()
const { apiFetch } = useApiFetch()
const { $swal } = useNuxtApp()
const { user } = useCurrentUser()

const sidebarOpen = ref<boolean>(false)

const handleCloseSidebar = (): void => {
    sidebarOpen.value = false
}

const handleOpenSidebar = (): void => {
    sidebarOpen.value = true
}

const statCards = computed(() => [
    {
        label: 'Total reviews',
        value: stats.value.total,
        icon: `<svg viewBox="0 0 24 24" fill="none">
            <rect x="4" y="5" width="16" height="15" rx="2"/>
            <path d="M8 3v4M16 3v4M4 9h16"/>
            <path d="M8 13h2M14 13h2M8 16h2M14 16h2"/>
        </svg>`
    },
    {
        label: 'Average rating',
        value: stats.value.average_rating.toFixed(1),
        icon: `<svg viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="9"/>
            <path d="M12 7v5l3 2"/>
        </svg>`
    },
    {
        label: 'Pending reviews',
        value: stats.value.pending,
        icon: `<svg viewBox="0 0 24 24" fill="none">
            <path d="M5 16l1.5-6h11L19 16"/>
            <path d="M4 16h16v3H4z"/>
            <circle cx="7.5" cy="19" r="1.5"/>
            <circle cx="16.5" cy="19" r="1.5"/>
            <path d="M8 10l1.5-3h5L16 10"/>
        </svg>`
    },
    {
        label: 'Published reviews',
        value: stats.value.approved,
        icon: `<svg viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="9"/>
            <path d="M7.5 12l3 3 6-6"/>
        </svg>`
    },
])

const { reviews, count, stats, nextPage, previousPage, currentPage, search,
        pageSize, totalPages, selectedStatus, selectedRating
    } = useAdminReviewsList()


const { handleStatus: updateStatus, handleDeleteReview: deleteReview } = useAdminReviewEdit()

async function handleStatus(
    review: AdminReview,
    newStatus: 'approved' | 'rejected'
) {
    const result = await updateStatus(review, newStatus)

    if (!result.success) return

    window.location.reload()
}

async function handleDelete(review: AdminReview) {
    const result = await $swal.fire({
        title: 'Delete review?',
        text: `Are you sure you want to delete this review by ${review.user.first_name} ${review.user.last_name}?`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel',
        background: '#1a1a1a',
        confirmButtonColor: '#C1121F',
        color: '#ffffff',
    })

    if (!result.isConfirmed) return

    const response = await deleteReview(review)

    if (!response.success) return

    window.location.reload()
}

onMounted(() => {
    document.documentElement.classList.add('admin-page')
})

onBeforeUnmount(() => {
    document.documentElement.classList.remove('admin-page')
})

</script>
