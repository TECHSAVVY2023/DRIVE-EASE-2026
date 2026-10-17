

import { type CarReviewsResponse, type ReviewsResponse, API_ENDPOINTS } from '~/utils/api/api'

const reviewsCacheExpiresAt: Record<string, number> = {}
const REVIEWS_CACHE_TTL_MS = 60 * 1000

const carReviewsCache: Record<string, CarReviewsResponse> = {}
const carReviewsRequests = new Map<string, Promise<CarReviewsResponse>>()

const allReviewsCache: Record<string, ReviewsResponse> = {}
const allReviewsRequests = new Map<string, Promise<ReviewsResponse>>()

const featuredReviewsCache: Record<string, ReviewsResponse> = {}
const featuredReviewsRequests = new Map<string, Promise<ReviewsResponse>>()

export const useReviews = () => {
    const { apiFetch } = useApiFetch()
    
    // Fetch reviews for a specific car
    const fetchCarReviews = async (
        carId: string,
        { force = false, page = 1, rating, sort }: { force?: boolean; page?: number; rating?: number; sort?: string } = {}
    ): Promise<CarReviewsResponse> => {

        const cacheKey = `${carId}-page-${page}-rating-${rating ?? 'all'}-sort-${sort ?? 'highest'}`
        const now = Date.now()


        const expiresAt = reviewsCacheExpiresAt[cacheKey]
        if (!force && cacheKey in carReviewsCache && expiresAt && now < expiresAt) {
            return carReviewsCache[cacheKey]
        }

        const existingRequest = carReviewsRequests.get(cacheKey)
        if (!force && existingRequest) {
            return existingRequest
        }

        const request = apiFetch<CarReviewsResponse>(
            `/cars/${carId}/reviews/?page=${page}${rating ? `&rating=${rating}` : ''}${sort ? `&sort=${sort}` : ''}`
        )
            .then((data) => {
                carReviewsCache[cacheKey] = data
                reviewsCacheExpiresAt[cacheKey] = Date.now() + REVIEWS_CACHE_TTL_MS
                return data
            })
            .finally(() => {
                carReviewsRequests.delete(cacheKey)
            })

        carReviewsRequests.set(cacheKey, request)

        return request
    }

    // Fetch all reviews
    const fetchAllReviews = async (
        { force = false, page = 1, rating, sort }: { force?: boolean; page?: number; rating?: number; sort?: string } = {}
    ): Promise<ReviewsResponse> => {

        const cacheKey = `all-reviews-page-${page}-rating-${rating ?? 'all'}-sort-${sort ?? 'highest'}`
        const now = Date.now()

        const expiresAt = reviewsCacheExpiresAt[cacheKey]
        if (!force && cacheKey in allReviewsCache && expiresAt && now < expiresAt) {
            return allReviewsCache[cacheKey]
        }

        const existingRequest = allReviewsRequests.get(cacheKey)
        if (!force && existingRequest) {
            return existingRequest
        }

        const request = apiFetch<ReviewsResponse>(
            `/reviews/?page=${page}${rating ? `&rating=${rating}` : ''}${sort ? `&sort=${sort}` : ''}`
        )
            .then((data) => {
                allReviewsCache[cacheKey] = data
                reviewsCacheExpiresAt[cacheKey] = Date.now() + REVIEWS_CACHE_TTL_MS
                return data
            })
            .finally(() => {
                allReviewsRequests.delete(cacheKey)
            })

        allReviewsRequests.set(cacheKey, request)

        return request
    }

    // Fetch reviews for landing page
    const fetchFeaturedReviews = async (
        { force = false }: { force?: boolean } = {}
    ): Promise<ReviewsResponse> => {

        const cacheKey = 'featured-reviews'
        const now = Date.now()

        const expiresAt = reviewsCacheExpiresAt[cacheKey]
        if (!force && cacheKey in featuredReviewsCache && expiresAt && now < expiresAt) {
            return featuredReviewsCache[cacheKey]
        }

        const existingRequest = featuredReviewsRequests.get(cacheKey)
        if (!force && existingRequest) {
            return existingRequest
        }

        const request = apiFetch<ReviewsResponse>('/reviews/featured/')
            .then((data) => {
                featuredReviewsCache[cacheKey] = data
                reviewsCacheExpiresAt[cacheKey] = Date.now() + REVIEWS_CACHE_TTL_MS
                return data
            })
            .finally(() => {
                featuredReviewsRequests.delete(cacheKey)
            })

        featuredReviewsRequests.set(cacheKey, request)

        return request
    }

    const createReview = async (
        carId: string,
        form: {
            rating: number
            review: string
            images?: string[]
        }
    ) => {
        const response = await apiFetch<{ message: string }>(
            API_ENDPOINTS.REVIEWS.CREATE(carId),
            {
                method: "POST",
                body: form,
            }
        )

        // Clear cached reviews for this car
        Object.keys(carReviewsCache).forEach((key) => {
            if (key.startsWith(`${carId}-`)) {
                delete carReviewsCache[key]
                delete reviewsCacheExpiresAt[key]
            }
        })

        return response
    }

    const updateReview = async (
        carId: string,
        reviewId: number,
        body: {
            rating: number
            review: string
            images: string[]
            deleted_images?: string[]
        }
    ) => {
        const response = await apiFetch<{ message: string }>(
            `/reviews/cars/${carId}/edit/${reviewId}/`,
            {
                method: "PATCH",
                body
            }
        )

        // Clear cached reviews
        Object.keys(carReviewsCache).forEach((key) => {
            if (key.startsWith(`${carId}-`)) {
                delete carReviewsCache[key]
                delete reviewsCacheExpiresAt[key]
            }
        })

        return response
    }

    return {
        createReview,
        updateReview,
        fetchCarReviews,
        fetchAllReviews,
        fetchFeaturedReviews,
    }
}

