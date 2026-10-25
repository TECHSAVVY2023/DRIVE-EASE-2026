export interface UnavailablePeriod {
    pickup_date: string
    return_date: string
    status: string
}

export interface CarType {
    id: number
    name: string
    slug: string
}

export interface Feature {
    id: number
    name: string
    slug: string
}

export interface Car {
    car_id: string
    brand: string
    model: string
    year: number
    car_type: string | null
    price_per_day: string
    transmission: string
    engine: string
    fuel_type: string
    seats: number
    features: string[]
    note: string | null
    png_image: string | null
    status: 'available' | 'maintenance'
    approval_status: string
    created_at: string
    created_by: number
    updated_at: string
    meta: {
        primary_image: string | null
        images: string[]
    }
    unavailable_periods: UnavailablePeriod[]
    rental_count: number
}

export interface VehicleImage {
    url: string
    file?: File
}

export interface CarForm {
    id: string
    car_type: string | null
    brand: string
    model: string
    year: number | null
    price_per_day: number | null
    transmission: string
    engine: string
    fuel_type: string
    seats: number | null
    note: string | null
    status: 'available' | 'maintenance'
    features: string[]
    images: VehicleImage[]
    thumbnail_url: string | null
}

export interface FilterOption {
    label: string
    count: number
}

export interface CarTypeFilterOption extends FilterOption {
    id: number
}

export interface FleetResponse {
    count: number
    page: number
    page_size: number
    total_pages: number
    next?: string | null
    previous?: string | null
    results: Car[]
    filters: {
        categories: CarTypeFilterOption[]
        transmissions: FilterOption[]
        seats: FilterOption[]
        fuel: FilterOption[]
        features: FilterOption[]
    }
}

export interface FleetStatsResponse {
    total_cars: number
    available_count: number
    unavailable_count: number
    maintenance_count: number
    pending_approval_count: number
    fleet_condition: number
    available_percentage: number
    rented_count: number
}
