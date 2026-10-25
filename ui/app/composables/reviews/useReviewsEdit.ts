import type { Review, Review1 } from '~/utils/api/api'
import { uploadFile } from '~/utils/api/upload'

interface CreateReviewResult {
    success: boolean
    message: string
}

export function useReviewsEdit() {
    const { updateReview } = useReviews()
    const { $swal } = useNuxtApp()

    const existingImages = ref<string[]>([])
    const originalImages = ref<string[]>([])

    const prepareEditReview = (review: Review1) => {
        const images = [...(review.images || [])]
        originalImages.value = images
        existingImages.value = [...images]
    }

    const resetEditReview = () => {
        originalImages.value = []
        existingImages.value = []
    }


    const validateFile = async (file: File): Promise<boolean> => {
        const MAX_FILE_SIZE = 50 * 1024 * 1024
        const ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png']

        const extension = file.name.split('.').pop()?.toLowerCase()

        if (!extension || !ALLOWED_EXTENSIONS.includes(extension)) {
            $swal.close()
            await $swal.fire({
                icon: 'error',
                title: 'Invalid File',
                text: 'Only JPG and PNG images are allowed.',
                confirmButtonText: 'OK',
                confirmButtonColor: '#C1121F',
                background: '#1a1a1a',
                color: '#ffffff'
            })
            return false
        }

        console.log('file size:', file.size)

        if (file.size > MAX_FILE_SIZE) {
            $swal.close()
            await $swal.fire({
                icon: 'error',
                title: 'File Too Large',
                text: 'Image size must not exceed 50 MB.',
                confirmButtonText: 'OK',
                confirmButtonColor: '#C1121F',
                background: '#1a1a1a',
                color: '#ffffff'
            })
            return false
        }

        return true
    }
    
    const validateForm = (form: Review): CreateReviewResult => {
        const requiredFields = [
            form.rating,
        ]

        const hasEmptyFields = requiredFields.some(
            value => value === null || value === undefined || value === 0
        )

        if (hasEmptyFields) {
            return {
                success: false,
                message: 'Please at least select a rating.',
            }
        }

        return {
            success: true,
            message: '',
        }
    }

    const handleSubmitEditReview = async (
        form: Review,
        carId: string
    ): Promise<CreateReviewResult> => {
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

        // Identify images removed by the user
        const removedImages = originalImages.value.filter(
            url => !existingImages.value.includes(url)
        )

        // Validate newly uploaded files before showing the loading alert
        for (const image of form.images) {
            if (!image.file) continue

            if (!(await validateFile(image.file))) {
                return {
                    success: false,
                    message: 'Invalid file type or size.',
                }
            }
        }

        try {
            $swal.fire({
                title: 'Saving changes...',
                text: 'Please wait.',
                background: '#1a1a1a',
                color: '#ffffff',
                allowOutsideClick: false,
                allowEscapeKey: false,
                didOpen: () => {
                    $swal.showLoading()
                }
            })

            // Upload only newly added images
            const newImagesUrls: string[] = []

            for (const image of form.images) {
                // Skip existing images
                if (!image.file) continue

                const url = await uploadFile(image.file)
                newImagesUrls.push(url)
            }

            // Keep remaining existing images and append new uploads
            const imageUrls: string[] = [
                ...existingImages.value,
                ...newImagesUrls,
            ]

            const body: {
                rating: number
                review: string
                images: string[]
                deleted_images?: string[]
            } = {
                rating: form.rating,
                review: form.text,
                images: imageUrls,
            }

            if (removedImages.length > 0) {
                body.deleted_images = removedImages
            }

            await updateReview(
                carId,
                form.id,
                body
            )

            $swal.close()

            await $swal.fire({
                icon: 'success',
                title: 'Success',
                text: 'Review updated successfully.',
                confirmButtonColor: '#C1121F',
                background: '#1a1a1a',
                color: '#ffffff',
                allowOutsideClick: false,
                allowEscapeKey: false,
                scrollbarPadding: false,
            })

            return {
                success: true,
                message: 'Review updated successfully.',
             }

        } catch (err) {
            $swal.close()

            console.error('Failed to update review:', err)

            await $swal.fire({
                icon: 'error',
                title: 'Update Failed',
                text: 'Something went wrong while updating your review.',
                confirmButtonColor: '#C1121F',
                background: '#1a1a1a',
                color: '#ffffff',
            })

            return {
                success: false,
                message: 'Something went wrong while updating your review.',
            }
        }
    }

    return {
        handleSubmitEditReview,
        existingImages,
        prepareEditReview,
        resetEditReview,
    }

}
