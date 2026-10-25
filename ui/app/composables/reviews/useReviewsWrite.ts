
import type { Review } from '~/utils/api/api'
import { uploadFile } from '~/utils/api/upload'

interface CreateReviewResult {
    success: boolean
    message: string
}

export function useReviewsWrite() {
    const { createReview } = useReviews()
    const { $swal } = useNuxtApp()

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

    const handleSubmitReview = async ( form: Review, carId: string ): Promise<CreateReviewResult> => {
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
            const uploadedImages = await Promise.all(
                form.images.map(async image => {
                    if (!image.file) {
                        throw new Error('Image file is missing.')
                    }

                    const url = await uploadFile(image.file)

                    return {
                        url,
                    }
                })
            )

            const imageUrls = uploadedImages.map(image => image.url)

            let body: any = {}
            
            if (imageUrls.length > 0) {
                body = {
                    rating: form.rating,
                    comment: form.text,
                    images: imageUrls
                }
            } else {
                body = {
                    rating: form.rating,
                    comment: form.text
                }
            }

            await createReview(carId, body)

            $swal.close()

            await $swal.fire({
                icon: 'success',
                title: 'Success',
                text: 'Review Submitted successfully. Wait for approval.',
                confirmButtonColor: '#C1121F',
                background: '#1a1a1a',
                color: '#ffffff',
                allowOutsideClick: false,
                allowEscapeKey: false,
                scrollbarPadding: false,
            })

            return {
                success: true,
                message: 'Review Submitted successfully. Wait for approval.',
            }

        } catch (error) {
            console.error('Failed to create review:', error)

            $swal.close()

            await $swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Failed to submit review.',
                confirmButtonColor: '#C1121F',
                background: '#1a1a1a',
                color: '#ffffff',
            })

            return {
                success: false,
                message: 'Failed to submit review.',
            }
        }
    }
    
    return {
        handleSubmitReview,
    }
}
