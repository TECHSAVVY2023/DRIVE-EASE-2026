<template>

    <MobileDrawer
        :menu-open="menuOpen"
        @close-menu="closeMenu"
    />
    <Navbar
        :menu-open="menuOpen"
        @toggle-menu="toggleMenu"
    />

    <Banner2 />

    <div class="min-h-screen bg-[#0D0D0D] font-[poppins]">

        <!-- =========================
                Main content
        ========================== -->
        <div class="max-w-5xl mx-auto px-6 py-10 grid grid-cols-1 md:grid-cols-5 gap-6">

            <!-- Left: Contact Form -->
            <div class="md:col-span-3 bg-[#1a1a1a] rounded-xl p-6 flex flex-col gap-5">
                <div>
                <h2 class="text-white font-bold text-lg">How can we help you?</h2>
                <p class="text-[#9E9E9E] text-xs mt-1">Fill out the form below and our team will get back to you within 24 hours.</p>
                </div>

                <!-- Form -->
                <div class="flex flex-col gap-4">

                    <div class="grid grid-cols-2 gap-4">
                        <div class="flex flex-col gap-1.5">
                            <label class="text-[#9E9E9E] text-xs">First name</label>
                            <input
                                type="text"
                                placeholder="Juan"
                                class="
                                    bg-[#111111] border border-[#2a2a2a] rounded-lg 
                                    px-3 py-2.5 text-white text-sm placeholder-[#444] 
                                    focus:outline-none focus:border-[#C1121F] 
                                    transition-colors duration-200"
                            />
                        </div>

                        <div class="flex flex-col gap-1.5">
                            <label class="text-[#9E9E9E] text-xs">Last name</label>
                            <input
                                type="text"
                                placeholder="Dela Cruz"
                                class="
                                    bg-[#111111] border border-[#2a2a2a] rounded-lg 
                                    px-3 py-2.5 text-white text-sm placeholder-[#444] 
                                    focus:outline-none focus:border-[#C1121F] 
                                    transition-colors duration-200"
                            />
                        </div>

                    </div>

                    <div class="grid grid-cols-2 gap-4">

                        <div class="flex flex-col gap-1.5">
                            <label class="text-[#9E9E9E] text-xs">Email address</label>
                            <input
                                type="email"
                                placeholder="juan@email.com"
                                class="
                                    bg-[#111111] border border-[#2a2a2a] rounded-lg 
                                    px-3 py-2.5 text-white text-sm placeholder-[#444] 
                                    focus:outline-none focus:border-[#C1121F] 
                                    transition-colors duration-200"
                            />
                        </div>

                        <div class="flex flex-col gap-1.5">
                            <label class="text-[#9E9E9E] text-xs">Contact number</label>
                            <input
                                type="tel"
                                placeholder="+63 912 345 6789"
                                class="
                                    bg-[#111111] border border-[#2a2a2a] rounded-lg 
                                    px-3 py-2.5 text-white text-sm placeholder-[#444] 
                                    focus:outline-none focus:border-[#C1121F] 
                                    transition-colors duration-200"
                            />
                        </div>

                    </div>

                    <div class="flex flex-col gap-1.5">
                        <label class="text-[#9E9E9E] text-xs">Topic</label>
                        <input
                            type="text"
                            placeholder="e.g. Booking inquiry, Complaint, General question"
                            class="
                                bg-[#111111] border border-[#2a2a2a] rounded-lg 
                                px-3 py-2.5 text-white text-sm placeholder-[#444] 
                                focus:outline-none focus:border-[#C1121F] 
                                transition-colors duration-200"
                        />
                    </div>

                    <div class="flex flex-col gap-1.5">
                        <label class="text-[#9E9E9E] text-xs">Message</label>
                        <textarea
                            rows="5"
                            placeholder="Write your message here..."
                            class="
                                bg-[#111111] border border-[#2a2a2a] rounded-lg 
                                px-3 py-2.5 text-white text-sm placeholder-[#444] 
                                focus:outline-none focus:border-[#C1121F] 
                                transition-colors duration-200 resize-none"
                        ></textarea>
                    </div>

                    <button class="w-full bg-[#C1121F] hover:bg-red-700 text-white text-sm font-semibold py-3 rounded-lg transition-colors duration-200">
                        Send message
                    </button>

                </div>

            </div>

            <!-- Right: Info Cards -->
            <div class="md:col-span-2 flex flex-col gap-4">

                <!-- Contact Information -->
                <div class="bg-[#1a1a1a] rounded-xl p-6 flex flex-col gap-4">
                    
                    <h3 class="text-white font-bold text-sm">Contact information</h3>

                    <div class="flex flex-col gap-3">

                        <div class="flex items-start gap-3">
                            <div class="w-8 h-8 rounded-lg bg-[#C1121F]/20 flex items-center justify-center flex-shrink-0">
                                <svg class="w-4 h-4 text-[#C1121F]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                                </svg>
                            </div>
                            <div>
                                <p class="text-[#9E9E9E] text-xs">Phone</p>
                                <p class="text-white text-sm font-medium">+63 912 345 6789</p>
                            </div>
                        </div>

                        <div class="flex items-start gap-3">
                            <div class="w-8 h-8 rounded-lg bg-[#C1121F]/20 flex items-center justify-center flex-shrink-0">
                                <svg class="w-4 h-4 text-[#C1121F]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                                </svg>
                            </div>
                            <div>
                                <p class="text-[#9E9E9E] text-xs">Email</p>
                                <p class="text-white text-sm font-medium">drive-ease@gmail.com</p>
                            </div>
                        </div>
                        
                        <div class="flex items-start gap-3">
                            <div class="w-8 h-8 rounded-lg bg-[#C1121F]/20 flex items-center justify-center flex-shrink-0">
                                <svg class="w-4 h-4 text-[#C1121F]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                                </svg>
                            </div>
                            <div>
                                <p class="text-[#9E9E9E] text-xs">Address</p>
                                <p class="text-white text-sm font-medium">Cagayan De Oro City, Philippines</p>
                            </div>
                        </div>

                    </div>

                </div>

                <!-- Opening Hours -->
                <div class="bg-[#1a1a1a] rounded-xl p-6 flex flex-col gap-4">

                    <h3 class="text-white font-bold text-sm">Opening hours</h3>

                    <div class="flex flex-col gap-2">

                        <div v-for="(schedule, i) in hours" :key="i" class="flex items-center justify-between">
                            
                            <span class="text-[#9E9E9E] text-xs">{{ schedule.day }}</span>
                            <span class="text-white text-xs font-medium" :class="schedule.closed ? 'text-[#C1121F]' : ''">
                                {{ schedule.time }}
                            </span>

                        </div>
                    </div>

                </div>

                <!-- Follow Us -->
                <div class="bg-[#1a1a1a] rounded-xl p-6 flex flex-col gap-4">

                    <h3 class="text-white font-bold text-sm">Follow us</h3>

                    <div class="flex gap-3">

                        <!-- Facebook -->
                        <a href="#" class="w-9 h-9 rounded-lg bg-[#232323] hover:bg-[#C1121F] flex items-center justify-center transition-colors duration-200">
                        <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z"/>
                        </svg>
                        </a>

                        <!-- Instagram -->
                        <a href="#" class="w-9 h-9 rounded-lg bg-[#232323] hover:bg-[#C1121F] flex items-center justify-center transition-colors duration-200">
                        <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24">
                            <rect x="2" y="2" width="20" height="20" rx="5" ry="5" fill="none" stroke="currentColor" stroke-width="2"/>
                            <circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/>
                            <circle cx="17.5" cy="6.5" r="1" fill="currentColor"/>
                        </svg>
                        </a>

                        <!-- X / Twitter -->
                        <a href="#" class="w-9 h-9 rounded-lg bg-[#232323] hover:bg-[#C1121F] flex items-center justify-center transition-colors duration-200">
                        <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                        </svg>
                        </a>

                        <!-- TikTok -->
                        <a href="#" class="w-9 h-9 rounded-lg bg-[#232323] hover:bg-[#C1121F] flex items-center justify-center transition-colors duration-200">
                        <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1V9.01a6.33 6.33 0 00-.79-.05 6.34 6.34 0 00-6.34 6.34 6.34 6.34 0 006.34 6.34 6.34 6.34 0 006.33-6.34V8.69a8.18 8.18 0 004.78 1.52V6.76a4.85 4.85 0 01-1.01-.07z"/>
                        </svg>
                        </a>

                    </div>
                </div>

            </div>
            
        </div>

    </div>

    <Footer />
</template>

<script setup lang="ts">
import { ref } from 'vue'

type Hour = {
  day: string
  time: string
  closed?: boolean
}

const hours: Hour[] = [
  { day: 'Monday – Friday', time: '8:00 AM – 6:00 PM' },
  { day: 'Saturday', time: '9:00 AM – 5:00 PM' },
  { day: 'Sunday', time: 'Closed', closed: true },
]

const menuOpen = ref(false)

const toggleMenu = () => {
    menuOpen.value = !menuOpen.value
}

const closeMenu = () => {
    menuOpen.value = false
}
</script>