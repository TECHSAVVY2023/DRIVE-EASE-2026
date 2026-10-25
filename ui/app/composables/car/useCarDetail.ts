

import type { Car } from '~/utils/types/fleet'

export function useCarDetail() {
    const car = ref<Car | null>(null)
    const { fetchCar } = useCar()

    const getCar = async (carId: string, options?: { force?: boolean }) => {
        try {
            car.value = await fetchCar(carId, {
                force: options?.force,
            })
        } catch (err) {
            car.value = null
        }
    }

    return {
        car,
        getCar,
    }
}
