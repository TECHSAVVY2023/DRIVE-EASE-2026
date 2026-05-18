<template>
    <!-- Sidebar -->
    <aside
        :class="[
            'fixed top-0 left-0 z-50 h-screen w-80 md:static sm:w-80 md:w-56 bg-[#1B1B1B] border-r border-[#1f1f1f] flex flex-col transition-transform duration-300',
            sidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
        ]"
    >

        <!-- Nav -->
        <nav 
            class="
                flex flex-col flex-1
                px-3 py-6
                gap-1
                text-xs
                overflow-y-auto
            "
        >

            <!-- Mobile Close Button -->
            <div class="flex items-center justify-between md:hidden px-4 py-2">

                <p class="text-white text-lg font-semibold">Menu</p>

                <button
                    @click="$emit('close-sidebar')"
                    class="
                        w-fit p-2
                        flex items-center justify-center
                        rounded-md
                        text-white hover:text-white
                        transition-colors duration-200
                    "
                >
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>

            <!-- Active -->
            <a href="#" 
                class="
                    flex items-center gap-3 mb-4
                    px-4 py-3 md:py-2.5
                    rounded-lg
                    text-white
                    bg-[#C1121F]
                    font-semibold
                "
            >
                <svg
                    class="w-5 h-5 md:w-4 md:h-4 flex-shrink-0"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                >

                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
                    />

                </svg>

                <span>Dashboard</span>
            </a>

            <!-- Section -->
            <p class="text-[#444] uppercase font-bold text-[10px] px-4 mb-1">
                Main
            </p>

                <!-- Item -->
                <a
                    href="#"
                    class="
                        flex items-center justify-between gap-2
                        px-3 py-3 rounded-lg
                        md:py-2.5 text-gray-400
                        hover:text-white hover:bg-[#232323]
                        transition-colors duration-200
                    "
                >
                    <div class="flex items-center gap-3 min-w-0">
                        <svg
                            class="w-5 h-5 md:w-4 md:h-4 flex-shrink-0"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
                            />
                        </svg>

                        <span class="truncate">
                            Notifications
                        </span>
                    </div>

                    <span
                        class="
                            bg-[#C1121F]
                            text-white
                            text-[9px]
                            font-bold
                            px-1.5 py-0.5
                            rounded-full
                            flex-shrink-0
                        "
                    >
                        67
                    </span>
                </a>

                <!-- Other Items -->
                <a
                    href="#"
                    class="
                        flex items-center gap-3
                        px-3 py-3 md:py-2.5
                        rounded-lg
                        text-gray-400
                        hover:text-white
                        hover:bg-[#232323]
                        transition-colors duration-200
                    "
                >
                    <svg
                        class="w-5 h-5 md:w-4 md:h-4 flex-shrink-0"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                        />
                    </svg>

                    Rental
                </a>

                <a
                    href="#"
                    class="
                        flex items-center gap-3
                        px-3 py-3 md:py-2.5
                        rounded-lg
                        text-gray-400
                        hover:text-white
                        hover:bg-[#232323]
                        transition-colors duration-200
                    "
                >
                    <svg
                        class="w-5 h-5 md:w-4 md:h-4 flex-shrink-0"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M13 10V3L4 14h7v7l9-11h-7z"
                        />
                    </svg>

                    Fleet
                </a>

                <a
                    href="#"
                    class="
                        flex items-center gap-3
                        px-3 py-3 md:py-2.5
                        rounded-lg
                        text-gray-400
                        hover:text-white
                        hover:bg-[#232323]
                        transition-colors duration-200
                    "
                >
                    <svg
                        class="w-5 h-5 md:w-4 md:h-4 flex-shrink-0"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0"
                        />
                    </svg>

                    Users
                </a>

                <!-- Report -->
                <p class="text-[#444] uppercase font-bold text-[10px] px-2 mb-1 mt-5">
                    Report
                </p>

                <a
                    href="#"
                    class="
                        flex items-center gap-3
                        px-3 py-3 md:py-2.5
                        rounded-lg
                        text-gray-400
                        hover:text-white
                        hover:bg-[#232323]
                        transition-colors duration-200
                    "
                >
                    <svg
                        class="w-5 h-5 md:w-4 md:h-4 flex-shrink-0"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                        />
                    </svg>

                    Analytics
                </a>

                <a
                    href="#"
                    class="
                        flex items-center gap-3
                        px-3 py-3 md:py-2.5
                        rounded-lg
                        text-gray-400
                        hover:text-white
                        hover:bg-[#232323]
                        transition-colors duration-200
                    "
                >
                    <svg
                        class="w-5 h-5 md:w-4 md:h-4 flex-shrink-0"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0"
                        />
                    </svg>

                    Activity logs
                </a>

        </nav>

    </aside>
</template>

<script setup lang="ts">
defineProps<{
    sidebarOpen: boolean
}>()

defineEmits<{
    (e: 'close-sidebar'): void
}>()
</script>
