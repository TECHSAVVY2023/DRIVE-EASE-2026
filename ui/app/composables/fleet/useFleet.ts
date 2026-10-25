import type { FleetResponse, FleetStatsResponse } from '~/utils/types/fleet'

const fleetCacheExpiresAt: Record<string, number> = {}
const FLEET_CACHE_TTL_MS = 60 * 1000

const FleetCache: Record<string, FleetResponse> = {}
const FleetRequests = new Map<string, Promise<FleetResponse>>()

export const useFleet = () => {
    const { apiFetch } = useApiFetch()

    const fetchFleet = async (
        {
            force = false,
            page = 1,
            search,
            brand,
            transmission,
            seats,
            car_type,
            fuel_type,
            features,
            sort,
            max_price,
            status,
            prioritize_available = false,
        }: {
            force?: boolean
            page?: number
            search?: string
            brand?: string
            transmission?: string
            seats?: string
            car_type?: string
            fuel_type?: string
            features?: string[]
            sort?: string
            max_price?: number
            status?: string
            prioritize_available?: boolean
        } = {}
    ): Promise<FleetResponse> => {

        const cacheKey =
            `cars-page-${page}` +
            `-search-${search ?? 'all'}` +
            `-brand-${brand ?? 'all'}` +
            `-transmission-${transmission ?? 'all'}` +
            `-seats-${seats ?? 'all'}` +
            `-car_type-${car_type ?? 'all'}` +
            `-fuel_type-${fuel_type ?? 'all'}` +
            `-features-${features?.slice().sort().join('-') ?? 'all'}` +
            `-max-${max_price ?? 'none'}` +
            `-sort-${sort ?? 'newest'}` +
            `-status-${status ?? 'all'}` +
            `-prioritize-${prioritize_available}`

        const now = Date.now()

        const expiresAt = fleetCacheExpiresAt[cacheKey]
        if (!force && cacheKey in FleetCache && expiresAt && now < expiresAt) {
            return FleetCache[cacheKey]
        }

        const existingRequest = FleetRequests.get(cacheKey)
        if (!force && existingRequest) {
            return existingRequest
        }

        const params = new URLSearchParams()

        params.append('page', String(page))

        if (search) params.append('search', search)
        if (brand) params.append('brand', brand)
        if (transmission) params.append('transmission', transmission)
        if (seats) params.append('seats', String(seats))
        if (car_type) params.append('car_type', car_type)
        if (fuel_type) params.append('fuel_type', fuel_type)
        features?.forEach(feature => {
            params.append('features', feature)
        })
        if (sort) params.append('sort', sort)

        if (max_price !== undefined && max_price !== null) {
            params.append("max_price", String(max_price))
        }

        if (status) params.append('status', status)
        if (prioritize_available) params.append('prioritize_available', 'true')

        const request = apiFetch<FleetResponse>(
            `/fleet/?${params.toString()}`
        )
            .then((data) => {
                FleetCache[cacheKey] = data
                fleetCacheExpiresAt[cacheKey] = Date.now() + FLEET_CACHE_TTL_MS
                return data
            })
            .finally(() => {
                FleetRequests.delete(cacheKey)
            })

        FleetRequests.set(cacheKey, request)

        return request
    }

    const fetchFleetStats = async (): Promise<FleetStatsResponse> => {
        return await apiFetch<FleetStatsResponse>('/fleet/stats/')
    }

    return {
        fetchFleet,
        fetchFleetStats,
    }
}
