import { type AdminReview } from '~/utils/api/api'

export const useAdminReviewEdit = () => {
    const { updateReviewStatus, deleteAdminReview } = useAdminReview()

    const handleStatus = async (
        review: AdminReview,
        newStatus: 'approved' | 'rejected'
    ) => {
        try {
            await updateReviewStatus(review.id, newStatus)

            return { success: true }
        } catch (error) {
            console.error('Failed to update review status:', error)

            return { success: false }
        }
    }

    const handleDeleteReview = async (review: AdminReview) => {
        try {
            await deleteAdminReview(review.id)

            return { success: true }
        } catch (error) {
            console.error('Failed to delete review:', error)

            return { success: false }
        }
    }
    
    return {
        handleStatus,
        handleDeleteReview
    }
}