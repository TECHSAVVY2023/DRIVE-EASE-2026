import type { Car } from '~/utils/types/fleet'

const unavailableStatuses = [
    'pending_approval',
    'confirmed',
    'picked_up'
]

export function useCurrentRental(car: Car) {
    if (!car.unavailable_periods?.length) return null

    const now = new Date()

    return car.unavailable_periods
        .filter(period =>
            unavailableStatuses.includes(period.status) &&
            new Date(period.return_date) > now
        )
        .sort(
            (a, b) =>
                new Date(a.return_date).getTime() -
                new Date(b.return_date).getTime()
        )[0] ?? null
}
