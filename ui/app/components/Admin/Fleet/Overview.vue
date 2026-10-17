<template>
    <div class="grid grid-cols-1 lg:grid-cols-[1.5fr_1fr] gap-[18px] mb-[26px]">

        <!-- Fleet availability -->
        <div class="bg-[#161616] border border-[#232323] rounded-xl p-4 sm:p-5">

            <div class="flex justify-between items-start mb-5 sm:mb-6">
                <div>
                    <h3 class="text-base font-bold text-white">
                        Fleet availability
                    </h3>

                    <p class="text-[#777] text-[12px] mt-1">
                        Current vehicle status
                    </p>
                </div>

                <span
                    class="
                        text-[11px] text-[#3ddc78] bg-[#17301f]
                        px-2.5 py-1 rounded-md whitespace-nowrap
                    "
                >
                    Live
                </span>
            </div>

            <div class="flex flex-col sm:flex-row items-center gap-6 sm:gap-7">

                <!-- Donut -->
                <div
                    class="
                        relative
                        w-[110px] h-[110px]
                        sm:w-[120px] sm:h-[120px]
                        rounded-full
                        flex items-center justify-center
                        flex-shrink-0
                    "
                    :style="props.availabilityRing"
                >
                    <div
                        class="
                            w-[76px] h-[76px]
                            sm:w-[82px] sm:h-[82px]
                            rounded-full
                            bg-[#161616]
                            flex flex-col
                            items-center justify-center
                        "
                    >
                        <span class="text-[20px] sm:text-[22px] font-extrabold text-white">
                            {{ props.availablePercentage }}%
                        </span>

                        <span class="text-[10px] text-[#777]">
                            available
                        </span>
                    </div>
                </div>

                <!-- Legend -->
                <div class="w-full flex-1 space-y-3.5 sm:space-y-4">
                    <div
                        v-for="item in props.availability"
                        :key="item.label"
                        class="flex items-center justify-between gap-4"
                    >
                        <div class="flex items-center gap-2 min-w-0">
                            <span
                                class="w-2 h-2 rounded-full flex-shrink-0"
                                :class="item.dot"
                            ></span>

                            <span class="text-[13px] text-[#bcbcbc] truncate">
                                {{ item.label }}
                            </span>
                        </div>

                        <span class="text-[13px] font-semibold text-white flex-shrink-0">
                            {{ item.value }}
                        </span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Fleet health -->
        <div class="bg-[#161616] border border-[#232323] rounded-xl p-4 sm:p-5">

            <div class="flex justify-between items-start mb-5">
                <div>
                    <h3 class="text-base font-bold text-white">
                        Fleet health
                    </h3>

                    <p class="text-[#777] text-[12px] mt-1">
                        Current vehicle condition
                    </p>
                </div>

                <div
                    class="
                        w-9 h-9
                        rounded-lg
                        bg-[#17301f]
                        flex items-center justify-center
                        flex-shrink-0
                    "
                >
                    <svg
                        viewBox="0 0 24 24"
                        class="w-[18px] h-[18px] text-[#3ddc78]"
                        stroke="currentColor"
                        fill="none"
                        stroke-width="1.8"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                    >
                        <path
                            d="M12 3 21 7v5c0 5-3.5 8.5-9 10-5.5-1.5-9-5-9-10V7l9-4z"
                        />
                        <path d="m8.5 12 2.3 2.3 4.7-5" />
                    </svg>
                </div>
            </div>

            <div class="space-y-5">

                <!-- Fleet condition -->
                <div>
                    <div class="flex justify-between items-center text-[12px] mb-2">
                        <span class="text-[#999]">
                            Fleet condition
                        </span>

                        <span class="font-semibold text-white">
                            {{ props.fleetCondition }}%
                        </span>
                    </div>

                    <div class="h-1.5 bg-[#252525] rounded-full overflow-hidden">
                        <div
                            class="h-full bg-[#3ddc78] rounded-full transition-all duration-500"
                            :style="{
                                width: `${props.fleetCondition}%`
                            }"
                        ></div>
                    </div>
                </div>

                <!-- Health summary -->
                <div class="grid grid-cols-2 gap-3">

                    <!-- Healthy -->
                    <div class="bg-[#1b241e] border border-[#25362a] rounded-lg p-3">
                        <div class="flex items-center gap-2 mb-1.5">
                            <span class="w-2 h-2 rounded-full bg-[#3ddc78]"></span>

                            <span class="text-[11px] text-[#888]">
                                Healthy
                            </span>
                        </div>

                        <span class="text-lg font-bold text-white">
                            {{ props.healthyCount }}
                        </span>

                        <span class="text-[11px] text-[#777] ml-1">
                            vehicles
                        </span>
                    </div>

                    <!-- Maintenance -->
                    <div class="bg-[#252119] border border-[#393124] rounded-lg p-3">
                        <div class="flex items-center gap-2 mb-1.5">
                            <span class="w-2 h-2 rounded-full bg-[#e0a83e]"></span>

                            <span class="text-[11px] text-[#888]">
                                Maintenance
                            </span>
                        </div>

                        <span class="text-lg font-bold text-white">
                            {{ props.maintenanceCount }}
                        </span>

                        <span class="text-[11px] text-[#777] ml-1">
                            vehicles
                        </span>
                    </div>

                </div>

            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { CSSProperties } from 'vue'

interface AvailabilityItem {
    label: string
    value: number
    dot: string
}

const props = defineProps<{
    availablePercentage: number
    availability: AvailabilityItem[]
    availabilityRing: CSSProperties
    fleetCondition: number
    healthyCount: number
    maintenanceCount: number
}>()
</script>