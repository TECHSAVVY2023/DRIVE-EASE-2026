<template>
    <div class="bg-[#111111] font-sans">

        <!-- Drawer Panel -->
        <Transition
            enter-active-class="transition-transform duration-300 ease-out"
            enter-from-class="-translate-x-full"
            enter-to-class="translate-x-0"
            leave-active-class="transition-transform duration-300 ease-in"
            leave-from-class="translate-x-0"
            leave-to-class="-translate-x-full"
        >

        <div
            v-if="menuOpen"
            class="fixed inset-0 z-50 flex md:hidden"
        >
            <!-- Drawer Panel -->
            <div class="w-64 bg-[#111111] h-full flex flex-col py-8 px-6">
                <!-- Close + Login -->
                <div class="flex flex-col items-center mb-8">
                    <button class="self-end text-white mb-6" @click="menuOpen = false">
                        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                    <!-- User icon -->
                    <div class="w-14 h-14 rounded-full bg-white flex items-center justify-center mb-2">
                        <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-gray-700" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>
                        </svg>
                    </div>
                    <span class="text-white text-sm font-semibold">Login</span>
                </div>

                <!-- Divider -->
                <div class="border-t border-[#2a2a2a] mb-4"></div>

                <!-- Nav Links -->
                <ul class="flex flex-col text-white text-sm font-medium">
                    <li><a href="#" class="block py-4 border-b border-[#2a2a2a] text-center hover:text-[#c1121f] transition-colors duration-200">Home</a></li>
                    <li><a href="#" class="block py-4 border-b border-[#2a2a2a] text-center hover:text-[#c1121f] transition-colors duration-200">Fleet</a></li>
                    <li><a href="#" class="block py-4 border-b border-[#2a2a2a] text-center hover:text-[#c1121f] transition-colors duration-200">About</a></li>
                    <li><a href="#" class="block py-4 border-b border-[#2a2a2a] text-center hover:text-[#c1121f] transition-colors duration-200">Contacts</a></li>
                </ul>
            </div>

        </div>
        </Transition>

        <!-- Backdrop -->
        <Transition
            enter-active-class="transition-opacity duration-300"
            enter-from-class="opacity-0"
            enter-to-class="opacity-100"
            leave-active-class="transition-opacity duration-300"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0"
        >
            <div v-if="menuOpen" class="fixed inset-0 z-40 bg-black/60 md:hidden" @click="menuOpen = false"></div>
        </Transition>

        <!-- Hero Section -->
        <section class="relative flex items-center min-h-[600px] overflow-hidden">
            <!-- Left: Text Content -->
            <div class="
                relative z-10
                flex flex-col justify-center items-center text-center
                w-full px-12 pb-[55%] py-16
                md:items-start md:text-left md:px-0
                md:w-1/2 md:pb-16 md:pl-20
                lg:pl-16 xl:pl-36">
                
                <h1 class="
                    text-white text-5xl font-[poppins]
                    sm:text-5xl md:text-4xl lg:text-6xl
                    font-extrabold leading-tight tracking-tight uppercase">
                        Drive Smart<br />Drive Easy
                </h1>
                <p class="mt-2 text-gray-400 text-sm font-[poppins]">
                    "Affordable. Reliable. Ready when you are."
                </p>
                <div class="mt-12 flex gap-4">
                <button class="
                    bg-[#C1121F] hover:bg-[#6B0A10]  font-[poppins]
                    text-white text-sm px-6 py-3 rounded-[10px] transition-colors duration-200">
                    View cars
                </button>
                <button class="
                    border border-white font-[poppins]
                    text-white text-sm
                    px-6 py-3 
                    rounded-[10px] hover:bg-white hover:text-[#C1121F] transition-colors duration-200"
                >
                    Sign up
                </button>
                </div>
            </div>

            <!-- Right: Red background block + Car Image (desktop only) -->
            <div class="absolute right-0 top-0 h-full w-[35%] bg-[#C1121F] hidden md:block overflow-visible">
                <img
                src="~/assets/images/car1.png"
                alt="Toyota Wigo"
                class="
                    absolute top-1/2 -translate-y-1/2 lg:-left-36 md:-left-20
                    w-full scale-[1.3] object-contain drop-shadow-2xl"
                />
            </div>

            <!-- Mobile: Car + Red block (stacked below text) -->
            <div class="md:hidden absolute bottom-0 left-0 right-0 h-[50%]">
                <!-- Red background strip -->
                <div class="absolute bottom-0 left-0 right-0 h-[55%] bg-[#C1121F]"></div>
                <!-- Car image -->
                <img
                    src="~/assets/images/car1.png"
                    alt="Toyota Wigo"
                    class="
                        absolute bottom-2 left-1/2 -translate-x-1/2 w-[75%] 
                        object-contain drop-shadow-2xl z-10"
                />
            </div>
        </section>

    </div>
</template>

<script setup>
import { ref } from 'vue'

    const menuOpen = ref(false)

    const toggleMenu = () => {
        menuOpen.value = !menuOpen.value
    }
</script>