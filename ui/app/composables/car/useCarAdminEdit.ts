import type { CarForm, Car } from '~/utils/api/api'
import { uploadFile } from '~/utils/api/upload'

interface CreateCarResult {
    success: boolean
    message: string
}

export const useCarAdminEdit = () => {
    const { updateCar, deleteCar } = useCar()
    const { $swal } = useNuxtApp()

    const validateFile = async (file: File): Promise<boolean> => {
        const MAX_FILE_SIZE = 50 * 1024 * 1024
        const ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png']

        const extension = file.name.split('.').pop()?.toLowerCase()

        if (!extension || !ALLOWED_EXTENSIONS.includes(extension)) {
            await $swal.fire({
                icon: 'error',
                title: 'Invalid File',
                text: 'Only JPG and PNG images are allowed.',
                confirmButtonColor: '#C1121F',
                background: '#1a1a1a',
                color: '#ffffff',
            })
            return false
        }

        if (file.size > MAX_FILE_SIZE) {
            await $swal.fire({
                icon: 'error',
                title: 'File Too Large',
                text: 'Image size must not exceed 50 MB.',
                confirmButtonColor: '#C1121F',
                background: '#1a1a1a',
                color: '#ffffff',
            })
            return false
        }

        return true
    }

    const validateForm = (form: CarForm): CreateCarResult => {
        const requiredFields = [
            form.brand,
            form.model,
            form.year,
            form.car_type,
            form.price_per_day,
            form.transmission,
            form.engine,
            form.fuel_type,
            form.seats,
            form.features,
        ]

        const hasEmptyFields = requiredFields.some(
            value => value === null || value === undefined || value === ''
        )

        if (hasEmptyFields) {
            return {
                success: false,
                message: 'Please fill in all required vehicle details.',
            }
        }

        if (form.images.length === 0) {
            return {
                success: false,
                message: 'Please upload at least one vehicle image.',
            }
        }

        return {
            success: true,
            message: '',
        }
    }

    const handleUpdateVehicle = async (
        form: CarForm
    ): Promise<CreateCarResult> => {

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

        // Validate newly added image files only
        for (const image of form.images) {
            if (image.file && !(await validateFile(image.file))) {
                return {
                    success: false,
                    message: 'Failed to update vehicle.',
                }
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
            // Upload new images and preserve existing URLs
            const uploadedImages = await Promise.all(
                form.images.map(async image => {
                    if (image.file) {
                        const url = await uploadFile(image.file)

                        return {
                            previewUrl: image.url,
                            url,
                        }
                    }

                    return {
                        previewUrl: image.url,
                        url: image.url,
                    }
                })
            )

            // Resolve the selected thumbnail to its final URL
            const primaryImage =
                uploadedImages.find(
                    image => image.previewUrl === form.thumbnail_url
                )?.url ?? null

            // Include all existing and newly uploaded images
            const imageUrls = uploadedImages.map(image => image.url)

            const body = {
                brand: form.brand,
                model: form.model,
                year: form.year,
                car_type: form.car_type,
                price_per_day: form.price_per_day,
                transmission: form.transmission,
                engine: form.engine,
                fuel_type: form.fuel_type,
                seats: form.seats,
                note: form.note ?? '',
                features: form.features,
                status: form.status,
                meta: {
                    primary_image: primaryImage,
                    images: imageUrls,
                },
            }

            if (!form.id) {
                throw new Error('Car ID is missing.')
            }

            await updateCar(form.id, body)

            $swal.close()

            await $swal.fire({
                icon: 'success',
                title: 'Success',
                text: 'Vehicle updated successfully.',
                confirmButtonColor: '#C1121F',
                background: '#1a1a1a',
                color: '#ffffff',
                allowOutsideClick: false,
                allowEscapeKey: false,
                scrollbarPadding: false,
            })

            return {
                success: true,
                message: 'Vehicle updated successfully.',
            }

        } catch (error) {
            console.error('Failed to update vehicle:', error)

            $swal.close()

            await $swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Failed to update vehicle.',
                confirmButtonColor: '#C1121F',
                background: '#1a1a1a',
                color: '#ffffff',
            })

            return {
                success: false,
                message: 'Failed to update vehicle.',
            }
        }
    }

    const handleSecondaryAction = async (
        car: Car
    ): Promise<{ success: boolean }> => {
        const newStatus =
            car.status === 'maintenance'
                ? 'available'
                : 'maintenance'

        try {
            await updateCar(car.car_id, {
                status: newStatus,
            })

            return { success: true }
        } catch (error) {
            console.error('Failed to update car status:', error)

            return { success: false }
        }
    }

    const handleDeleteVehicle = async (car: Car) => {
        try {
            await deleteCar(car.car_id)

            return { success: true }
        } catch (error) {
            console.error('Failed to delete vehicle:', error)

            return { success: false }
        }
    }

    return {
        handleUpdateVehicle,
        handleSecondaryAction,
        handleDeleteVehicle,
    }
}