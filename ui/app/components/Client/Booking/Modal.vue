<template>
    <Transition name="fade">
        <div
            v-if="modelValue"
            class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/70 p-4"
            @click.self="$emit('update:modelValue', false)"
        >
            <Transition
                enter-active-class="transition-all duration-200"
                enter-from-class="opacity-0 scale-95"
                enter-to-class="opacity-100 scale-100"
                leave-active-class="transition-all duration-200"
                leave-from-class="opacity-100 scale-100"
                leave-to-class="opacity-0 scale-95"
            >
                <div class="h-full w-full flex items-center justify-center">
                    <div
                        v-if="modelValue"
                        class="
                            bg-[#111111] border-t-[#C1121F] border-t-5 rounded-xl 
                            w-full h-[90%] max-w-lg font-[poppins] flex flex-col
                        "
                    >
                        <!-- Header -->
                        <div class="px-6 pt-6 pb-4 flex-shrink-0">
                            <h2 class="text-white font-extrabold text-xl">Book this car</h2>
                            <p class="text-[#929292] text-xs mt-1">Complete all steps to confirm your reservation</p>
                        </div>

                        <ClientBookingSteps 
                            :current-step="currentStep"
                            :steps="steps"
                        />

                        <!-- Content -->
                        <div class="scroll-container w-[100%] pl-6 pr-5 py-6 flex flex-col gap-4 overflow-y-auto">

                            <!-- Car summary card -->
                            <div class="flex shrink-0 items-center gap-3 bg-[#1a1a1a] border border-[#C1121F] h-fit rounded-xl overflow-hidden">
                                <div class="flex-none w-24 h-full overflow-hidden">
                                    <img
                                        :src="`${car?.meta.primary_image}`"
                                        :alt="`${car?.brand} ${car?.model}`"
                                        class="object-cover w-full h-full"
                                    />
                                </div>

                                <div class="flex-1 min-w-0 py-2">
                                    <p class="text-white text-sm font-bold">
                                        {{ car?.brand }} {{ car?.model }}
                                    </p>
                                    <p class="text-gray-400 text-xs">
                                        ₱{{ car?.price_per_day }} / day
                                    </p>
                                </div>

                                <div class="pr-3 flex-shrink-0">
                                    <span
                                        class="flex items-center gap-1 text-[10px] font-semibold text-green-400 bg-green-500/10 border border-green-500/20 px-2 py-1 rounded-full"
                                    >
                                        <span class="w-1.5 h-1.5 rounded-full bg-green-400"></span>
                                        AVAILABLE
                                    </span>
                                </div>
                            </div>

                            <ClientBookingStepOne
                                v-if="currentStep === 1"
                                :form="form"
                                :user="user"
                                :existingIdImages="existingIdImages"
                                :uploadedIdFiles="uploadedIdFiles"
                                @file-change="handleIdChange"
                                @drop="handleIdDrop"
                                @remove-existing-id="removeExistingId"
                                @remove-uploaded-id="removeIdFile"
                            />

                            <ClientBookingStepTwo
                                v-if="currentStep === 2"
                                :form="form"
                            />

                            <!-- Step 3: Review & Confirm (placeholder) -->
                            <template v-else-if="currentStep === 3">
                                <div class="bg-[#1a1a1a] border border-[#222] rounded-xl p-4 flex flex-col gap-3 text-sm">
                                    <div class="flex justify-between">
                                        <span class="text-gray-400 text-xs">Name</span>
                                        <span class="text-white text-xs font-semibold">{{ form.firstName }} {{ form.lastName }}</span>
                                    </div>

                                    <div class="flex justify-between">
                                        <span class="text-gray-400 text-xs">Address</span>
                                        <span class="text-white text-xs font-semibold">{{ form.address }}</span>
                                    </div>

                                    <div class="flex justify-between">
                                        <span class="text-gray-400 text-xs">Contact</span>
                                        <span class="text-white text-xs font-semibold">{{ form.contact }}</span>
                                    </div>

                                    <div class="border-t border-[#222] pt-2 flex flex-col gap-2">
                                        <span class="text-gray-400 text-xs">Uploaded Valid IDs</span>

                                        <template v-if="existingIdImages.length">
                                            <div
                                                v-for="(url, index) in existingIdImages"
                                                :key="'id-' + index"
                                                class="flex items-center justify-between bg-[#0f0f0f] border border-white/10 rounded-lg px-3 py-2"
                                            >
                                                <div class="flex items-center gap-3">
                                                    <div class="w-8 h-8 flex items-center justify-center bg-[#1a1a1a] rounded">
                                                        <svg class="w-4 h-4 text-[#C1121F]" fill="currentColor" viewBox="0 0 24 24">
                                                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                                                        </svg>
                                                    </div>

                                                    <a
                                                        :href="url"
                                                        target="_blank"
                                                        class="text-white text-xs hover:text-[#C1121F] transition-colors"
                                                    >
                                                        Valid ID {{ index + 1 }}
                                                    </a>
                                                </div>

                                                <span class="text-[11px] text-green-400 font-medium">
                                                    Uploaded
                                                </span>
                                            </div>
                                        </template>

                                        <!-- Newly selected IDs -->
                                        <template v-if="uploadedIdFiles.length">
                                            <div
                                                v-for="(file, index) in uploadedIdFiles"
                                                :key="'uploaded-' + index"
                                                class="flex items-center justify-between bg-[#0f0f0f] border border-white/10 rounded-lg px-3 py-2"
                                            >
                                                <div class="flex items-center gap-3">
                                                    <div class="w-8 h-8 flex items-center justify-center bg-[#1a1a1a] rounded">
                                                        <svg class="w-4 h-4 text-[#C1121F]" fill="currentColor" viewBox="0 0 24 24">
                                                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                                                        </svg>
                                                    </div>

                                                    <div class="flex flex-col">
                                                        <p @click="openImage(file)" 
                                                            class="text-white text-xs truncate max-w-[100px] font-medium hover:text-[#c1121f] transition-colors cursor-pointer">
                                                            {{ file.name }}
                                                        </p>
                                                    </div>
                                                </div>

                                                <span class="text-[11px] text-green-400 font-medium">
                                                    Uploaded
                                                </span>

                                            </div>
                                        </template>
                                    </div>

                                    <div class="border-t border-[#222] pt-2 flex justify-between">
                                        <span class="text-gray-400 text-xs">Pickup date</span>
                                        <span class="text-white text-xs font-semibold">{{ form.pickupDate }}</span>
                                    </div>

                                    <div class="flex justify-between">
                                        <span class="text-gray-400 text-xs">Return date</span>
                                        <span class="text-white text-xs font-semibold">{{ form.returnDate }}</span>
                                    </div>

                                    <div class="flex justify-between">
                                        <span class="text-gray-400 text-xs">Location</span>
                                        <span class="text-white text-xs font-semibold">{{ form.location }}</span>
                                    </div>

                                    <div class="border-t border-[#222] pt-2 flex justify-between">
                                        <span class="text-gray-400 text-xs">Rental Duration</span>
                                        <span class="text-white text-xs font-semibold">{{ rentalDays }} day(s)</span>
                                    </div>

                                    <div class="flex justify-between">
                                        <span class="text-gray-400 text-xs">Rate per day</span>
                                        <span class="text-white text-xs font-semibold">₱{{ car?.price_per_day.toLocaleString() }}</span>
                                    </div>

                                    <div class="flex justify-between border-t border-[#222] pt-5">
                                        <span class="text-white text-[18px] font-semibold">Total Price</span>
                                        <span class="text-white text-[18px] font-bold">
                                            ₱{{ totalPrice.toLocaleString() }}
                                        </span>
                                    </div>
                                </div>
                            </template>

                        </div>

                        <div class="flex flex-col gap-2 mt-4 mb-8 mx-6">
                            <button
                                @click="currentStep === steps.length ? confirmBooking() : handleNext()"
                                :disabled="isSubmitting"
                                class="w-full bg-[#C1121F] hover:bg-red-700 disabled:opacity-50 text-white text-sm font-bold py-3 rounded-lg transition-colors duration-200"
                            >
                                {{
                                    isSubmitting
                                        ? 'Submitting...'
                                        : currentStep === steps.length
                                            ? 'Confirm Booking'
                                            : 'Next Step'
                                }}
                            </button>

                            <button
                                @click="closeModal"
                                class="w-full border border-[#2a2a2a] hover:border-white text-white text-sm font-semibold py-3 rounded-lg transition-colors duration-200"
                            >
                                Cancel
                            </button>
                        </div>

                    </div>
                </div>
            </Transition>
        </div>
    </Transition>
</template>

<script setup lang="ts">
import type { User } from '~/utils/api/api'
import type { Car } from '~/utils/api/api'
import { ref, reactive } from 'vue'

const { $swal } = useNuxtApp()
const { apiFetch } = useApiFetch()
const currentStep = ref<number>(1)

interface Step {
    title: string
    subtitle: string
}

const steps: Step[] = [
    { title: 'Your info', subtitle: '& ID' },
    { title: 'Schedule', subtitle: '& Location' },
    { title: 'Review', subtitle: '& Confirm' },
]

const props = defineProps<{
    modelValue: boolean
    car: Car | null
    user: User | null
}>()

const emit = defineEmits<{
    (e: 'update:modelValue', value: boolean): void
}>()

const form = reactive({
    userid: props.user?.id,
    carid: props.car?.car_id,
    firstName: '',
    lastName: '',
    email: '',
    address: '',
    contact: '',
    id_images: [] as string[],
    pickupDate: '',
    returnDate: '',
    location: '',
})

const {
    uploadedIdFiles,
    removeIdFile,
    removeExistingId,
    uploadIdFiles,

    existingIdImages,
    originalIdImages,

    handleIdChange,
    handleIdDrop,

    validateFile
} = useProfileUploads()

function openImage(file: File) {
    const url = URL.createObjectURL(file)
    window.open(url, '_blank')

    // Release the object URL after a short delay
    setTimeout(() => URL.revokeObjectURL(url), 1000)
}

const closeModal = () => {
    if (import.meta.client) {
        document.documentElement.style.overflow = 'hidden'
    }
    currentStep.value = 1
    emit('update:modelValue', false)
}

const rentalDays = computed(() => {
    if (!form.pickupDate || !form.returnDate) return 0

    const pickup = new Date(form.pickupDate)
    const dropoff = new Date(form.returnDate)

    const diff = dropoff.getTime() - pickup.getTime()

    return Math.ceil(diff / (1000 * 60 * 60 * 24))
})

const totalPrice = computed(() => {
    return rentalDays.value * Number(props.car?.price_per_day)
})

const { validateStepOne, validateStepTwo } = useBookingValidation()

async function handleNext(): Promise<void> {

    if (currentStep.value === 1) {
        const valid = await validateStepOne(
            form,
            existingIdImages.value,
            uploadedIdFiles.value
        )

        if (!valid) return
    }
    
    if (currentStep.value === 2) {
        const valid = await validateStepTwo(form)

        if (!valid) return
    }

    if (currentStep.value < steps.length) {
        currentStep.value++
    } else {

        emit('update:modelValue', false)
    }
}

const isSubmitting = ref(false)

async function confirmBooking(): Promise<void> {
    if (isSubmitting.value) return

    const result = await $swal.fire({
        title: 'Confirm booking?',
        text: 'Please review your booking details before submitting.',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Proceed to Payment',
        cancelButtonText: 'Cancel',
        confirmButtonColor: '#C1121F',
        background: '#1a1a1a',
        color: '#ffffff'
    })

    if (!result.isConfirmed) return

    isSubmitting.value = true

    try{
        const { updateUserProfile } = useBookingProfileUpdate()

        await updateUserProfile({
            user: props.user,
            form: form,
            uploadedIdFiles: uploadedIdFiles.value,
            existingIdImages: existingIdImages.value,
            originalIdImages: originalIdImages.value,
            validateFile: validateFile,
            uploadIdFiles: uploadIdFiles
        })

        // Create booking first (status = pending_payment)
        const bookingBody = {
            user: props.user?.id,
            car: props.car?.car_id,
            pickup_date: form.pickupDate,
            return_date: form.returnDate,
            location: form.location,
            daily_rate: props.car?.price_per_day,
            number_of_days: rentalDays.value,
            subtotal: totalPrice.value,
            discount: 0,
            total_price: totalPrice.value
        }

        const bookingRes = await apiFetch<{ message: string; booking_id: number; booking_reference: string }>('/bookings/create/', {
            method: 'POST',
            body: bookingBody
        })

        // Create PayMongo payment session with booking_id
        const paymentData = {
            amount: Math.round(totalPrice.value * 100), // PayMongo expects amount in cents
            description: `Car rental: ${props.car?.brand} ${props.car?.model} - Booking: ${bookingRes.booking_reference}`,
            currency: 'PHP',
            booking_id: bookingRes.booking_id
        }

        const paymentRes = await apiFetch<{ 
            checkout_url: string
            payment_intent_id: string 
        }>('/payments/create-paymongo-payment/', {
            method: 'POST',
            body: paymentData
        })

        // Redirect to PayMongo checkout
        if (paymentRes.checkout_url) {
            window.location.href = paymentRes.checkout_url
            return
        }

        console.log('form:', form)
        console.log('Booking submitted successfully:', bookingRes)
    }catch(error){
        console.error(error)
    }finally{
        isSubmitting.value = false
    }
}

watch(
    () => props.modelValue,
    (open) => {
        if (!open) {
            currentStep.value = 1

            uploadedIdFiles.value = []
            existingIdImages.value = []
            originalIdImages.value = []

            Object.assign(form, {
                firstName: '',
                lastName: '',
                email: '',
                contact: '',
                address: '',
                id_images: []
            })

            return
        }

        if (!props.user) return

        Object.assign(form, {
            firstName: props.user.given_name,
            lastName: props.user.family_name,
            email: props.user.email,
            contact: props.user.contact_number,
            address: props.user.address,
            id_images: props.user.id_images || []
        })

        const images = props.user.id_images?.images || []

        existingIdImages.value = [...images]
        originalIdImages.value = [...images]

    }
)

watch(
    () => props.modelValue,
    (open) => {
        if (!import.meta.client) return

        document.documentElement.style.overflow =
            open ? 'hidden' : ''
    },
    { immediate: true }
)
</script>

<style scoped>
    .fade-enter-active,
    .fade-leave-active {
    transition: opacity .2s ease;
    }

    .fade-enter-from,
    .fade-leave-to {
    opacity: 0;
    }
</style>