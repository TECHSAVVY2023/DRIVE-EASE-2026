import { ref } from 'vue'


export const useAboutPage = () => {

    interface Stat {
        value: string
        label: string
    }

    interface TeamMember {
        name: string
        role: string
        image: string
        description: string
    }

    interface Milestone {
        year: string
        title: string
        description: string
        progress: number
    }

    const stats: Stat[] = [
        { value: '5+', label: 'Locations' },
        { value: '10+', label: 'Cars' },
        { value: '4.8', label: 'Rating' },
    ]

    const team: TeamMember[] = [
        { name: 'Juber Sahiol', role: 'Founder & CEO', image: '', description: 'Leading the vision and growth of Drive Ease with a passion for customer satisfaction.' },
        { name: 'Juber Sahiol', role: 'Operations Manager', image: '', description: 'Overseeing daily operations to ensure smooth and efficient service delivery.' },
        { name: 'Juber Sahiol', role: 'Fleet Manager', image: '', description: 'Managing our vehicle fleet to maintain quality and reliability for all customers.' },
        { name: 'Juber Sahiol', role: 'Customer Support', image: '', description: 'Providing exceptional support to ensure every customer has a positive experience.' },
    ]

    const journey: Milestone[] = [
        {
            year: '2020',
            title: 'Drive Ease was founded',
            description: 'Started with a small fleet of 3 cars in Cagayan De Oro, focused on providing affordable local transportation.',
            progress: 30,
        },
        {
            year: '2021',
            title: 'Expanded to 10 vehicles',
            description: 'Grew our fleet to include economy, family, and SUV categories to meet growing customer demand.',
            progress: 55,
        },
        {
            year: '2022',
            title: 'Launched online booking',
            description: 'Introduced our digital platform, making it easier for customers to browse, book, and manage rentals online.',
            progress: 70,
        },
        {
            year: '2023',
            title: 'Reached 1,000+ happy customers',
            description: 'Achieved a milestone of over 1,000 satisfied customers with a 4.8-star average rating.',
            progress: 85,
        },
        {
            year: '2024',
            title: 'Opening new locations',
            description: 'Expanding our reach across Mindanao with new branches and a growing fleet of 20+ vehicles.',
            progress: 95,
        },
    ]

    return {
        stats,
        team,
        journey,
    }
}
