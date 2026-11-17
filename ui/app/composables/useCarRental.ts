import type { Car, UnavailablePeriod } from '~/utils/types/fleet'

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
            new Date(period.pickup_date) <= now
        )
        .sort(
            (a, b) =>
                new Date(a.return_date).getTime() -
                new Date(b.return_date).getTime()
        )[0] ?? null
}

export function periodBlocksDate(period: UnavailablePeriod, date: Date) {
    const start = new Date(period.pickup_date)
    const end = new Date(period.return_date)

    start.setHours(0, 0, 0, 0)
    end.setHours(23, 59, 59, 999)

    return date >= start && (period.is_overdue || date <= end)
}
