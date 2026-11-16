export interface DashboardRevenuePoint {
    label: string
    value: number
}

export interface DashboardRevenueResponse {
    month: string
    label: string
    total: number
    previous_total: number
    percentage_change: number
    points: DashboardRevenuePoint[]
}

export interface DashboardStatsResponse {
    month: string
    total_bookings: number
    bookings_change: number | null
    total_revenue: number
    revenue_change: number | null
    active_rentals: number
    customers: number
    customers_change: number | null
}

export interface StatCard {
    label: string
    value: string
    change: string
    icon: string
    positive: boolean
}

export interface DashboardFleetStatusItem {
    label: string
    value: number
    percentage: number
}

export interface DashboardFleetStatusResponse {
    total: number
    items: DashboardFleetStatusItem[]
}

export interface DashboardRecentBooking {
    booking_reference: string
    customer: string
    vehicle: string
    amount: number
    status: string
    status_label: string
}

export interface DashboardRecentBookingsResponse {
    bookings: DashboardRecentBooking[]
}

export interface DashboardAttentionItem {
    label: string
    description: string
    count: number
    route: string
}

export interface DashboardAttentionResponse {
    items: DashboardAttentionItem[]
}
