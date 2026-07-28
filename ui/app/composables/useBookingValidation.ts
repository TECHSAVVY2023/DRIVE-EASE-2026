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

        if (totalIds > 6) {
            await showError('A maximum of 6 ID images is allowed.')
            return false
        }

        return true
    }

    async function validateStepTwo(form: any): Promise<boolean> {
        if (!form.pickupDate) {
            await showError('Please select a pickup date.')
            return false
        }

        if (!form.returnDate) {
            await showError('Please select a return date.')
            return false
        }

        if (!form.location.trim()) {
            await showError('Please enter a pickup location.')
            return false
        }

        return true
    }

    return {
        validateStepOne,
        validateStepTwo
    }
}