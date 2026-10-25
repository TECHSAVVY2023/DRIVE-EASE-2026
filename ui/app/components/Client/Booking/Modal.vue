<template>
    <Transition name="fade">
        <div
            v-if="modelValue"
            class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/70 p-0 sm:p-4"
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
                            w-full h-[90dvh] sm:h-[90%] max-h-[100dvh] sm:max-h-[90dvh]
                            max-w-lg font-[poppins] flex flex-col
                        "
                    >
                        <!-- Header -->
                        <div class="px-4 sm:px-6 pt-5 sm:pt-6 pb-4 flex-shrink-0">
                            <h2 class="text-white font-extrabold text-lg sm:text-xl">Book this car</h2>
                            <p class="text-[#929292] text-xs mt-1">Complete all steps to confirm your reservation</p>
                        </div>

                        <ClientBookingSteps 
                            :current-step="currentStep"
                            :steps="steps"
                        />

                        <!-- Content -->
                        <div class="scroll-container w-full px-4 sm:pl-6 sm:pr-5 py-4 sm:py-6 flex flex-col gap-4 overflow-y-auto">

                            <!-- Car summary card -->
                            <div class="flex shrink-0 items-center gap-3 bg-[#1a1a1a] border border-[#C1121F] h-fit rounded-xl overflow-hidden">
                                <div class="flex-none w-20 sm:w-24 self-stretch overflow-hidden">
                                    <img
                                        :src="`${car?.meta.primary_image}`"
                                        :alt="`${car?.brand} ${car?.model}`"
                                        class="object-cover w-full h-full"
                                    />
                                </div>

                                <div class="flex-1 min-w-0 py-2">
                                    <p class="text-white text-sm font-bold truncate">
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
                                v-if="currentStep === 2 && car"
                                :form="form"
                                :car="car"
                            />

                            <!-- Step 3: Review & Confirm (placeholder) -->
                            <template v-else-if="currentStep === 3">
                                <div class="bg-[#1a1a1a] border border-[#222] rounded-xl p-3 sm:p-4 flex flex-col gap-3 text-sm">
                                    <div class="flex justify-between gap-3">
                                        <span class="text-gray-400 text-xs flex-shrink-0">Name</span>
                                        <span class="text-white text-xs font-semibold text-right min-w-0 break-words">{{ form.firstName }} {{ form.lastName }}</span>
                                    </div>

                                    <div class="flex justify-between gap-3">
                                        <span class="text-gray-400 text-xs flex-shrink-0">Address</span>
                                        <span class="text-white text-xs font-semibold text-right min-w-0 break-words">{{ form.address }}</span>
                                    </div>

                                    <div class="flex justify-between gap-3">
                                        <span class="text-gray-400 text-xs flex-shrink-0">Contact</span>
                                        <span class="text-white text-xs font-semibold text-right min-w-0 break-words">{{ form.contact }}</span>
                                    </div>

                                    <div class="border-t border-[#222] pt-2 flex flex-col gap-2">
                                        <span class="text-gray-400 text-xs">Uploaded Valid IDs</span>

                                        <template v-if="existingIdImages.length">
                                            <div
                                                v-for="(url, index) in existingIdImages"
                                                :key="'id-' + index"
                                                class="flex items-center justify-between gap-3 bg-[#0f0f0f] border border-white/10 rounded-lg px-3 py-2"
                                            >
                                                <div class="flex items-center gap-3 min-w-0">
                                                    <div class="w-8 h-8 flex-shrink-0 flex items-center justify-center bg-[#1a1a1a] rounded">
                                                        <svg class="w-4 h-4 text-[#C1121F]" fill="currentColor" viewBox="0 0 24 24">
                                                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                                                        </svg>
                                                    </div>

                                                    <a
                                                        :href="url"
                                                        target="_blank"
                                                        class="text-white text-xs truncate hover:text-[#C1121F] transition-colors"
                                                    >
                                                        Valid ID {{ index + 1 }}
                                                    </a>
                                                </div>

                                                <span class="text-[11px] text-green-400 font-medium flex-shrink-0">
                                                    Uploaded
                                                </span>
                                            </div>
                                        </template>

                                        <!-- Newly selected IDs -->
                                        <template v-if="uploadedIdFiles.length">
                                            <div
                                                v-for="(file, index) in uploadedIdFiles"
                                                :key="'uploaded-' + index"
                                                class="flex items-center justify-between gap-3 bg-[#0f0f0f] border border-white/10 rounded-lg px-3 py-2"
                                            >
                                                <div class="flex items-center gap-3 min-w-0">
                                                    <div class="w-8 h-8 flex-shrink-0 flex items-center justify-center bg-[#1a1a1a] rounded">
                                                        <svg class="w-4 h-4 text-[#C1121F]" fill="currentColor" viewBox="0 0 24 24">
                                                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                                                        </svg>
                                                    </div>

                                                    <div class="flex flex-col min-w-0">
                                                        <p @click="openImage(file)" 
                                                            class="text-white text-xs truncate font-medium hover:text-[#c1121f] transition-colors cursor-pointer">
                                                            {{ file.name }}
                                                        </p>
                                                    </div>
                                                </div>

                                                <span class="text-[11px] text-green-400 font-medium flex-shrink-0">
                                                    Uploaded
                                                </span>

                                            </div>
                                        </template>
                                    </div>

                                    <div class="border-t border-[#222] pt-2 flex justify-between gap-3">
                                        <span class="text-gray-400 text-xs flex-shrink-0">Pickup date</span>
                                        <span class="text-white text-xs font-semibold text-right min-w-0 break-words">{{ formatDateTime(form.pickupDate) }}</span>
                                    </div>

                                    <div class="flex justify-between gap-3">
                                        <span class="text-gray-400 text-xs flex-shrink-0">Pickup Location</span>
                                        <span class="text-white text-xs font-semibold text-right min-w-0 break-words">{{ form.pickupLocation }}</span>
                                    </div>

                                    <div class="flex justify-between gap-3">
                                        <span class="text-gray-400 text-xs flex-shrink-0">Return date</span>
                                        <span class="text-white text-xs font-semibold text-right min-w-0 break-words">{{ formatDateTime(form.returnDate) }}</span>
                                    </div>

                                    <div class="flex justify-between gap-3">
                                        <span class="text-gray-400 text-xs flex-shrink-0">Return Location</span>
                                        <span class="text-white text-xs font-semibold text-right min-w-0 break-words">{{ form.returnLocation }}</span>
                                    </div>

                                    <div class="border-t border-[#222] pt-2 flex justify-between gap-3">
                                        <span class="text-gray-400 text-xs flex-shrink-0">Rental Duration</span>
                                        <span class="text-white text-xs font-semibold text-right">{{ rentalDays }} day(s)</span>
                                    </div>

                                    <div class="flex justify-between gap-3">
                                        <span class="text-gray-400 text-xs flex-shrink-0">Rate per day</span>
                                        <span class="text-white text-xs font-semibold text-right">₱{{ car?.price_per_day.toLocaleString() }}</span>
                                    </div>

                                    <div class="flex justify-between gap-3 border-t border-[#222] pt-5">
                                        <span class="text-white text-base sm:text-[18px] font-semibold">Total Price</span>
                                        <span class="text-white text-base sm:text-[18px] font-bold">
                                            ₱{{ totalPrice.toLocaleString() }}
                                        </span>
                                    </div>
                                </div>
                            </template>

                        </div>

                        <div class="flex flex-col gap-2 mt-4 mb-5 sm:mb-8 mx-4 sm:mx-6 flex-shrink-0">
                            <button
                                @click="currentStep === steps.length ? confirmBooking() : nextStep(form, existingIdImages, uploadedIdFiles)"
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
import type { User } from '~/utils/types/accounts'
import type { Car } from '~/utils/types/fleet'
import { steps } from '~/constants/client/bookingSteps'
import { ref, reactive } from 'vue'

const { $swal } = useNuxtApp()
const { apiFetch } = useApiFetch()
const currentStep = ref<number>(1)

const props = defineProps<{
    modelValue: boolean
    car: Car | null
    user: User | null
}>()

const emit = defineEmits<{
    (e: 'update:modelValue', value: boolean): void
}>()

const { form, closeModal, openImage } = useBookingForm(
    toRef(props, 'modelValue'),
    toRef(props, 'user'),
    toRef(props, 'car'),
    currentStep,
    () => emit('update:modelValue', false)
)

const { uploadedIdFiles, removeIdFile, removeExistingId, uploadIdFiles, existingIdImages,
originalIdImages, handleIdChange, handleIdDrop, validateFile } = useProfileUploads()

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

const { nextStep } = useBookingSteps( steps, currentStep, validateStepOne, validateStepTwo )

const isSubmitting = ref(false)

const formatDateTime = (date: string | Date) => {
    return new Date(date).toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    })
}

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

    try {
        const { updateUserProfile } = useBookingProfileUpdate()

        await updateUserProfile({
            user: props.user,
            form,
            uploadedIdFiles: uploadedIdFiles.value,
            existingIdImages: existingIdImages.value,
            originalIdImages: originalIdImages.value,
            validateFile,
            uploadIdFiles
        })

        const bookingRes = await apiFetch<{ message: string; booking_id: number; booking_reference: string }>('/bookings/create/', {
            method: 'POST',
            body: {
                user: props.user?.id,
                car: props.car?.car_id,
                pickup_date: form.pickupDate,
                return_date: form.returnDate,
                pickup_location: form.pickupLocation,
                return_location: form.returnLocation,
                daily_rate: props.car?.price_per_day,
                number_of_days: rentalDays.value,
                subtotal: totalPrice.value,
                discount: 0,
                total_price: totalPrice.value
            }
        })

        const paymentRes = await apiFetch<{ checkout_url: string; payment_intent_id: string }>('/payments/create-paymongo-payment/', {
            method: 'POST',
            body: {
                amount: Math.round(totalPrice.value * 100),
                description: `Car rental: ${props.car?.brand} ${props.car?.model} - Booking: ${bookingRes.booking_reference}`,
                currency: 'PHP',
                booking_id: bookingRes.booking_id
            }
        })

        if (paymentRes.checkout_url) window.location.href = paymentRes.checkout_url
    } catch (error) {
        console.error(error)
    } finally {
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

        console.log('step one user:', props.user.family_name)

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