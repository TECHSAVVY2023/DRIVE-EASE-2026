import { watch } from 'vue'
import type { User, Car } from '~/utils/api/api'
import Swal from 'sweetalert2'
import { useRouter } from 'vue-router'

export function useBookingForm(
    modelValue: Ref<boolean>,
    user: Ref<User | null>,
    car: Ref<Car | null>,
    currentStep: Ref<number>,
    close: () => void
) {

    const router = useRouter()
    
    const form = reactive({
        userid: user.value?.id,
        carid: car.value?.car_id,
        firstName: '',
        lastName: '',
        email: '',
        address: '',
        contact: '',
        id_images: [] as string[],
        pickupDate: '',
        returnDate: '',
        pickupLocation: '',
        returnLocation: '',
    })

    function openImage(file: File) {
        const url = URL.createObjectURL(file)
        window.open(url, '_blank')

        // Release the object URL after a short delay
        setTimeout(() => URL.revokeObjectURL(url), 1000)
    }

    function closeModal() {
        if (import.meta.client) {
            document.documentElement.style.overflow = ''
        }

        currentStep.value = 1
        close()
    }

    function resetBookingForm() {

    }

    function loadUserProfile() {

    }


    async function handleBook() {
        if (!user.value) {
            const result = await Swal.fire({
                icon: 'warning',
                title: 'Login Required',
                text: 'You need to log in before booking a vehicle.',
                showCancelButton: true,
                confirmButtonText: 'Login',
                cancelButtonText: 'Cancel',
                confirmButtonColor: '#C1121F',
            })

            if (result.isConfirmed) {
                router.push('/client/login')
            }

            return
        }

        open()
    }


    watch(modelValue, (open) => {
        if (!open) {
            resetBookingForm()
            return
        }

        loadUserProfile()
    })

    return {
        form,
        resetBookingForm,
        loadUserProfile,
        closeModal,
        openImage,
        handleBook
    }
}