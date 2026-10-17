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
                All vehicles
            </h3>

            <div class="flex flex-wrap sm:flex-nowrap md:justify-evenly gap-2 w-full max-w-[600px] sm:w-full">

                <!-- Search -->
                <input
                    :value="props.search"
                    @input="handleSearch"
                    placeholder="Search vehicles..."
                    class="
                        bg-[#0f0f0f] border border-[#2a2a2a] rounded-lg px-3.5 py-[9px] text-[13px]
                        text-[#e4e4e4] placeholder-[#8a8a8a] w-full outline-none
                        focus:border-[#C1121F] transition-colors
                    "
                />

                <!-- Type filter -->
                <div class="relative flex-1 sm:flex-none">
                    <select
                        :value="props.selectedCarType"
                        @change="handleTypeChange"
                        class="
                            appearance-none w-full sm:w-auto
                            bg-[#0f0f0f] border border-[#2a2a2a] rounded-lg
                            pl-3.5 pr-9 py-2 text-[13px]
                            text-[#c8c8c8] cursor-pointer outline-none
                            hover:border-[#C1121F] focus:border-[#C1121F]
                            transition-colors
                        "
                    >
                        <option value="">Type</option>
                        <option
                            v-for="option in props.carTypeOptions"
                            :key="option.id"
                            :value="option.id"
                        >
                            {{ option.label }}
                        </option>
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

                <!-- Condition filter -->
                <div class="relative flex-1 sm:flex-none">
                    <select
                        :value="props.selectedCondition"
                        @change="handleConditionChange"
                        class="
                            appearance-none w-full sm:w-auto
                            bg-[#0f0f0f] border border-[#2a2a2a] rounded-lg
                            pl-3.5 pr-9 py-2 text-[13px]
                            text-[#c8c8c8] cursor-pointer outline-none
                            hover:border-[#C1121F] focus:border-[#C1121F]
                            transition-colors
                        "
                    >
                        <option value="">Condition</option>
                        <option value="available">Operational</option>
                        <option value="maintenance">Maintenance</option>
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
                        <th class="px-5 py-3">Vehicle</th>
                        <th class="px-5 py-3">Type</th>
                        <th class="px-5 py-3">Price / Day</th>
                        <th class="px-5 py-3">Condition</th>
                        <th class="px-5 py-3">Rental Status</th>
                        <th class="px-5 py-3">Bookings</th>
                        <th class="px-5 py-3">Actions</th>
                    </tr>
                </thead>

                <tbody>
                    <tr
                        v-for="(car, i) in props.cars"
                        :key="car.car_id"
                        :class="
                            i !== props.cars.length - 1
                                ? 'border-b border-[#1c1c1c]'
                                : ''
                        "
                    >
                        <!-- Vehicle -->
                        <td class="px-5 py-3.5 text-sm text-[#e4e4e4]">
                            <div class="flex items-center gap-2.5">

                                <!-- Car image -->
                                <div
                                    v-if="car?.meta?.primary_image"
                                    class="
                                        w-10 h-8 rounded-md bg-[#2a2a2a]
                                        flex items-center justify-center
                                        flex-shrink-0 overflow-hidden
                                    "
                                >
                                    <img
                                        :src="car?.meta?.primary_image"
                                        :alt="`${car.brand} ${car.model}`"
                                        class="w-full h-full object-cover"
                                    />
                                </div>

                                <!-- Fallback -->
                                <div
                                    v-else
                                    class="
                                        w-10 h-8 rounded-md bg-[#2a2a2a]
                                        flex items-center justify-center
                                        flex-shrink-0
                                    "
                                >
                                    <svg
                                        class="w-5 h-5 text-[#8a8a8a]"
                                        viewBox="0 0 24 24"
                                        fill="none"
                                        stroke="currentColor"
                                        stroke-width="1.8"
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                    >
                                        <path d="M5 17h14" />
                                        <path d="M6 17l1.5-6h9L18 17" />
                                        <circle cx="8" cy="17" r="1.5" />
                                        <circle cx="16" cy="17" r="1.5" />
                                    </svg>
                                </div>

                                <div class="min-w-0">
                                    <div class="font-semibold text-white truncate">
                                        {{ car.brand }} {{ car.model }}
                                    </div>

                                    <div
                                        class="
                                            text-[#8a8a8a] text-[12.5px]
                                            truncate
                                        "
                                    >
                                        {{ car.year }} · {{ car.transmission }}
                                    </div>
                                </div>

                            </div>
                        </td>

                        <!-- Type -->
                        <td class="px-5 py-3.5 text-sm">
                            <span
                                class="
                                    text-xs px-2.5 py-1 rounded-md
                                    bg-[#232323] text-[#c8c8c8]
                                    inline-block whitespace-nowrap capitalize
                                "
                            >
                                {{ car.car_type }}
                            </span>
                        </td>

                        <!-- Price -->
                        <td
                            class="
                                px-5 py-3.5 text-sm
                                text-[#e4e4e4]
                                whitespace-nowrap
                            "
                        >
                            ₱{{ formatPrice(Number(car?.price_per_day)) }}
                        </td>

                        <!-- Condition -->
                        <td class="px-5 py-3.5 text-sm">
                            <span
                                class="
                                    flex items-center gap-[7px]
                                    text-[13px] whitespace-nowrap
                                "
                            >
                                <span
                                    class="w-[7px] h-[7px] rounded-full flex-shrink-0"
                                    :class="{
                                        'bg-[#3ddc78]':
                                            car.status === 'available',

                                        'bg-[#c81e2c]':
                                            car.status === 'maintenance'
                                    }"
                                ></span>

                                {{
                                    car.status === 'available'
                                        ? 'Operational'
                                        : 'Maintenance'
                                }}
                            </span>
                        </td>

                        <!-- Rental Status -->
                        <td class="px-5 py-3.5 text-sm">
                            <span
                                class="
                                    flex items-center gap-[7px]
                                    text-[13px] whitespace-nowrap
                                "
                            >
                                <span
                                    class="w-[7px] h-[7px] rounded-full flex-shrink-0"
                                    :class="{
                                        'bg-[#3ddc78]':
                                            getRentalStatus(car) === 'available',

                                        'bg-[#e6a23c]':
                                            getRentalStatus(car) === 'currently_rented'
                                    }"
                                ></span>

                                {{
                                    getRentalStatus(car) === 'currently_rented'
                                        ? 'Currently rented'
                                        : 'Available'
                                }}
                            </span>
                        </td>

                        <td class="px-5 py-3.5 text-sm">
                            {{ car.rental_count }}
                        </td>

                        <!-- Actions -->
                        <td class="px-5 py-3.5 text-sm">
                            <div class="flex items-center gap-1 text-[#8a8a8a]">

                                <button
                                    type="button"
                                    class="
                                        hover:border-[#c1121f] cursor-pointer
                                        hover:text-[#c1121f] inline-flex h-8 items-center 
                                        gap-1.5 rounded-lg border border-[#292929] 
                                        bg-[#151515] px-2.5 text-[11px] font-semibold 
                                        text-[#9b9b9b] transition-all
                                    "
                                    @click="$emit('edit', car)"
                                >
                                    <svg
                                        viewBox="0 0 24 24"
                                        fill="none"
                                        class="h-3.5 w-3.5"
                                        stroke="currentColor"
                                        stroke-width="2"
                                    >
                                        <path d="M12 20h9" />
                                        <path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z" />
                                    </svg>
                                    Edit
                                </button>

                                <button
                                    type="button"
                                    class="
                                        hover:border-[#c1121f] cursor-pointer
                                        hover:text-[#c1121f] inline-flex h-8 items-center 
                                        gap-1.5 rounded-lg border border-[#292929] 
                                        bg-[#151515] px-2.5 text-[11px] font-semibold 
                                        text-[#9b9b9b] transition-all
                                    "
                                    @click="$emit('status', car)"
                                >
                                    <svg
                                        viewBox="0 0 24 24"
                                        fill="none"
                                        class="h-3.5 w-3.5"
                                        stroke="currentColor"
                                        stroke-width="2"
                                    >
                                        <path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18v3h3l6.3-6.3a4 4 0 0 0 5.4-5.4l-2.1 2.1-2.4-.6-.6-2.4Z" />
                                        <path d="m17 3 4 4" />
                                    </svg>

                                    {{
                                        car.status === 'maintenance'
                                            ? 'Activate'
                                            : 'Maintenance'
                                    }}
                                </button>

                                <button
                                    type="button"
                                    class="
                                        hover:border-[#c1121f] cursor-pointer
                                        hover:text-[#c1121f] inline-flex h-8 items-center 
                                        gap-1.5 rounded-lg border border-[#292929] 
                                        bg-[#151515] px-2.5 text-[11px] font-semibold 
                                        text-[#9b9b9b] transition-all
                                    "
                                    @click="$emit('delete', car)"
                                >
                                    <svg
                                        viewBox="0 0 24 24"
                                        fill="none"
                                        class="h-3.5 w-3.5"
                                        stroke="currentColor"
                                        stroke-width="2"
                                    >
                                        <path d="M3 6h18" />
                                        <path d="M8 6V4h8v2" />
                                        <path d="M19 6l-1 14H6L5 6" />
                                        <path d="M10 11v5M14 11v5" />
                                    </svg>
                                    Delete
                                </button>

                            </div>
                        </td>
                    </tr>

                    <!-- Empty state -->
                    <tr v-if="props.cars.length === 0">
                        <td
                            colspan="7"
                            class="
                                px-5 py-10 text-center
                                text-sm text-[#8a8a8a]
                            "
                        >
                            No vehicles found.
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
                    props.cars.length
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
                of {{ props.count }} vehicles
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
import type { Car, CarTypeFilterOption } from '~/utils/api/api'

const props = defineProps<{
    cars: Car[]
    search: string
    currentPage: number
    count: number
    pageSize: number
    totalPages: number
    nextPage: string | null
    previousPage: string | null
    selectedCarType: number[]
    selectedCondition: string
    carTypeOptions: CarTypeFilterOption[]
}>()

const emit = defineEmits<{
    'update:search': [value: string]
    'update:page': [value: number]
    'update:selectedCarType': [value: number[]]
    'update:selectedCondition': [value: string]
    edit: [car: Car]
    status: [car: Car]
    delete: [car: Car]
}>()

const handleSearch = (event: Event) => {
    const target = event.target as HTMLInputElement
    emit('update:search', target.value)
}

const handleTypeChange = (event: Event) => {
    const value = (event.target as HTMLSelectElement).value
    const selected = value === '' ? [] : [Number(value)]
    emit('update:selectedCarType', selected)
}

const handleConditionChange = (event: Event) => {
    const target = event.target as HTMLSelectElement
    console.log('Condition changed:', target.value)
    emit('update:selectedCondition', target.value)
}

const formatPrice = (price: number) => {
    return price.toLocaleString('en-PH')
}

const getRentalStatus = (car: Car) => {
    const now = new Date()

    const currentRental = car.unavailable_periods?.some((period) => {
        const pickupDate = new Date(period.pickup_date)
        const returnDate = new Date(period.return_date)

        return (
            now >= pickupDate &&
            now <= returnDate &&
            ['pending_approval', 'confirmed', 'picked_up'].includes(
                period.status
            )
        )
    })

    return currentRental ? 'currently_rented' : 'available'
}

const getCarTypeName = (id: number | null) => {
    return props.carTypeOptions.find(type => type.id === id)?.label ?? 'Unknown'
}

</script>