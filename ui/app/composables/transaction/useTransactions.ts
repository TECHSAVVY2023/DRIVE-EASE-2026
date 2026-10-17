import { type TransactionResponse, type Transaction } from "~/utils/api/api"

const transactionCacheExpiresAt: Record<string, number> = {}
const TRANSACTION_CACHE_TTL_MS = 60 * 1000

const TransactionCache: Record<string, TransactionResponse> = {}
const TransactionRequests = new Map<string, Promise<TransactionResponse>>()
const TransactionDetailCache: Record<string, Transaction> = {}
const TransactionDetailRequests = new Map<string, Promise<Transaction>>()

export const useTransactions = () => {
    const { apiFetch } = useApiFetch()

    const fetchTransactionsList = async (
        {
            force = false,
            page = 1,
            search,
            status,
            sort,
        }: {
            force?: boolean
            page?: number
            search?: string
            status?: string
            sort?: string
        } = {}
    ): Promise<TransactionResponse> => {

        const cacheKey =
            `transactions-page-${page}` +
            `-search-${search ?? "all"}` +
            `-status-${status ?? "all"}` +
            `-sort-${sort ?? "newest"}`

        const now = Date.now()

        const expiresAt = transactionCacheExpiresAt[cacheKey]

        if (
            !force &&
            cacheKey in TransactionCache &&
            expiresAt &&
            now < expiresAt
        ) {
            return TransactionCache[cacheKey]
        }

        const existingRequest = TransactionRequests.get(cacheKey)

        if (!force && existingRequest) {
            return existingRequest
        }

        const params = new URLSearchParams()

        params.append("page", String(page))

        if (search) params.append("search", search)
        if (status) params.append("status", status)
        if (sort) params.append("sort", sort)

        const request = apiFetch<TransactionResponse>(
            `/bookings/?${params.toString()}`
        )
            .then((data) => {
                TransactionCache[cacheKey] = data
                transactionCacheExpiresAt[cacheKey] =
                    Date.now() + TRANSACTION_CACHE_TTL_MS

                return data
            })
            .finally(() => {
                TransactionRequests.delete(cacheKey)
            })

        TransactionRequests.set(cacheKey, request)

        return request
    }

    const fetchTransactionDetail = async (
        bookingReference: string,
        force = false
    ): Promise<Transaction> => {

        const cacheKey = `transaction-detail-${bookingReference}`

        const now = Date.now()
        const expiresAt = transactionCacheExpiresAt[cacheKey]

        if (
            !force &&
            cacheKey in TransactionDetailCache && //
            expiresAt &&
            now < expiresAt
        ) {
            return TransactionDetailCache[cacheKey] //
        }

        const existingRequest = TransactionDetailRequests.get(cacheKey)

        if (!force && existingRequest) {
            return existingRequest
        }

        const request = apiFetch<Transaction>(
            `/bookings/${bookingReference}/`
        )
            .then((data) => {
                TransactionDetailCache[cacheKey] = data //
                transactionCacheExpiresAt[cacheKey] =
                    Date.now() + TRANSACTION_CACHE_TTL_MS

                return data
            })
            .finally(() => {
                TransactionDetailRequests.delete(cacheKey)
            })

        TransactionDetailRequests.set(cacheKey, request)

        return request
    }

    return {
        fetchTransactionsList,
        fetchTransactionDetail,
    }
}