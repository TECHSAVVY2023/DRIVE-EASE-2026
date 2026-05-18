<template>
    <!-- Top Navbar -->
    <header
        class="
            w-full bg-black border-b border-[#1f1f1f] 
            px-4 py-4
            flex items-center justify-between 
            sm:px-6 lg:px-8
        "
    >

        <!-- Left Side -->
        <div class="flex items-center gap-3 min-w-0">

            <!-- Mobile Menu Button -->
            <button
                @click="handleOpenSidebar"
                class="
                    flex justify-center items-center text-white
                    w-10 h-10 rounded-lg border border-[#2a2a2a] 
                    md:hidden hover:border-[#C1121F] transition-colors duration-200
                "
            >
                <svg
                    class="w-5 h-5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M4 6h16M4 12h16M4 18h16"
                    />
                </svg>
            </button>

            <!-- Logo -->
            <div class="w-10 h-10 rounded-full overflow-hidden flex-shrink-0">
                <img
                    src="~/assets/images/logo.png"
                    alt="Logo"
                    class="w-full h-full object-cover"
                />
            </div>

        </div>

        <!-- Right Side -->
        <div class="flex items-center gap-2 sm:gap-4">

            <!-- User Dropdown Wrapper -->
            <div class="relative">

                <!-- User Button -->
                <button
                    @click="toggleDropdown"
                    class="
                        flex items-center gap-2 max-w-[180px]
                        bg-[#0D0D0D] border border-[#323232] hover:border-[#C1121F]
                        text-white text-sm
                        px-2 sm:px-4 py-2 rounded-full
                        transition-colors duration-200
                    "
                >

                    <!-- Avatar -->
                    <div
                        class="w-7 h-7 rounded-full bg-gray-500 flex items-center justify-center flex-shrink-0"
                    >
                        <svg
                            class="w-4 h-4 text-white"
                            fill="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"
                            />
                        </svg>
                    </div>

                    <!-- Name -->
                    <span class="hidden sm:block truncate">
                        Hi, Juber
                    </span>

                    <!-- Dropdown Arrow -->
                    <svg
                        class="w-4 h-4 text-gray-400 flex-shrink-0 transition-transform duration-200"
                        :class="{ 'rotate-180': isDropdownOpen }"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M19 9l-7 7-7-7"
                        />
                    </svg>

                </button>

                <!-- Dropdown Menu -->
                <div
                    v-if="isDropdownOpen"
                    class="
                        absolute right-0 mt-2 w-52 z-50
                        bg-[#0D0D0D] border border-[#323232] rounded-xl shadow-lg
                        overflow-hidden
                    "
                >

                    <!-- Profile -->
                    <button
                        class="
                            w-full flex items-center gap-3
                            px-4 py-3
                            text-sm text-white
                            hover:bg-[#1A1A1A]
                            transition-colors duration-200
                        "
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-white" fill="currentColor" stroke="currentColor" viewBox="0 0 640 640">
                            <path d="M320 312C386.3 312 440 258.3 440 192C440 125.7 386.3 72 320 72C253.7 72 200 125.7 200 192C200 258.3 253.7 312 320 312zM290.3 368C191.8 368 112 447.8 112 546.3C112 562.7 125.3 576 141.7 576L498.3 576C514.7 576 528 562.7 528 546.3C528 447.8 448.2 368 349.7 368L290.3 368z"/>
                        </svg>

                        <span>Profile</span>
                    </button>

                    <!-- Divider -->
                    <div class="border-t border-[#222222]"></div>

                    <!-- Logout -->
                    <button
                        class="
                            w-full px-4 py-3 flex items-center gap-3
                            text-sm text-red-400
                            hover:bg-[#1A1A1A]
                            transition-colors duration-200
                        "
                    >
                        <svg
                            class="w-5 h-5"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a2 2 0 01-2 2H6a2 2 0 01-2-2V7a2 2 0 012-2h5a2 2 0 012 2v1"
                            />
                        </svg>

                        <span>Logout</span>
                    </button>

                </div>
            </div>

        </div>

    </header>

</template>

<script setup lang="ts">
    import { ref } from 'vue'

    const emit = defineEmits<{
        (e: 'close-sidebar'): void
        (e: 'open-sidebar'): void
    }>()

    const handleOpenSidebar = (): void => {
        console.log('Menu button clicked')
        emit('open-sidebar')
    }

    const isDropdownOpen = ref(false)

    const toggleDropdown = (): void => {
        isDropdownOpen.value = !isDropdownOpen.value
    }
</script>