export interface RefundDetails {
    id: number
    paymongo_refund_id: string | null
    amount: number
    reason: string
    customer_reason: string
    admin_note: string
    status: 'pending_review' | 'processing' | 'succeeded' | 'failed' | 'rejected'
    failure_message: string
    requested_at: string
    processed_at: string | null
    updated_at: string
}

export interface Transaction {
    id:number
    booking_reference: string
    status: string

    payment_method: string
    payment_status: 'pending' | 'paid' | 'failed' | 'refunded' | null

    created_at: string
    total_price: number

    pending_approval_at: string | null
    confirmed_at: string | null
    picked_up_at: string | null
    returned_at: string | null
    completed_at: string | null
    cancelled_at: string | null
    cancel_reason: string | null
    refund: RefundDetails | null
    can_refund: boolean
    refund_unavailable_reason: string | null

    pickup_date: string
    return_date: string

    pickup_location: string
    return_location: string

    daily_rate: number
    number_of_days: number
    subtotal: number
    discount: number

    car: {
        car_reference: string
        brand: string
        model: string
        image: string
        year: number
        price_per_day: number
    }

    user: {
        user_reference: string
        email: string
        first_name: string
        last_name: string
        contact_number: string
        address: string
        profile_picture: string | null
        id_images: {
            images: string[]
        }
    }
}

export interface BookingForm {
    booking_reference: string
    user_reference: string
    car_reference: string

    payment_status?: 'pending' | 'paid' | 'failed' | 'refunded' | null
    payment_method?: string
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
