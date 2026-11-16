export interface AnalyticsRevenuePoint {
    label: string
    value: number
}

export interface AnalyticsRevenueResponse {
    period: number
    label: string
    total: number
    previous_total: number
    percentage_change: number | null
    points: AnalyticsRevenuePoint[]
}

export interface AnalyticsStatsResponse {
    period: number
    label: string
    total_revenue: number
    revenue_change: number | null
    total_bookings: number
    bookings_change: number | null
    fleet_utilization: number
    fleet_utilization_change: number | null
    cancellation_rate: number
    cancellation_rate_change: number | null
}

export interface AnalyticsTopVehicle {
    car_reference: string
    name: string
    bookings: number
    score: number
}

export interface AnalyticsTopVehiclesResponse {
    period: number
    label: string
    vehicles: AnalyticsTopVehicle[]
}

export interface AnalyticsCustomerInsightsResponse {
    period: number
    label: string
    new_customers: number
    new_customer_percentage: number
    returning_customers: number
    return_rate: number
    average_rental_days: number
    average_booking_value: number
}

export interface AnalyticsStatusDistributionResponse {
    period: number
    label: string
    total: number
    status_distribution: Status_Distribution[]
}

export interface BookingStatsResponse {
    total: number
    pending_approval: number
    active_rentals: number
    completed: number
    cancelled: number
    status_distribution: Status_Distribution[]
}

export interface Status_Distribution {
    status: string
    label: string
    count: number
    percentage: number
}
