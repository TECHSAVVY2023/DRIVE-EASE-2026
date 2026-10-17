```vue
<script setup lang="ts">
type Status = 'pending' | 'published' | 'hidden'

interface Review {
  id: string
  rating: 1 | 2 | 3 | 4 | 5
  comment: string
  created_at: string
  status: Status
  customer: { name: string; email: string }
  car: { brand: string; model: string; year: number; image?: string }
}

// Replace with your real fetch:
// const { data: reviews } = await useFetch<Review[]>('/api/admin/reviews')
const reviews = ref<Review[]>([
  {
    id: 'r1',
    rating: 5,
    comment:
      'Smooth pickup and the Raptor was spotless. Handled the city and the rough road to the beach without any issue. Will book again for the next trip.',
    created_at: '2026-10-07T10:12',
    status: 'pending',
    customer: { name: 'Zen Itsuka', email: 'zitsuka7@gmail.com' },
    car: { brand: 'Fords', model: 'Raptor', year: 2022 },
  },
  {
    id: 'r2',
    rating: 4,
    comment: 'Good car for the price. A bit old but ran fine the whole time.',
    created_at: '2026-09-19T15:30',
    status: 'published',
    customer: { name: 'Zen Itsuka', email: 'zitsuka7@gmail.com' },
    car: { brand: 'Toyota', model: 'Wigo', year: 2003 },
  },
  {
    id: 'r3',
    rating: 2,
    comment: 'Return process took too long and the aircon was weak.',
    created_at: '2026-09-12T09:05',
    status: 'pending',
    customer: { name: 'Mika Santos', email: 'mika.santos@gmail.com' },
    car: { brand: 'Toyota', model: 'Vios', year: 2023 },
  },
  {
    id: 'r4',
    rating: 5,
    comment: 'Great service, very responsive on chat.',
    created_at: '2026-09-02T18:44',
    status: 'published',
    customer: { name: 'Carlo Reyes', email: 'carlo.r@yahoo.com' },
    car: { brand: 'Honda', model: 'CR-V', year: 2021 },
  },
  {
    id: 'r5',
    rating: 1,
    comment: 'Spam spam spam visit my website for cheap deals.',
    created_at: '2026-08-28T03:21',
    status: 'hidden',
    customer: { name: 'Unknown User', email: 'promo@example.com' },
    car: { brand: 'Toyota', model: 'Vios', year: 2023 },
  },
  {
    id: 'r6',
    rating: 4,
    comment: 'Clean and comfortable, perfect for a family of five.',
    created_at: '2026-08-15T12:00',
    status: 'published',
    customer: { name: 'Anna Cruz', email: 'anna.cruz@gmail.com' },
    car: { brand: 'Suzuki', model: 'Ertiga', year: 2022 },
  },
  {
    id: 'r7',
    rating: 3,
    comment: 'Decent overall.',
    created_at: '2026-08-01T08:10',
    status: 'published',
    customer: { name: 'Paolo Lim', email: 'paolo.lim@gmail.com' },
    car: { brand: 'Fords', model: 'Raptor', year: 2022 },
  },
])

const STATUS_STYLES: Record<Status, string> = {
  pending: 'text-amber-300 bg-amber-500/10 border-amber-500/20',
  published: 'text-emerald-300 bg-emerald-500/10 border-emerald-500/20',
  hidden: 'text-[#929292] bg-white/[0.04] border-white/10',
}

const STATUS_ACTIONS: Record<Status, { label: string; to: Status; icon: string }[]> = {
  pending: [
    { label: 'Approve', to: 'published', icon: 'tabler:check' },
    { label: 'Reject', to: 'hidden', icon: 'tabler:x' },
  ],
  published: [{ label: 'Hide', to: 'hidden', icon: 'tabler:eye-off' }],
  hidden: [{ label: 'Publish', to: 'published', icon: 'tabler:eye' }],
}

// Stats
const count = (status: Status) => reviews.value.filter(r => r.status === status).length

const averageRating = computed(() => {
  const published = reviews.value.filter(r => r.status === 'published')
  if (!published.length) return '0.0'

  return (
    published.reduce((sum, r) => sum + r.rating, 0) / published.length
  ).toFixed(1)
})

// Filters + pagination
const search = ref('')
const statusFilter = ref<'all' | Status>('all')
const ratingFilter = ref<'all' | '1' | '2' | '3' | '4' | '5'>('all')
const page = ref(1)
const pageSize = 5

const filtered = computed(() => {
  const q = search.value.trim().toLowerCase()

  return reviews.value.filter(r => {
    if (statusFilter.value !== 'all' && r.status !== statusFilter.value) return false
    if (ratingFilter.value !== 'all' && r.rating !== Number(ratingFilter.value)) return false

    if (!q) return true

    return [r.comment, r.customer.name, r.customer.email, r.car.brand, r.car.model]
      .join(' ')
      .toLowerCase()
      .includes(q)
  })
})

const totalPages = computed(() =>
  Math.max(1, Math.ceil(filtered.value.length / pageSize)),
)

const paged = computed(() =>
  filtered.value.slice((page.value - 1) * pageSize, page.value * pageSize),
)

const showingFrom = computed(() =>
  filtered.value.length ? (page.value - 1) * pageSize + 1 : 0,
)

const showingTo = computed(() =>
  Math.min(page.value * pageSize, filtered.value.length),
)

watch([search, statusFilter, ratingFilter], () => (page.value = 1))

watch(totalPages, pages => {
  if (page.value > pages) page.value = pages
})

// Long comments collapse to two lines until clicked
const expanded = ref(new Set<string>())

function toggle(id: string) {
  expanded.value.has(id)
    ? expanded.value.delete(id)
    : expanded.value.add(id)
}

// Actions
async function setStatus(review: Review, status: Status) {
  // await $fetch(`/api/admin/reviews/${review.id}`, {
  //   method: 'PATCH',
  //   body: { status },
  // })

  review.status = status
}

const pendingDelete = ref<Review | null>(null)

async function confirmDelete() {
  if (!pendingDelete.value) return

  // await $fetch(`/api/admin/reviews/${pendingDelete.value.id}`, {
  //   method: 'DELETE',
  // })

  const id = pendingDelete.value.id
  reviews.value = reviews.value.filter(r => r.id !== id)
  pendingDelete.value = null
}

const fmtDate = (d: string) =>
  new Date(d).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })

const card = 'rounded-2xl border border-[#222] bg-[#111111]'

const control =
  'h-10 rounded-lg border border-[#252525] bg-[#0d0d0d] px-3.5 text-sm text-white placeholder:text-[#666] transition-colors focus:border-[#C1121F] focus:outline-none [color-scheme:dark]'
</script>

<template>
    <div class="min-h-full px-4 py-6 sm:px-8 sm:py-8">

        <!-- Page heading -->
        <div class="mb-7">
        <div class="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
            <div>
            <div class="mb-2 flex items-center gap-2 text-xs font-medium text-[#666]">
                <Icon name="tabler:settings" class="size-3.5" />
                <span>Administration</span>
                <Icon name="tabler:chevron-right" class="size-3" />
                <span class="text-[#929292]">Reviews</span>
            </div>

            <h1 class="text-2xl font-extrabold tracking-tight text-white sm:text-3xl">
                Review moderation
            </h1>

            <p class="mt-1 text-sm text-[#777]">
                Manage customer feedback and keep your reviews trustworthy.
            </p>
            </div>

            <!-- Pending indicator -->
            <button
            v-if="count('pending')"
            class="flex w-fit items-center gap-2 rounded-lg border border-amber-500/20 bg-amber-500/[0.06] px-3.5 py-2 text-xs font-semibold text-amber-300 transition-colors hover:bg-amber-500/10"
            @click="statusFilter = 'pending'"
            >
            <span class="size-1.5 rounded-full bg-amber-400" />
            {{ count('pending') }} reviews need attention
            </button>
        </div>
        </div>

        <!-- Stats -->
        <div class="mb-6 grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-5">
        <!-- Total reviews -->
        <div :class="[card, 'relative overflow-hidden p-5']">
            <div class="mb-5 flex size-10 items-center justify-center rounded-xl bg-[#C1121F]/10 text-[#C1121F]">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="1.8"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="size-5"
                aria-hidden="true"
            >
                <path d="M21 11.5a8.4 8.4 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.4 8.4 0 0 1-3.8-.9L3 21l1.9-5.7a8.4 8.4 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.4 8.4 0 0 1 3.8-.9h.5a8.5 8.5 0 0 1 8 8v.5Z" />
            </svg>
            </div>

            <p class="text-sm text-[#929292]">Total reviews</p>
            <p class="mt-1 text-2xl font-extrabold text-white">{{ reviews.length }}</p>
            <p class="mt-1 text-xs text-[#6f6f6f]">All customer feedback</p>

            <div class="absolute inset-x-0 bottom-0 h-0.5 bg-[#C1121F]/60" />
        </div>

        <!-- Average rating -->
        <div :class="[card, 'relative overflow-hidden p-5']">
            <div class="mb-5 flex size-10 items-center justify-center rounded-xl bg-amber-400/10 text-amber-400">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="1.8"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="size-5"
                aria-hidden="true"
            >
                <path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1.1 6.2-5.6-3-5.6 3 1.1-6.2L3 9.6l6.2-.9L12 3Z" />
            </svg>
            </div>

            <p class="text-sm text-[#929292]">Average rating</p>
            <p class="mt-1 text-2xl font-extrabold text-white">
            {{ averageRating }}<span class="text-sm font-normal text-[#929292]"> / 5</span>
            </p>
            <p class="mt-1 text-xs text-[#6f6f6f]">From published reviews</p>

            <div class="absolute inset-x-0 bottom-0 h-0.5 bg-amber-400/60" />
        </div>

        <!-- Pending approval -->
        <button
            type="button"
            :class="[
            card,
            'relative overflow-hidden p-5 text-left transition-colors hover:border-amber-500/40',
            statusFilter === 'pending' ? 'border-amber-500/50 bg-amber-500/[0.04]' : '',
            ]"
            @click="statusFilter = statusFilter === 'pending' ? 'all' : 'pending'"
        >
            <div class="mb-5 flex size-10 items-center justify-center rounded-xl bg-amber-400/10 text-amber-400">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="1.8"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="size-5"
                aria-hidden="true"
            >
                <circle cx="12" cy="12" r="9" />
                <path d="M12 7v5l3 2" />
            </svg>
            </div>

            <p class="text-sm text-[#929292]">Pending approval</p>
            <p class="mt-1 text-2xl font-extrabold text-white">{{ count('pending') }}</p>
            <p class="mt-1 text-xs text-[#6f6f6f]">Awaiting moderation</p>

            <div class="absolute inset-x-0 bottom-0 h-0.5 bg-amber-400/60" />
        </button>

        <!-- Published -->
        <button
            type="button"
            :class="[
            card,
            'relative overflow-hidden p-5 text-left transition-colors hover:border-emerald-500/40',
            statusFilter === 'published' ? 'border-emerald-500/50 bg-emerald-500/[0.04]' : '',
            ]"
            @click="statusFilter = statusFilter === 'published' ? 'all' : 'published'"
        >
            <div class="mb-5 flex size-10 items-center justify-center rounded-xl bg-emerald-400/10 text-emerald-400">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="1.8"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="size-5"
                aria-hidden="true"
            >
                <circle cx="12" cy="12" r="9" />
                <path d="m8 12 2.5 2.5L16 9" />
            </svg>
            </div>

            <p class="text-sm text-[#929292]">Published</p>
            <p class="mt-1 text-2xl font-extrabold text-white">{{ count('published') }}</p>
            <p class="mt-1 text-xs text-[#6f6f6f]">Visible to customers</p>

            <div class="absolute inset-x-0 bottom-0 h-0.5 bg-emerald-400/60" />
        </button>

        <!-- Hidden -->
        <button
            type="button"
            :class="[
            card,
            'relative overflow-hidden p-5 text-left transition-colors hover:border-white/20',
            statusFilter === 'hidden' ? 'border-white/30 bg-white/[0.04]' : '',
            ]"
            @click="statusFilter = statusFilter === 'hidden' ? 'all' : 'hidden'"
        >
            <div class="mb-5 flex size-10 items-center justify-center rounded-xl bg-white/5 text-[#929292]">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="1.8"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="size-5"
                aria-hidden="true"
            >
                <path d="M3 3l18 18" />
                <path d="M10.6 10.6a2 2 0 0 0 2.8 2.8" />
                <path d="M9.9 5.2A10.8 10.8 0 0 1 12 5c5 0 8.3 4.5 9 7a10.8 10.8 0 0 1-2.1 3.8" />
                <path d="M6.2 6.2C4.1 7.6 2.7 10 2 12c.4 1.4 1.4 3.1 3.2 4.5A10.5 10.5 0 0 0 12 19" />
            </svg>
            </div>

            <p class="text-sm text-[#929292]">Hidden</p>
            <p class="mt-1 text-2xl font-extrabold text-white">{{ count('hidden') }}</p>
            <p class="mt-1 text-xs text-[#6f6f6f]">Not shown publicly</p>

            <div class="absolute inset-x-0 bottom-0 h-0.5 bg-white/20" />
        </button>
        </div>

        <!-- Main review panel -->
        <section :class="card">

        <!-- Toolbar -->
        <div class="border-b border-[#222] px-4 py-4 sm:px-5">
            <div class="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">

            <div>
                <div class="flex items-center gap-2">
                <h2 class="text-sm font-bold text-white">
                    All reviews
                </h2>

                <span class="rounded-md bg-white/[0.05] px-2 py-0.5 text-[10px] font-semibold text-[#777]">
                    {{ filtered.length }}
                </span>
                </div>

                <p class="mt-1 text-xs text-[#666]">
                Review, approve, hide, or remove customer feedback.
                </p>
            </div>

            <div class="flex flex-col gap-2 sm:flex-row">

                <!-- Search -->
                <div class="relative sm:w-64">
                <Icon
                    name="tabler:search"
                    class="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-[#555]"
                />

                <input
                    v-model="search"
                    type="search"
                    placeholder="Search reviews..."
                    :class="[control, 'w-full pl-9']"
                />
                </div>

                <!-- Status -->
                <div class="relative">
                <select
                    v-model="statusFilter"
                    :class="[control, 'w-full appearance-none pr-9 sm:w-32']"
                >
                    <option value="all">All status</option>
                    <option value="pending">Pending</option>
                    <option value="published">Published</option>
                    <option value="hidden">Hidden</option>
                </select>

                <Icon
                    name="tabler:chevron-down"
                    class="pointer-events-none absolute right-3 top-1/2 size-3.5 -translate-y-1/2 text-[#555]"
                />
                </div>

                <!-- Rating -->
                <div class="relative">
                <select
                    v-model="ratingFilter"
                    :class="[control, 'w-full appearance-none pr-9 sm:w-32']"
                >
                    <option value="all">All ratings</option>
                    <option v-for="n in [5, 4, 3, 2, 1]" :key="n" :value="String(n)">
                    {{ n }} star{{ n > 1 ? 's' : '' }}
                    </option>
                </select>

                <Icon
                    name="tabler:chevron-down"
                    class="pointer-events-none absolute right-3 top-1/2 size-3.5 -translate-y-1/2 text-[#555]"
                />
                </div>
            </div>
            </div>
        </div>

        <!-- Table -->
        <div class="overflow-x-auto">
            <table class="w-full min-w-[1050px] text-left">

            <thead class="border-b border-[#222] bg-[#0d0d0d]">
                <tr>
                <th class="px-5 py-3 text-[10px] font-bold uppercase tracking-wider text-[#666]">
                    Review
                </th>

                <th class="px-5 py-3 text-[10px] font-bold uppercase tracking-wider text-[#666]">
                    Customer
                </th>

                <th class="px-5 py-3 text-[10px] font-bold uppercase tracking-wider text-[#666]">
                    Vehicle
                </th>

                <th class="px-5 py-3 text-[10px] font-bold uppercase tracking-wider text-[#666]">
                    Submitted
                </th>

                <th class="px-5 py-3 text-[10px] font-bold uppercase tracking-wider text-[#666]">
                    Status
                </th>

                <th class="px-5 py-3 text-right text-[10px] font-bold uppercase tracking-wider text-[#666]">
                    Actions
                </th>
                </tr>
            </thead>

            <tbody>

                <!-- Empty -->
                <tr v-if="!paged.length">
                <td colspan="6" class="px-5 py-16 text-center">
                    <div class="mx-auto flex size-11 items-center justify-center rounded-xl bg-white/[0.04] text-[#555]">
                    <Icon name="tabler:message-off" class="size-5" />
                    </div>

                    <p class="mt-3 text-sm font-semibold text-white">
                    No reviews found
                    </p>

                    <p class="mt-1 text-xs text-[#666]">
                    Try adjusting your search or filters.
                    </p>
                </td>
                </tr>

                <!-- Review rows -->
                <tr
                v-for="review in paged"
                :key="review.id"
                class="border-b border-[#1d1d1d] align-top transition-colors last:border-b-0 hover:bg-white/[0.018]"
                >

                <!-- Review -->
                <td class="max-w-[390px] px-5 py-5">

                    <div class="mb-2 flex items-center gap-1">
                    <Icon
                        v-for="n in 5"
                        :key="n"
                        :name="n <= review.rating ? 'tabler:star-filled' : 'tabler:star'"
                        class="size-3.5"
                        :class="n <= review.rating ? 'text-amber-400' : 'text-[#333]'"
                    />

                    <span class="ml-1 text-[11px] font-semibold text-[#666]">
                        {{ review.rating }}.0
                    </span>
                    </div>

                    <p
                    class="text-sm leading-6 text-[#d8d8d8]"
                    :class="expanded.has(review.id) ? '' : 'line-clamp-2'"
                    >
                    {{ review.comment }}
                    </p>

                    <button
                    v-if="review.comment.length > 100"
                    class="mt-1.5 text-[11px] font-semibold text-[#666] transition-colors hover:text-white"
                    @click="toggle(review.id)"
                    >
                    {{ expanded.has(review.id) ? 'Show less' : 'Read more' }}
                    </button>
                </td>

                <!-- Customer -->
                <td class="px-5 py-5">
                    <div class="flex items-center gap-3">

                    <div class="flex size-8 shrink-0 items-center justify-center rounded-full bg-[#1c1c1c] text-xs font-bold text-[#aaa]">
                        {{ review.customer.name.charAt(0).toUpperCase() }}
                    </div>

                    <div class="min-w-0">
                        <p class="truncate text-sm font-semibold text-white">
                        {{ review.customer.name }}
                        </p>

                        <p class="mt-0.5 max-w-[170px] truncate text-xs text-[#666]">
                        {{ review.customer.email }}
                        </p>
                    </div>

                    </div>
                </td>

                <!-- Vehicle -->
                <td class="px-5 py-5">
                    <div class="flex items-center gap-3">

                    <div class="flex size-10 shrink-0 items-center justify-center overflow-hidden rounded-lg border border-[#252525] bg-[#171717]">
                        <img
                        v-if="review.car.image"
                        :src="review.car.image"
                        :alt="`${review.car.brand} ${review.car.model}`"
                        class="size-full object-cover"
                        />

                        <Icon
                        v-else
                        name="tabler:car"
                        class="size-4 text-[#555]"
                        />
                    </div>

                    <div>
                        <p class="text-sm font-semibold text-white">
                        {{ review.car.brand }} {{ review.car.model }}
                        </p>

                        <p class="mt-0.5 text-xs text-[#666]">
                        {{ review.car.year }}
                        </p>
                    </div>

                    </div>
                </td>

                <!-- Date -->
                <td class="whitespace-nowrap px-5 py-5">
                    <p class="text-sm font-medium text-[#d0d0d0]">
                    {{ fmtDate(review.created_at) }}
                    </p>

                    <p class="mt-0.5 text-[11px] text-[#555]">
                    {{ new Date(review.created_at).toLocaleTimeString('en-US', {
                        hour: 'numeric',
                        minute: '2-digit'
                    }) }}
                    </p>
                </td>

                <!-- Status -->
                <td class="px-5 py-5">
                    <span
                    class="inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-[10px] font-bold capitalize"
                    :class="STATUS_STYLES[review.status]"
                    >
                    <span
                        class="size-1.5 rounded-full"
                        :class="{
                        'bg-amber-400': review.status === 'pending',
                        'bg-emerald-400': review.status === 'published',
                        'bg-[#555]': review.status === 'hidden',
                        }"
                    />

                    {{ review.status }}
                    </span>
                </td>

                <!-- Actions -->
                <td class="px-5 py-5">
                    <div class="flex justify-end gap-1.5">

                    <button
                        v-for="action in STATUS_ACTIONS[review.status]"
                        :key="action.to"
                        class="inline-flex h-8 items-center gap-1.5 rounded-lg border border-[#292929] bg-[#151515] px-2.5 text-[11px] font-semibold text-[#aaa] transition-all hover:border-[#444] hover:bg-[#1c1c1c] hover:text-white"
                        :class="{
                        'hover:border-emerald-500/30 hover:text-emerald-300': action.to === 'published',
                        'hover:border-amber-500/30 hover:text-amber-300': action.to === 'hidden' && review.status === 'pending',
                        }"
                        @click="setStatus(review, action.to)"
                    >
                        <Icon :name="action.icon" class="size-3.5" />
                        {{ action.label }}
                    </button>

                    <button
                        class="flex size-8 items-center justify-center rounded-lg border border-[#292929] bg-[#151515] text-[#666] transition-all hover:border-red-500/30 hover:bg-red-500/[0.05] hover:text-[#C1121F]"
                        title="Delete review"
                        aria-label="Delete review"
                        @click="pendingDelete = review"
                    >
                        <Icon name="tabler:trash" class="size-3.5" />
                    </button>

                    </div>
                </td>

                </tr>
            </tbody>
            </table>
        </div>

        <!-- Footer -->
        <div class="flex flex-col gap-3 border-t border-[#222] px-5 py-4 sm:flex-row sm:items-center sm:justify-between">

            <p class="text-xs text-[#666]">
            Showing
            <span class="font-semibold text-[#aaa]">{{ showingFrom }}</span>
            –
            <span class="font-semibold text-[#aaa]">{{ showingTo }}</span>
            of
            <span class="font-semibold text-[#aaa]">{{ filtered.length }}</span>
            reviews
            </p>

            <div class="flex items-center gap-1.5">

            <button
                :disabled="page === 1"
                class="flex size-8 items-center justify-center rounded-lg border border-[#252525] text-[#666] transition-colors hover:border-[#3a3a3a] hover:text-white disabled:pointer-events-none disabled:opacity-30"
                aria-label="Previous page"
                @click="page--"
            >
                <Icon name="tabler:chevron-left" class="size-4" />
            </button>

            <button
                v-for="n in totalPages"
                :key="n"
                class="flex size-8 items-center justify-center rounded-lg text-[11px] font-bold transition-colors"
                :class="
                n === page
                    ? 'bg-[#C1121F] text-white shadow-[0_0_12px_rgba(193,18,31,0.18)]'
                    : 'border border-[#252525] text-[#666] hover:border-[#3a3a3a] hover:text-white'
                "
                @click="page = n"
            >
                {{ n }}
            </button>

            <button
                :disabled="page === totalPages"
                class="flex size-8 items-center justify-center rounded-lg border border-[#252525] text-[#666] transition-colors hover:border-[#3a3a3a] hover:text-white disabled:pointer-events-none disabled:opacity-30"
                aria-label="Next page"
                @click="page++"
            >
                <Icon name="tabler:chevron-right" class="size-4" />
            </button>

            </div>
        </div>
        </section>

        <!-- Delete confirmation -->
        <Teleport to="body">
        <Transition
            enter-active-class="transition duration-150"
            leave-active-class="transition duration-100"
            enter-from-class="opacity-0"
            leave-to-class="opacity-0"
        >
            <div
            v-if="pendingDelete"
            class="fixed inset-0 z-50 flex items-center justify-center bg-black/75 p-4 backdrop-blur-sm"
            @click.self="pendingDelete = null"
            >
            <div
                class="w-full max-w-md overflow-hidden rounded-2xl border border-[#292929] bg-[#111111] shadow-2xl"
                role="alertdialog"
                aria-modal="true"
            >
                <div class="border-b border-[#222] px-6 py-5">
                <div class="flex items-start gap-3">

                    <div class="flex size-10 shrink-0 items-center justify-center rounded-xl bg-red-500/10 text-[#C1121F]">
                    <Icon name="tabler:trash" class="size-5" />
                    </div>

                    <div>
                    <h3 class="text-base font-extrabold text-white">
                        Delete review?
                    </h3>

                    <p class="mt-1 text-xs leading-5 text-[#666]">
                        This action permanently removes the review from your system.
                    </p>
                    </div>

                </div>
                </div>

                <div class="px-6 py-5">
                <div class="rounded-xl border border-[#222] bg-[#0d0d0d] p-4">

                    <div class="flex items-center justify-between">
                    <p class="text-sm font-semibold text-white">
                        {{ pendingDelete.customer.name }}
                    </p>

                    <div class="flex items-center gap-0.5">
                        <Icon
                        v-for="n in 5"
                        :key="n"
                        :name="n <= pendingDelete.rating ? 'tabler:star-filled' : 'tabler:star'"
                        class="size-3"
                        :class="n <= pendingDelete.rating ? 'text-amber-400' : 'text-[#333]'"
                        />
                    </div>
                    </div>

                    <p class="mt-2 line-clamp-2 text-xs leading-5 text-[#777]">
                    {{ pendingDelete.comment }}
                    </p>

                </div>

                <p class="mt-3 text-xs leading-5 text-[#555]">
                    If you only want this review removed from the public site,
                    consider hiding it instead.
                </p>
                </div>

                <div class="flex flex-col-reverse gap-2 border-t border-[#222] bg-[#0d0d0d] px-6 py-4 sm:flex-row sm:justify-end">
                <button
                    class="h-9 rounded-lg border border-[#292929] px-4 text-xs font-semibold text-[#aaa] transition-colors hover:border-[#444] hover:text-white"
                    @click="pendingDelete = null"
                >
                    Cancel
                </button>

                <button
                    class="h-9 rounded-lg bg-[#C1121F] px-4 text-xs font-bold text-white transition-colors hover:bg-red-700"
                    @click="confirmDelete"
                >
                    Delete review
                </button>
                </div>
            </div>
            </div>
        </Transition>
        </Teleport>

    </div>
</template>
