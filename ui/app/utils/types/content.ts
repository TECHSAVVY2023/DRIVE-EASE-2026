export interface HomepageContentResult {
    success: boolean
    message: string
}

export interface HomePageFeaturedCar {
    id: number;
    car: number;
    car_name: string;
    car_reference: string;
    featured_image: string | null;
    price_per_day: string;
    order: number;
}

export interface HomePageFAQ {
    id: number;
    question: string;
    answer: string;
    order: number;
}

export interface HomeTrustUs {
    id: number;
    value: string;
    label: string;
    order: number;
}

export interface MiniCar {
    id: number;
    car_reference: string;
    brand: string;
    model: string;
    year: number;
    price_per_day: string;
}

export interface HomepageContent {
    id: number;
    hero_heading1: string;
    hero_heading2: string;
    hero_tagline: string;
    hero_image: string;
    fleet_heading: string;
    fleet_description: string;
    fleet_button_label: string;
    fleet_button_link: string;
    trust_heading: string;
    trust_items: HomeTrustUs[];
    faq_heading: string;
    faq_highlight: string;
    faq_description: string;
    faq_button_label: string;
    faq_button_link: string;
    featured_cars: HomePageFeaturedCar[];
    faqs: HomePageFAQ[];
    cars: MiniCar[];
    created_at: string;
    updated_at: string;
}

export type HomepageContentUpdatePayload = Partial<
    Omit<HomepageContent, 'trust_items' | 'featured_cars' | 'faqs'>
> & {
    deleted_image?: string | null;
    deleted_featured_images?: string[];
    trust_items?: Array<Pick<HomeTrustUs, 'id' | 'value' | 'label' | 'order'>>;
    featured_cars?: Array<
        Pick<HomePageFeaturedCar, 'id' | 'car' | 'featured_image' | 'order'>
    >;
    faqs?: HomePageFAQ[];
}

export interface AboutUsWwrStats {
    id: number;
    stat: string;
    value: string;
    order: number;
}

export interface AboutUsTeam {
    id: number;
    user: number | null;
    user_name: string;
    user_email: string;
    user_profile_picture: string | null;
    position: string;
    description: string;
    order: number;
}

export interface AboutUsJourney {
    id: number;
    title: string;
    description: string;
    year: string;
    order: number;
}

export interface AboutUsPageContent {
    id: number;
    content_reference: string;
    wwr_heading: string;
    wwr_description: string;
    wwr_image: string | null;
    mission_heading: string;
    mission_description: string;
    vission_heading: string;
    vission_description: string;
    wwr_stats: AboutUsWwrStats[];
    team: AboutUsTeam[];
    journey: AboutUsJourney[];
    updated_at: string;
}

export interface AboutTeamUserOption {
    id: number;
    user_reference: string;
    name: string;
    email: string;
    profile_picture: string | null;
}

export type AboutUsPageUpdatePayload = Omit<
    AboutUsPageContent,
    'id' | 'content_reference' | 'updated_at' | 'wwr_stats' | 'team' | 'journey'
> & {
    deleted_image?: string | null;
    wwr_stats: AboutUsWwrStats[];
    team: Array<Pick<AboutUsTeam, 'id' | 'user' | 'position' | 'description' | 'order'>>;
    journey: AboutUsJourney[];
}

export type AboutuspageContent = AboutUsPageContent

export interface ContactOpeningHour {
    id: number;
    day: string;
    time: string;
    is_closed: boolean;
    order: number;
}

export interface ContactPageContent {
    id: number;
    content_reference: string;
    form_heading: string;
    form_description: string;
    phone: string;
    email: string;
    address: string;
    facebook_url: string;
    instagram_url: string;
    x_url: string;
    tiktok_url: string;
    opening_hours: ContactOpeningHour[];
    updated_at: string;
}

export type ContactPageUpdatePayload = Omit<
    ContactPageContent,
    'id' | 'content_reference' | 'updated_at'
>
