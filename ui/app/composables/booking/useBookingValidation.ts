import type { Car } from '~/utils/types/fleet'
import { hasBookingConflict } from '~/composables/car/useCarRental'

export function useBookingValidation() {
    const { $swal } = useNuxtApp()

    async function showError(text: string): Promise<void> {
        await $swal.fire({
            icon: 'error',
            title: 'Error',
            text,
            confirmButtonColor: '#C1121F',
            background: '#1a1a1a',
            color: '#ffffff'
        })
    }

    async function validateStepOne(
        form: any,
        existingIdImages: string[],
        uploadedIdFiles: File[]
    ): Promise<boolean> {
        const totalIds = existingIdImages.length + uploadedIdFiles.length

        if (!form.lastName) {
            await showError('Please provide your last name.')
            return false
        }

        if (!form.address) {
            await showError('Please provide your address.')
            return false
        }

        if (!form.contact) {
            await showError('Please provide your contact number.')
            return false
        }

        if (totalIds < 2) {
            await showError('Please upload two valid ID images (front and back) before continuing.')
            return false
        }

        if (totalIds > 5) {
            await showError('A maximum of 5 ID images is allowed.')
            return false
        }

        return true
    }

    async function validateStepTwo(form: any, car: Car | null): Promise<boolean> {
        if (!form.pickupDate) {
            await showError('Please select a pickup date.')
            return false
        }

        if (!form.returnDate) {
            await showError('Please select a return date.')
            return false
        }

        const pickupDate = new Date(form.pickupDate)
        const returnDate = new Date(form.returnDate)

        if (returnDate <= pickupDate) {
            await showError('Return time must be later than the pickup time.')
            return false
        }

        if (
            car && hasBookingConflict(
                pickupDate,
                returnDate,
                car.unavailable_periods ?? [],
                car.availability_buffer_minutes,
            )
        ) {
            await showError(
                'This time overlaps an existing booking or its one-hour turnover buffer. Please choose a different time.',
            )
            return false
        }

        if (!form.pickupLocation.trim()) {
            await showError('Please enter a pickup location.')
            return false
        }

        if (!form.returnLocation.trim()) {
            await showError('Please enter a return location.')
            return false
        }

        return true
    }

    return {
        validateStepOne,
        validateStepTwo
    }
}
