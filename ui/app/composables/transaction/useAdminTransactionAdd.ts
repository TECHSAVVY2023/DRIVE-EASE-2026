import type { BookingForm } from '~/utils/types/booking'

interface CreateBookingResult {
    success: boolean
    message: string
}

export const useAdminTransactionAdd = () => {
    const { createBooking } = useAdminTransactions()
    const { $swal } = useNuxtApp()

    const handleCreateBooking = async (
        form: BookingForm
    ): Promise<CreateBookingResult> => {

        $swal.fire({
            title: 'Creating booking...',
            text: 'Please wait.',
            background: '#1a1a1a',
            color: '#ffffff',
            allowOutsideClick: false,
            allowEscapeKey: false,
            didOpen: () => $swal.showLoading(),
        })

        try {
            await createBooking(form)

            $swal.close()

            await $swal.fire({
                icon: 'success',
                title: 'Success',
                text: 'Booking created successfully.',
                confirmButtonColor: '#C1121F',
                background: '#1a1a1a',
                color: '#ffffff',
                allowOutsideClick: false,
                allowEscapeKey: false,
                scrollbarPadding: false,
            })

            return {
                success: true,
                message: 'Booking created successfully.',
            }

        } catch (error) {
            console.error('Failed to create booking:', error)

            $swal.close()

            await $swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Failed to create booking.',
                confirmButtonColor: '#C1121F',
                background: '#1a1a1a',
                color: '#ffffff',
            })

            return {
                success: false,
                message: 'Failed to create booking.',
            }
        }
    }
    
    return {
        handleCreateBooking
    }
}
