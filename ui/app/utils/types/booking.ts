export interface Transaction {
    booking_reference: string
    status: string

    payment_method: string

    created_at: string
    total_price: number

    pending_approval_at: string | null
    confirmed_at: string | null
    picked_up_at: string | null
    returned_at: string | null
    completed_at: string | null
    cancelled_at: string | null
    cancel_reason: string | null

    pickup_date: string
    return_date: string

    pickup_location: string
    return_location: string

    daily_rate: number
    number_of_days: number
    subtotal: number
    discount: number

    car: {
        car_id: string
        brand: string
        model: string
        image: string
        year: number
        price_per_day: number
    }

    user: {
        id: number
        email: string
        first_name: string
        last_name: string
        contact_number: string
        address: string
        id_images: {
            images: string[]
        }
    }
}

export interface BookingForm {
    booking_reference: string
    user: number
    car: string

    status: string
    cancel_reason: string

    daily_rate: number
    number_of_days: number
    subtotal: number
    discount: number
    total_price: number

    pickup_date: string
    return_date: string
    pickup_location: string
    return_location: string
}

export interface TransactionResponse {
    count: number
    next?: string | null
    previous?: string | null
    results: Transaction[]
}

export interface BookingStatsResponse {
    total: number
    pending_approval: number
    active_rentals: number
    completed: number
    cancelled: number
}

export interface Tab {
    label: string
    value: string
}

export interface SortOption {
    label: string
    value: string
}
