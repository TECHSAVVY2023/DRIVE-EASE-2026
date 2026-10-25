import type { Booking } from "~/components/Admin/Booking/bookingmodal.vue"
import type { TransactionResponse, BookingStatsResponse, BookingForm } from "~/utils/types/booking"
import { API_ENDPOINTS } from '~/utils/api/api'

const TRANSACTION_CACHE_TTL_MS = 60 * 1000

// Admin booking cache
const AdminBookingCache: Record<string, TransactionResponse> = {}
const AdminBookingRequests = new Map<string, Promise<TransactionResponse>>()
const adminBookingCacheExpiresAt: Record<string, number> = {}

export const useAdminTransactions = () => {

    const { apiFetch } = useApiFetch()

    const fetchAdminBookingsList = async (
        {
            force = false,
            page = 1,
            search,
            status,
            payment_status,
            sort,
        }: {
            force?: boolean
            page?: number
            search?: string
            status?: string
            payment_status?: string
            sort?: string
        } = {}
    ): Promise<TransactionResponse> => {

        const cacheKey =
            `admin-bookings-page-${page}` +
            `-search-${search ?? "all"}` +
            `-status-${status ?? "all"}` +
            `-payment-${payment_status ?? "all"}` +
            `-sort-${sort ?? "newest"}`

        const now = Date.now()
        const expiresAt = adminBookingCacheExpiresAt[cacheKey]

        // Cache
        if (
            !force &&
            cacheKey in AdminBookingCache &&
            expiresAt &&
            now < expiresAt
        ) {
            return AdminBookingCache[cacheKey]
        }

        // Prevent duplicate requests
        const existingRequest = AdminBookingRequests.get(cacheKey)

        if (!force && existingRequest) {
            return existingRequest
        }

        const params = new URLSearchParams()

        params.append("page", String(page))

        if (search) {
            params.append("search", search)
        }

        if (status) {
            params.append("status", status)
        }

        if (payment_status) {
            params.append("payment_status", payment_status)
        }

        if (sort) {
            params.append("sort", sort)
        }

        const request = apiFetch<TransactionResponse>(
            `/admin/bookings/?${params.toString()}`
        )
            .then((data) => {

                AdminBookingCache[cacheKey] = data

                adminBookingCacheExpiresAt[cacheKey] =
                    Date.now() + TRANSACTION_CACHE_TTL_MS

                return data
            })
            .finally(() => {
                AdminBookingRequests.delete(cacheKey)
            })

        AdminBookingRequests.set(cacheKey, request)

        return request
    }

    const createBooking = async (form: BookingForm) => {
        const response = await apiFetch<BookingForm>(
            API_ENDPOINTS.BOOKINGS.CREATE,
            {
                method: 'POST',
                body: form,
            }
        )

        return response
    }

    const updateBooking = async (
        bookingId: string,
        form: Partial<BookingForm>
    ): Promise<Booking> => {
        const response = await apiFetch<Booking>(
            API_ENDPOINTS.BOOKINGS.UPDATE(bookingId),
            {
                method: 'PATCH',
                body: form,
            }
        )

        return response
    }

    const deleteBooking = async (bookingId: string): Promise<void> => {
        await apiFetch(
            API_ENDPOINTS.BOOKINGS.DELETE(bookingId),
            {
                method: 'DELETE',
            }
        )

        for (const key in AdminBookingCache) {
            delete AdminBookingCache[key]
            delete adminBookingCacheExpiresAt[key]
        }
    }

    const fetchBookingStats = async (): Promise<BookingStatsResponse> => {
        return await apiFetch<BookingStatsResponse>('/admin/bookings/stats/')
    }

    return {
        fetchAdminBookingsList,
        fetchBookingStats,
        createBooking,
        updateBooking,
        deleteBooking,
    }
}
