import type { Car, UnavailablePeriod } from '~/utils/types/fleet'

export const DEFAULT_BOOKING_BUFFER_MINUTES = 60

export function useCurrentRental(car: Car) {
    if (!car.unavailable_periods?.length) return null

    const now = new Date()

    return car.unavailable_periods
        .filter(period => {
            const pickup = new Date(period.pickup_date)
            const returnDate = new Date(period.return_date)
            const bufferMilliseconds =
                (car.availability_buffer_minutes ?? DEFAULT_BOOKING_BUFFER_MINUTES)
                * 60 * 1000

            return (
                pickup <= now &&
                (returnDate.getTime() + bufferMilliseconds > now.getTime()
                    || period.is_overdue)
            )
        })
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

export function getBookingConflict(
    pickupDate: Date,
    returnDate: Date,
    periods: UnavailablePeriod[],
    bufferMinutes = DEFAULT_BOOKING_BUFFER_MINUTES,
): UnavailablePeriod | null {
    if (returnDate <= pickupDate) return null

    const bufferMilliseconds = bufferMinutes * 60 * 1000

    return periods.find(period => {
        const existingPickup = new Date(period.pickup_date)
        const existingReturn = period.is_overdue
            ? Infinity
            : new Date(period.return_date).getTime()

        return (
            pickupDate.getTime() < existingReturn + bufferMilliseconds &&
            returnDate.getTime() > existingPickup.getTime() - bufferMilliseconds
        )
    }) ?? null
}

export function hasBookingConflict(
    pickupDate: Date,
    returnDate: Date,
    periods: UnavailablePeriod[],
    bufferMinutes = DEFAULT_BOOKING_BUFFER_MINUTES,
): boolean {
    return Boolean(
        getBookingConflict(pickupDate, returnDate, periods, bufferMinutes),
    )
}
