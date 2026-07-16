// export const useReviews = () => {

//     const LandingVisibleReviews = computed(() =>
//         reviews.value.slice(0, 3)
//     )
    
//     interface Review {
//         name: string
//         avatar: string
//         date: string
//         rating: number
//         text: string
//         images: string[]
//         helpfulCount: number
//         helpfulClicked: boolean
//         car_id: number
//     }
    
//     const reviews = ref<Review[]>([
//         {
//             name: 'Juber Sahiol',
//             avatar: '',
//             date: 'January 1, 2026',
//             rating: 4,
//             car_id: 1,
//             text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean fermentum, sapien sed efficitur suscipit, turpis magna luctus sapien, vel sodales tortor tortor vel erat. Etiam consectetur ante et dolor consectetur, et lacinia eros mattis. Aliquam erat volutpat. Aliquam sit amet nisl eu sem posuere varius. Mauris ac nunc id nibh posuere ornare et vel tellus.',
//             images: ['', '', '', ''],
//             helpfulCount: 10,
//             helpfulClicked: false,
//         },
//         {
//             name: 'Juber Sahiol',
//             avatar: '',
//             date: 'January 1, 2026',
//             rating: 5,
//             car_id: 1,
//             text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean fermentum, sapien sed efficitur suscipit, turpis magna luctus sapien, vel sodales tortor tortor vel erat. Etiam consectetur ante et dolor consectetur, et lacinia eros mattis. Aliquam erat volutpat. Aliquam sit amet nisl eu sem posuere varius. Mauris ac nunc id nibh posuere ornare et vel tellus.',
//             images: ['', '', '', ''],
//             helpfulCount: 10,
//             helpfulClicked: false,
//         },
//         {
//             name: 'Maria Santos',
//             avatar: '',
//             date: 'February 14, 2026',
//             rating: 4,
//             car_id: 2,
//             text: 'Great experience overall! The car was clean and well-maintained. Pickup was smooth and the owner was very accommodating. Would definitely rent again.',
//             images: [],
//             helpfulCount: 5,
//             helpfulClicked: false,
//         },
//         {
//             name: 'Carlo Reyes',
//             avatar: '',
//             date: 'March 3, 2026',
//             rating: 5,
//             car_id: 2,
//             text: 'Highly recommended! Very affordable and the car performed great throughout our trip. No issues at all.',
//             images: [],
//             helpfulCount: 8,
//             helpfulClicked: false,
//         },
//     ])
    
//     return {
//         reviews,
//         LandingVisibleReviews,
//     }
// }