<template>
    <div class="bg-[#111111] font-sans">

        <!-- =========================
             Mobile Drawer Menu
        ========================== -->
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
                <div class="w-64 h-full bg-[#111111] flex flex-col px-6 py-8">

                    <!-- Close Button + User -->
                    <div class="flex flex-col items-center mb-8">

                        <button
                            class="self-end text-white mb-6"
                            @click="menuOpen = false"
                        >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                class="w-6 h-6"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M6 18L18 6M6 6l12 12"
                                />
                            </svg>
                        </button>

                        <!-- User Icon -->
                        <div class="w-14 h-14 rounded-full bg-white flex items-center justify-center mb-2">
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                class="w-8 h-8 text-gray-700"
                                viewBox="0 0 24 24"
                                fill="currentColor"
                            >
                                <path
                                    d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"
                                />
                            </svg>
                        </div>

                        <span class="text-sm font-semibold text-white">
                            Login
                        </span>
                    </div>

                    <!-- Navigation -->
                    <div class="border-t border-[#2a2a2a] mb-4"></div>

                    <ul class="flex flex-col text-sm font-medium text-white">
                        <li>
                            <a
                                href="#"
                                class="block py-4 text-center border-b border-[#2a2a2a] hover:text-[#c1121f] transition-colors duration-200"
                            >
                                Home
                            </a>
                        </li>

                        <li>
                            <a
                                href="#"
                                class="block py-4 text-center border-b border-[#2a2a2a] hover:text-[#c1121f] transition-colors duration-200"
                            >
                                Fleet
                            </a>
                        </li>

                        <li>
                            <a
                                href="#"
                                class="block py-4 text-center border-b border-[#2a2a2a] hover:text-[#c1121f] transition-colors duration-200"
                            >
                                About
                            </a>
                        </li>

                        <li>
                            <a
                                href="#"
                                class="block py-4 text-center border-b border-[#2a2a2a] hover:text-[#c1121f] transition-colors duration-200"
                            >
                                Contacts
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </Transition>

        <!-- =========================
             Mobile Menu Backdrop
        ========================== -->
        <Transition
            enter-active-class="transition-opacity duration-300"
            enter-from-class="opacity-0"
            enter-to-class="opacity-100"
            leave-active-class="transition-opacity duration-300"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0"
        >
            <div
                v-if="menuOpen"
                class="fixed inset-0 z-40 bg-black/60 md:hidden"
                @click="menuOpen = false"
            ></div>
        </Transition>

        <!-- =========================
             Hero Section
        ========================== -->
        <section class="relative flex items-center min-h-[600px] overflow-hidden">

            <!-- Hero Content -->
            <div
                class="
                    relative z-10
                    flex flex-col justify-center items-center text-center
                    w-full px-12 py-16 pb-[55%]

                    md:w-1/2
                    md:items-start md:text-left
                    md:px-0 md:pb-16 md:pl-20

                    lg:pl-16
                    xl:pl-36
                "
            >
                <h1
                    class="
                        text-5xl sm:text-5xl md:text-4xl lg:text-6xl
                        font-[poppins] font-extrabold
                        leading-tight tracking-tight uppercase text-white
                    "
                >
                    Drive Smart<br />
                    Drive Easy
                </h1>

                <p class="mt-2 text-sm text-[#9E9E9E] font-[poppins]">
                    "Affordable. Reliable. Ready when you are."
                </p>

                <!-- CTA Buttons -->
                <div class="mt-12 flex gap-4">

                    <button
                        class="
                            px-8 py-4 rounded-[10px]
                            bg-[#C1121F] hover:bg-[#6B0A10]
                            text-sm text-white font-[poppins]
                            transition-colors duration-250
                        "
                    >
                        View cars
                    </button>

                    <button
                        class="
                            px-8 py-4 rounded-[10px]
                            border border-white
                            text-sm text-white font-[poppins]
                            hover:bg-white hover:text-[#C1121F]
                            transition-colors duration-200
                        "
                    >
                        Sign up
                    </button>
                </div>
            </div>

            <!-- =========================
                 Desktop Hero Image
            ========================== -->
            <div
                class="
                    absolute top-0 right-0
                    hidden md:block
                    h-full w-[35%]
                    bg-[#C1121F]
                    overflow-visible
                "
            >
                <img
                    src="~/assets/images/car1.png"
                    alt="Toyota Wigo"
                    class="
                        absolute top-1/2 -translate-y-1/2
                        md:-left-20 lg:-left-36
                        w-full scale-[1.3]
                        object-contain drop-shadow-2xl
                    "
                />
            </div>

            <!-- =========================
                 Mobile Hero Image
            ========================== -->
            <div class="absolute bottom-0 left-0 right-0 h-[50%] md:hidden">

                <!-- Red Background -->
                <div
                    class="
                        absolute bottom-0 left-0 right-0
                        h-[55%] bg-[#C1121F]
                    "
                ></div>

                <!-- Car Image -->
                <img
                    src="~/assets/images/car1.png"
                    alt="Toyota Wigo"
                    class="
                        absolute bottom-2 left-1/2
                        w-[75%] -translate-x-1/2
                        object-contain drop-shadow-2xl z-10
                    "
                />
            </div>
        </section>
    </div>
</template>

<script setup>
import { ref } from 'vue'

/* =========================
   Mobile Drawer State
========================= */
const menuOpen = ref(false)

const toggleMenu = () => {
    menuOpen.value = !menuOpen.value
}
</script>