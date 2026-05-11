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

            <!-- User -->
            <button
                class="
                    flex items-center gap-2 max-w-[180px]
                    bg-[#0D0D0D] border border-[#3C3C3C] hover:border-[#C1121F]
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

                <!-- Dropdown -->
                <svg
                    class="w-4 h-4 text-gray-400 flex-shrink-0"
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
        </div>

    </header>
</template>

<script setup lang="ts">
    const emit = defineEmits<{
        (e: 'close-sidebar'): void
        (e: 'open-sidebar'): void
    }>()

    const handleCloseSidebar = (): void => {
        console.log('Close button clicked')
        emit('close-sidebar')
    }

    const handleOpenSidebar = (): void => {
        console.log('Menu button clicked')
        emit('open-sidebar')
    }
</script>