import { type AdminReviewsResponse, API_ENDPOINTS, type AdminReview } from '~/utils/api/api'

const adminReviewsCache = new Map<string, AdminReviewsResponse>()
const adminReviewsCacheExpiresAt = new Map<string, number>()
const adminReviewsRequests = new Map<string, Promise<AdminReviewsResponse>>()

const REVIEWS_CACHE_TTL_MS = 60 * 1000

export const useAdminReview = () => {
    const { apiFetch } = useApiFetch()

    const fetchAdminReviews = async (
        {
            force = false,
            page = 1,
            status,
            rating,
            search,
        }: {
            force?: boolean
            page?: number
            status?: string
            rating?: number
            search?: string
        } = {}
    ): Promise<AdminReviewsResponse> => {
        const cacheKey =
            `admin-reviews-page-${page}` +
            `-status-${status ?? 'all'}` +
            `-rating-${rating ?? 'all'}` +
            `-search-${search ?? ''}`

        const now = Date.now()

        // 1. Cache check
        const cached = adminReviewsCache.get(cacheKey)
        const expiresAt = adminReviewsCacheExpiresAt.get(cacheKey)

        if (!force && cached && expiresAt && now < expiresAt) {
            return cached
        }

        // 2. Prevent duplicate requests
        const existingRequest = adminReviewsRequests.get(cacheKey)

        if (!force && existingRequest) {
            return existingRequest
        }

        // 3. Build query parameters
        const params = new URLSearchParams()

        params.append('page', String(page))

        if (status && status !== 'all') {
            params.append('status', status)
        }

        if (rating !== undefined) {
            params.append('rating', String(rating))
        }

        if (search?.trim()) {
            params.append('search', search.trim())
        }

        // 4. Fetch admin reviews
        const request = apiFetch<AdminReviewsResponse>(
            `${API_ENDPOINTS.ADMIN_REVIEWS.LIST}?${params.toString()}`
        )
            .then((data) => {
                adminReviewsCache.set(cacheKey, data)
                adminReviewsCacheExpiresAt.set(
                    cacheKey,
                    Date.now() + REVIEWS_CACHE_TTL_MS
                )

                return data
            })
            .finally(() => {
                adminReviewsRequests.delete(cacheKey)
            })

        adminReviewsRequests.set(cacheKey, request)

        return request
    }

    // Update review status
    const updateReviewStatus = async (
        reviewId: number,
        status: 'approved' | 'rejected'
    ): Promise<AdminReview> => {
        return await apiFetch<AdminReview>(
            API_ENDPOINTS.ADMIN_REVIEWS.UPDATE_STATUS(reviewId),
            {
                method: 'PATCH',
                body: { status },
            }
        )
    }

    // Delete review
    const deleteAdminReview = async (reviewId: number): Promise<void> => {
        await apiFetch(
            API_ENDPOINTS.ADMIN_REVIEWS.DELETE(reviewId),
            {
                method: 'DELETE',
            }
        )
    }

    return {
        fetchAdminReviews,
        updateReviewStatus,
        deleteAdminReview,
    }
}