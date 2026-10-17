<template>
    <div class="bg-[#161616] border border-[#232323] rounded-xl overflow-hidden">
        
        <!-- Header / Filters -->
        <div
            class="
                flex justify-between items-center
                px-4 sm:px-5
                py-4 sm:py-[18px]
                border-b border-[#232323]
                gap-3 sm:gap-4
                flex-wrap
            "
        >
            <h3 class="text-base font-bold text-white">
                All reviews
            </h3>

            <div class="flex flex-wrap sm:flex-nowrap md:justify-evenly gap-2 w-full max-w-[600px] sm:w-full">

                <!-- Search -->
                <input
                    :value="props.search"
                    @input="handleSearch"
                    placeholder="Search reviews..."
                    class="
                        bg-[#0f0f0f] border border-[#2a2a2a] rounded-lg px-3.5 py-[9px] text-[13px]
                        text-[#e4e4e4] placeholder-[#8a8a8a] w-full outline-none
                        focus:border-[#C1121F] transition-colors
                    "
                />

                <!-- Review Status Filter -->
                <div class="relative flex-1 sm:flex-none">
                    <select
                        :value="props.selectedStatus"
                        @change="handleStatusChange"
                        class="
                            appearance-none w-full sm:w-auto
                            bg-[#0f0f0f] border border-[#2a2a2a] rounded-lg
                            pl-3.5 pr-9 py-2 text-[13px]
                            text-[#c8c8c8] cursor-pointer outline-none
                            hover:border-[#C1121F] focus:border-[#C1121F]
                            transition-colors
                        "
                    >
                        <option value="all">All statuses</option>
                        <option value="pending">Pending</option>
                        <option value="approved">Approved</option>
                        <option value="hidden">Hidden</option>
                    </select>

                    <svg
                        class="absolute right-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-[#8a8a8a] pointer-events-none"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                    >
                        <path d="m6 9 6 6 6-6" />
                    </svg>
                </div>

                <!-- Rating Filter -->
                <div class="relative flex-1 sm:flex-none">
                    <select
                        :value="props.selectedRating"
                        @change="handleRatingChange"
                        class="
                            appearance-none w-full sm:w-auto
                            bg-[#0f0f0f] border border-[#2a2a2a] rounded-lg
                            pl-3.5 pr-9 py-2 text-[13px]
                            text-[#c8c8c8] cursor-pointer outline-none
                            hover:border-[#C1121F] focus:border-[#C1121F]
                            transition-colors
                        "
                    >
                        <option value="all">All ratings</option>
                        <option value="5">5 stars</option>
                        <option value="4">4 stars</option>
                        <option value="3">3 stars</option>
                        <option value="2">2 stars</option>
                        <option value="1">1 star</option>
                    </select>

                    <svg
                        class="absolute right-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-[#8a8a8a] pointer-events-none"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                    >
                        <path d="m6 9 6 6 6-6" />
                    </svg>
                </div>

            </div>
        </div>

        <!-- Table scroll container -->
        <div class="table-scroll w-full overflow-x-auto">
            <table class="w-full min-w-[1050px] border-collapse">

                <thead class="bg-[#0f0f0f]">
                    <tr
                        class="
                            text-left text-[12px]
                            text-[#8a8a8a]
                            uppercase tracking-wide
                            font-semibold
                            border-b border-[#232323]
                        "
                    >
                        <th class="px-5 py-3">Reviewer</th>
                        <th class="px-5 py-3">Vehicle</th>
                        <th class="px-5 py-3">Review</th>
                        <th class="px-5 py-3">Status</th>
                        <th class="px-5 py-3">Date</th>
                        <th class="px-5 py-3">Actions</th>
                    </tr>
                </thead>

                <tbody>
                    <tr
                        v-for="(review, i) in props.reviews"
                        :key="review.id"
                        :class="
                            i !== props.reviews.length - 1
                                ? 'border-b border-[#1c1c1c]'
                                : ''
                        "
                    >
                        <!-- Reviewer -->
                        <td class="px-5 py-3.5 text-sm">
                            <div class="flex items-center gap-3">

                                <!-- Profile Picture -->
                                <img
                                    v-if="review.user.profile_picture"
                                    :src="review.user.profile_picture"
                                    :alt="`${review.user.first_name} ${review.user.last_name}`"
                                    class="w-7 h-7 rounded-full object-cover flex-shrink-0"
                                />

                                <!-- Fallback Icon -->
                                <div
                                    v-else
                                    class="
                                        w-7 h-7 rounded-full bg-[#C1121F]
                                        flex items-center justify-center flex-shrink-0
                                    "
                                >
                                    <svg
                                        class="w-4 h-4 text-white"
                                        fill="currentColor"
                                        viewBox="0 0 24 24"
                                    >
                                        <path
                                            d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4
                                            7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6
                                            1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"
                                        />
                                    </svg>
                                </div>

                                <!-- User Details -->
                                <div class="min-w-0">
                                    <p class="truncate text-sm font-semibold text-white">
                                        {{ review.user.first_name }} {{ review.user.last_name }}
                                    </p>

                                    <p class="mt-0.5 max-w-[170px] truncate text-xs text-[#666]">
                                        {{ review.user.email }}
                                    </p>
                                </div>

                            </div>
                        </td>

                        <!-- Vehicle -->
                        <td class="px-5 py-3.5 text-sm text-[#e4e4e4]">
                            <div class="font-medium">
                                {{ review.car?.brand }} {{ review.car?.model }}
                            </div>
                        </td>

                        <!-- Rating & Review -->
                        <td class="px-5 py-3.5 text-sm max-w-[320px]">
                            <div class="flex flex-col gap-2">

                                <!-- Rating -->
                                <div class="flex items-center gap-1">
                                    <svg
                                        v-for="star in 5"
                                        :key="star"
                                        class="w-3.5 h-3.5"
                                        :class="
                                            star <= review.rating
                                                ? 'text-[#e6a23c]'
                                                : 'text-[#414141]'
                                        "
                                        viewBox="0 0 24 24"
                                        fill="currentColor"
                                    >
                                        <path
                                            d="M12 2.5l2.9 5.88 6.49.94-4.7 4.58 1.11 6.46L12 17.31l-5.8 3.05 1.11-6.46-4.7-4.58 6.49-.94L12 2.5z"
                                        />
                                    </svg>

                                    <span class="ml-1 text-xs text-[#c8c8c8]">
                                        {{ review.rating }}/5
                                    </span>
                                </div>

                                <!-- Review Text -->
                                <p class="text-[#c8c8c8] line-clamp-2 break-words">
                                    {{ review.text }}
                                </p>

                            </div>
                        </td>

                        <!-- Status -->
                        <td class="px-5 py-3.5 text-sm">
                        <span
                            class="
                                inline-flex items-center gap-2
                                rounded-md px-2.5 py-1
                                text-xs capitalize whitespace-nowrap
                            "
                            :class="{
                                'bg-[#e6a23c]/10 text-[#e6a23c]':
                                    review.status === 'pending',

                                'bg-[#3ddc78]/10 text-[#3ddc78]':
                                    review.status === 'approved',

                                'bg-[#c81e2c]/10 text-[#f87171]':
                                    review.status === 'rejected',
                            }"
                        >
                            <span
                                class="w-1.5 h-1.5 rounded-full"
                                :class="{
                                    'bg-[#e6a23c]': review.status === 'pending',
                                    'bg-[#3ddc78]': review.status === 'approved',
                                    'bg-[#c81e2c]': review.status === 'rejected',
                                }"
                            ></span>

                            {{ review.status }}
                        </span>
                        </td>

                        <!-- Date -->
                        <td
                            class="
                                px-5 py-3.5 text-sm text-[#8a8a8a]
                                whitespace-nowrap
                            "
                        >
                            {{ new Date(review.created_at).toLocaleDateString() }}
                        </td>

                    <!-- Actions -->
                    <td class="px-5 py-3.5 text-sm">
                        <div class="flex items-center gap-1.5">

                            <!-- Approve -->
                            <button
                                v-if="review.status !== 'approved'"
                                type="button"
                                class="
                                    inline-flex h-8 items-center gap-1.5 rounded-lg
                                    border border-[#244b35] bg-[#14251b] px-2.5
                                    text-[11px] font-semibold text-[#65c98b]
                                    transition-all hover:border-[#3b8f5b]
                                    hover:bg-[#1b3525] cursor-pointer
                                "
                                @click="$emit('approve', review)"
                            >
                                <svg
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    class="h-3.5 w-3.5"
                                    stroke="currentColor"
                                    stroke-width="2"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                >
                                    <path d="m5 12 4 4L19 6" />
                                </svg>
                                Approve
                            </button>

                            <!-- Reject -->
                            <button
                                v-if="review.status !== 'rejected'"
                                type="button"
                                class="
                                    inline-flex h-8 items-center gap-1.5 rounded-lg
                                    border border-[#4a2528] bg-[#291719] px-2.5
                                    text-[11px] font-semibold text-[#ef777d]
                                    transition-all hover:border-[#c1121f]
                                    hover:bg-[#381a1d] cursor-pointer
                                "
                                @click="$emit('reject', review)"
                            >
                                <svg
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    class="h-3.5 w-3.5"
                                    stroke="currentColor"
                                    stroke-width="2"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                >
                                    <path d="m18 6-12 12M6 6l12 12" />
                                </svg>
                                Reject
                            </button>

                            <!-- Delete -->
                            <button
                                type="button"
                                class="
                                    hover:border-[#c1121f] cursor-pointer
                                    hover:text-[#c1121f] inline-flex h-8 items-center 
                                    gap-1.5 rounded-lg border border-[#292929] 
                                    bg-[#151515] px-2.5 text-[11px] font-semibold 
                                    text-[#9b9b9b] transition-all
                                "
                                @click="$emit('delete', review)"
                            >
                                <svg
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    class="h-3.5 w-3.5"
                                    stroke="currentColor"
                                    stroke-width="2"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                >
                                    <path d="M3 6h18" />
                                    <path d="M8 6V4h8v2" />
                                    <path d="M19 6l-1 14H6L5 6" />
                                    <path d="M10 11v5M14 11v5" />
                                </svg>
                                <p v-if="review.status !== 'pending'">Delete</p>
                            </button>

                        </div>
                    </td>

                    </tr>

                    <!-- Empty state -->
                    <tr v-if="props.reviews.length === 0">
                        <td
                            colspan="7"
                            class="
                                px-5 py-10 text-center
                                text-sm text-[#8a8a8a]
                            "
                        >
                            No reviews found.
                        </td>
                    </tr>
                </tbody>

            </table>
        </div>

        <!-- Pagination -->
        <div
            class="
                flex justify-between items-center
                px-5 py-4
                text-[#8a8a8a] text-[13px]
            "
        >
            <span>
                Showing
                {{
                    props.reviews.length
                        ? (props.currentPage - 1) * props.pageSize + 1
                        : 0
                }}
                –
                {{
                    Math.min(
                        props.currentPage * props.pageSize,
                        props.count
                    )
                }}
                of {{ props.count }} reviews
            </span>

            <div class="flex gap-1.5">

                <!-- Previous -->
                <button
                    type="button"
                    :disabled="!props.previousPage"
                    @click="
                        emit(
                            'update:page',
                            props.currentPage - 1
                        )
                    "
                    class="
                        w-7 h-7 flex items-center justify-center
                        rounded-md border border-[#2a2a2a]
                    "
                    :class="
                        props.previousPage
                            ? 'cursor-pointer hover:bg-[#222]'
                            : 'opacity-40 cursor-not-allowed'
                    "
                >
                    ‹
                </button>

                <!-- Pages -->
                <button
                    v-for="p in props.totalPages"
                    :key="p"
                    type="button"
                    @click="emit('update:page', p)"
                    class="
                        w-7 h-7 flex items-center justify-center
                        rounded-md border
                    "
                    :class="
                        p === props.currentPage
                            ? 'bg-[#c81e2c] border-[#c81e2c] text-white'
                            : 'border-[#2a2a2a] hover:bg-[#222]'
                    "
                >
                    {{ p }}
                </button>

                <!-- Next -->
                <button
                    type="button"
                    :disabled="!props.nextPage"
                    @click="
                        emit(
                            'update:page',
                            props.currentPage + 1
                        )
                    "
                    class="
                        w-7 h-7 flex items-center justify-center
                        rounded-md border border-[#2a2a2a]
                    "
                    :class="
                        props.nextPage
                            ? 'cursor-pointer hover:bg-[#222]'
                            : 'opacity-40 cursor-not-allowed'
                    "
                >
                    ›
                </button>

            </div>
        </div>

    </div>
</template>

<script setup lang="ts">
import type { AdminReview } from '~/utils/api/api'

const props = defineProps<{
    reviews: AdminReview[]
    search: string
    currentPage: number
    count: number
    pageSize: number
    totalPages: number
    nextPage: string | null
    previousPage: string | null
    selectedRating: string
    selectedStatus: string
}>()

const emit = defineEmits<{
    'update:page': [value: number]
    'update:search': [value: string]
    'update:selected-status': [value: string]
    'update:selected-rating': [value: string]
    approve: [review: AdminReview]
    reject: [review: AdminReview]
    delete: [review: AdminReview]
}>()

const handleSearch = (event: Event) => {
    emit('update:search', (event.target as HTMLInputElement).value)
}

const handleStatusChange = (event: Event) => {
    emit('update:selected-status', (event.target as HTMLSelectElement).value)
}

const handleRatingChange = (event: Event) => {
    emit('update:selected-rating', (event.target as HTMLSelectElement).value)
}

</script>