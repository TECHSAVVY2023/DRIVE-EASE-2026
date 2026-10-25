import type { BookingForm } from "~/utils/types/booking"

interface CreateBookingResult {
    success: boolean
    message: string
}

export const useAdminTransactionEdit = () => {
    const { updateBooking, deleteBooking } = useAdminTransactions()
    const { $swal } = useNuxtApp()

    const validateForm = (form: BookingForm) => {
        if (!form.user) {
            return {
                success: false,
                message: 'Please select a user.',
            }
        }

        if (!form.car) {
            return {
                success: false,
                message: 'Please select a vehicle.',
            }
        }

        if (!form.status) {
            return {
                success: false,
                message: 'Please select a booking status.',
            }
        }

        if (!form.pickup_date) {
            return {
                success: false,
                message: 'Please select a pickup date.',
            }
        }

        if (!form.return_date) {
            return {
                success: false,
                message: 'Please select a return date.',
            }
        }

        if (!form.pickup_location.trim()) {
            return {
                success: false,
                message: 'Please enter a pickup location.',
            }
        }

        if (!form.return_location.trim()) {
            return {
                success: false,
                message: 'Please enter a return location.',
            }
        }

        return {
            success: true,
            message: '',
        }
    }
    
    const handleUpdateBooking = async (
        form: BookingForm
    ): Promise<CreateBookingResult> => {

        const validation = validateForm(form)

        if (!validation.success) {
            await $swal.fire({
                icon: 'warning',
                title: 'Incomplete Form',
                text: validation.message,
                background: '#1a1a1a',
                confirmButtonColor: '#C1121F',
                color: '#ffffff',
            })

            return {
                success: false,
                message: validation.message,
            }
        }

        $swal.fire({
            title: 'Saving changes...',
            text: 'Please wait.',
            background: '#1a1a1a',
            color: '#ffffff',
            allowOutsideClick: false,
            allowEscapeKey: false,
            didOpen: () => $swal.showLoading(),
        })

        try {
            if (!form.booking_reference) {
                throw new Error('Booking reference is missing.')
            }

            await updateBooking(
                form.booking_reference,
                form
            )

            $swal.close()

            await $swal.fire({
                icon: 'success',
                title: 'Success',
                text: 'Booking updated successfully.',
                confirmButtonColor: '#C1121F',
                background: '#1a1a1a',
                color: '#ffffff',
                allowOutsideClick: false,
                allowEscapeKey: false,
                scrollbarPadding: false,
            })

            return {
                success: true,
                message: 'Booking updated successfully.',
            }

        } catch (error) {
            console.error('Failed to update booking:', error)

            $swal.close()

            await $swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Failed to update booking.',
                confirmButtonColor: '#C1121F',
                background: '#1a1a1a',
                color: '#ffffff',
            })

            return {
                success: false,
                message: 'Failed to update booking.',
            }
        }
    }   

    const handleDeleteBooking = async (bookingId: string) => {
        try {
            await deleteBooking(bookingId)

            return { success: true }
        } catch (error) {
            console.error('Failed to delete booking:', error)

            return { success: false }
        }
    }

    return {
        handleUpdateBooking,
        handleDeleteBooking,
    }
}
