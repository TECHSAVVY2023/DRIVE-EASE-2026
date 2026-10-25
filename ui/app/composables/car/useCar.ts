
import { API_ENDPOINTS } from '~/utils/api/api'
import type { Car } from '~/utils/types/fleet'


let carCache = new Map<string, Car>()
let carCacheExpiresAt = new Map<string, number>()
let carRequests = new Map<string, Promise<Car>>()
const CAR_CACHE_TTL_MS = 60 * 1000

export const useCar = () => {
    const { apiFetch } = useApiFetch()

    const fetchCar = async (
        carId: string,
        { force = false }: { force?: boolean } = {}
    ): Promise<Car> => {
        const now = Date.now()

        // 1. Cache check
        const cached = carCache.get(carId)
        const expiresAt = carCacheExpiresAt.get(carId)

        //if this condition is true, return the cached car so the system doesn't have to make request again
        //if this condition is false, proceed to fetch the car so that the data will be updated
        if (!force && cached && expiresAt && now < expiresAt) {
            return cached
        }

        // prevents the same request from being being made again and returns an ongoing Promise, 
        // which is the first request, for other components that need the same data
        const existingRequest = carRequests.get(carId)
        if (!force && existingRequest) {
            return existingRequest
        }

        // 3. Fetch
        const request = apiFetch<Car>(
            API_ENDPOINTS.CARS.DETAIL(carId)
        )
            .then((car) => {
            carCache.set(carId, car)
            carCacheExpiresAt.set(carId, Date.now() + CAR_CACHE_TTL_MS)
            return car
            })
            .finally(() => {
            carRequests.delete(carId)
            })

        carRequests.set(carId, request)

        return request
    }

    const createCar = async (form: {
        brand: string
        model: string
        year: number | null
        car_type: string | null
        price_per_day: number | null
        transmission: string
        engine: string
        fuel_type: string
        seats: number | null
        note: string
        status: string
        features: string[]
        meta: {
            primary_image: string | null
            images: string[]
        }
    }) => {
        const response = await apiFetch<Car>(
            API_ENDPOINTS.CARS.CREATE,
            {
                method: 'POST',
                body: form,
            }
        )

        return response
    }

    // Update car
    const updateCar = async (
        carId: string,
        form: Partial<{
            brand: string
            model: string
            year: number | null
            car_type: string | null
            price_per_day: number | null
            transmission: string
            engine: string
            fuel_type: string
            seats: number | null
            note: string
            status: string
            features: string[]
            meta: {
                primary_image: string | null
                images: string[]
            }
            deleted_images: string[]
        }>
    ): Promise<Car> => {
        const response = await apiFetch<Car>(
            API_ENDPOINTS.CARS.UPDATE(carId),
            {
                method: 'PATCH',
                body: form,
            }
        )

        // Update cache
        carCache.set(carId, response)
        carCacheExpiresAt.set(
            carId,
            Date.now() + CAR_CACHE_TTL_MS
        )

        return response
    }

    const deleteCar = async (carId: string): Promise<void> => {
        await apiFetch(
            API_ENDPOINTS.CARS.DELETE(carId),
            {
                method: 'DELETE',
            }
        )

        carCache.delete(carId)
        carCacheExpiresAt.delete(carId)
    }

    return {
        createCar,
        updateCar,
        fetchCar,
        deleteCar,
    }

}
