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
        :auth-ready="authReady"
        :is-logged-in="isLoggedIn"
        :menu-open="menuOpen"
        @toggle-menu="toggleMenu"
        @open-sidebar="handleOpenSidebar" 
        @close-sidebar="handleCloseSidebar"
    />

    <Messenger />

    <div class="charcoal-blueprint-surface h-fit font-[poppins]">

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

            <ClientContactUsContactForm
                v-if="contact"
                :contact="contact"
                :form-data="formData"
                @submit="submitForm"
            />

            <!-- Right: Info Cards -->
            <div class="md:col-span-2 flex flex-col gap-4">

                <ClientContactUsContactInfo
                    v-if="contact"
                    :contact="contact"
                />

                <ClientContactUsOpeningHours
                    v-if="contact"
                    :contact="contact"
                />

                <ClientContactUsSocialMedia
                    v-if="contact"
                    :contact="contact"
                />

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

const { $swal } = useNuxtApp()

const serverIP = "http://127.0.0.1:8000"

const submitForm = async () => {
    loading.value = true
    success.value = null
    error.value = null

    $swal.fire({
        title: 'Sending message...',
        text: 'Please wait.',
        allowOutsideClick: false,
        allowEscapeKey: false,
        background: '#1a1a1a',
        color: '#ffffff',
        heightAuto: false,
        didOpen: () => {
            $swal.showLoading()
        }
    })

    try {
        await $fetch(`${serverIP}/api/driveease/contact/create/`, {
            method: "POST",
            body: formData.value,
        })

        await sendToGmail()

        await $swal.fire({
            title: 'Success!',
            text: 'Message sent successfully!',
            icon: 'success',
            confirmButtonColor: '#C1121F',
            background: '#1a1a1a',
            color: '#ffffff',
            heightAuto: false
        })

        formData.value.contact_id = "CID" + moment().valueOf()
        formData.value.firstname = ""
        formData.value.lastname = ""
        formData.value.contact_email = ""
        formData.value.contact_number = ""
        formData.value.message = ""

    } catch (err) {
        console.error(err)

        await $swal.fire({
            title: 'Error',
            text: 'Failed to send message.',
            icon: 'error',
            confirmButtonColor: '#C1121F',
            background: '#1a1a1a',
            color: '#ffffff',
            heightAuto: false
        })

    } finally {
        loading.value = false
        $swal.close()
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
const { isLoggedIn, authReady } = useAuth()
const { user } = useCurrentUser()

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

const {
   loadContactPageContent,
   contact
} = useContactPageContentLoad()

onMounted(() => {
    loadContactPageContent()
})
</script>
