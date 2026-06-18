<template>

    <Toast
        :message="toastMessage"
        :type="toastType"
        :visible="showToast"
    />

    <MobileDrawer
        :menu-open="menuOpen"
        @close-menu="closeMenu"
    />
    <Navbar
        :user="user"
        :is-logged-in="isLoggedIn"
        :menu-open="menuOpen"
        @toggle-menu="toggleMenu"
        @open-sidebar="handleOpenSidebar" 
        @close-sidebar="handleCloseSidebar"
    />

    <Messenger />

    <div class="h-fit bg-[#0D0D0D] font-[poppins]">

        <Banner 
            subtitle="We're here to help"
            title="Contact Us"
            :breadcrumbs="[
                { label: 'Home', to: '/' },
                { label: 'Contact' }
            ]"
        />

        <!-- =========================
                Main content
        ========================== -->
        <div class="max-w-5xl mx-auto px-6 py-10 grid grid-cols-1 md:grid-cols-5 gap-6">

            <ContactForm
                :form-data="formData"
                @submit="submitForm"
            />

            <!-- Right: Info Cards -->
            <div class="md:col-span-2 flex flex-col gap-4">

                <!-- Contact Information -->
                <div class="bg-[#1a1a1a] rounded-xl p-6 flex flex-col gap-4">
                    
                    <h3 class="text-white font-bold text-sm">Contact information</h3>

                    <div class="flex flex-col gap-3">

                        <div class="flex items-start gap-3">
                            <div class="w-8 h-8 bg-[#C1121F] rounded-md flex items-center justify-center flex-shrink-0">
                                <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                                </svg>
                            </div>
                            <div>
                                <p class="text-[#9E9E9E] text-xs">Phone</p>
                                <p class="text-white text-sm font-medium">0960 064 4095</p>
                            </div>
                        </div>

                        <div class="flex items-start gap-3">
                            <div class="w-8 h-8 bg-[#C1121F] rounded-md flex items-center justify-center flex-shrink-0">
                                <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                                </svg>
                            </div>
                            <div>
                                <p class="text-[#9E9E9E] text-xs">Email</p>
                                <p class="text-white text-sm font-medium">driveease.biz@gmail.com</p>
                            </div>
                        </div>
                        
                        <div class="flex items-start gap-3">
                            <div class="w-8 h-8 bg-[#C1121F] rounded-md flex items-center justify-center flex-shrink-0">
                                <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                                </svg>
                            </div>
                            <div>
                                <p class="text-[#9E9E9E] text-xs">Address</p>
                                <p class="text-white text-sm font-medium">
                                    Tipolo, Mandaue City, Philippines, 6014
                                </p>
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
                        <a href="https://www.facebook.com/drive.easee" class="w-9 h-9 rounded-lg bg-[#232323] hover:bg-[#C1121F] flex items-center justify-center transition-colors duration-200">
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
import moment from 'moment'

const loading = ref(false)
const success = ref<string | null>(null)
const error = ref<string | null>(null)
const showToast = ref(false)
const toastMessage = ref("")
const toastType = ref("success")

const serverIP = "http://127.0.0.1:8000"

const submitForm = async () => {
loading.value = true
success.value = null
error.value = null

try {
    await $fetch(`${serverIP}/api/driveease/contact/create/`, {
        method: "POST",
        body: formData.value,
    })

    await sendToGmail()

    toastMessage.value = "Message sent successfully!"
    toastType.value = "success"
    showToast.value = true

    formData.value.contact_id = "CID" + moment().valueOf()
    formData.value.firstname = ""
    formData.value.lastname = ""
    formData.value.contact_email = ""
    formData.value.contact_number = ""
    formData.value.message = ""

    setTimeout(() => {
        showToast.value = false
    }, 3000)
} catch (err) {
    console.error(err)

    toastMessage.value = "Failed to send message"
    toastType.value = "error"
    showToast.value = true

    setTimeout(() => {
        showToast.value = false
    }, 3000)
} finally {
    loading.value = false
}
}

const sendToGmail = async () => {
  try {
    await $fetch(`${serverIP}/api/driveease/contact/gmail-notif/`, {
      method: "POST",
      body: formData.value,
    })
  } catch (err) {
    console.error(err)
    throw err
  }
}

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

//Navbar + User Profile + Working login // Line 244-272 //
const { isLoggedIn } = useAuth()
const { apiFetch } = useApiFetch()

const user = ref<any>(null)

watch(isLoggedIn, async (val) => {
    if (val) {
        user.value = await apiFetch('/auth/me/')
    } else {
        user.value = null
    }
}, { immediate: true })

const formData = ref({
    contact_id: "CID" + moment().valueOf(),
    firstname: '',
    lastname: '',
    contact_email: '',
    contact_number: '',
    message: ''
})

const { 
    menuOpen,
    toggleMenu,
    closeMenu,
    handleCloseSidebar,
    handleOpenSidebar
} = useNavbar()

</script>