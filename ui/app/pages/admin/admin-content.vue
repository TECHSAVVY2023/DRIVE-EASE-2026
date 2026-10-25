<template>
    <div class="flex h-screen overflow-hidden bg-[#0D0D0D] font-[poppins] text-white">
        <AdminCommonSidebarNav
            :sidebar-open="sidebarOpen"
            @close-sidebar="sidebarOpen = false"
        />

        <div class="flex min-w-0 flex-1 flex-col overflow-hidden">
            <AdminCommonTopbarNav
                :user="user"
                :is-logged-in="isLoggedIn"
                title="Content"
                :subtitle="currentDate"
                @open-sidebar="sidebarOpen = true"
                @close-sidebar="sidebarOpen = false"
            />

            <main class="flex-1 overflow-y-auto px-4 py-6 sm:px-6 lg:px-8 lg:py-8">
                <header class="mb-6">
                    <h1 class="text-[22px] font-extrabold">Website content</h1>
                    <p class="mt-1 text-[13px] text-[#8a8a8a]">
                        Update the information displayed on your public pages
                    </p>
                </header>

                <div class="mb-5 flex gap-2 overflow-x-auto border-b border-[#242424]">
                    <button
                        v-for="page in pages"
                        :key="page.id"
                        type="button"
                        class="relative shrink-0 px-4 py-3 text-xs font-semibold transition-colors"
                        :class="selectedPage === page.id
                            ? 'text-white'
                            : 'text-[#747474] hover:text-white'"
                        @click="selectedPage = page.id"
                    >
                        {{ page.label }}
                        <span
                            v-if="selectedPage === page.id"
                            class="absolute inset-x-0 bottom-0 h-0.5 bg-[#C1121F]"
                        />
                    </button>
                </div>

                <section class="overflow-hidden rounded-xl border border-[#232323] bg-[#161616]">
                    <div class="flex flex-col gap-3 border-b border-[#252525] px-5 py-4 sm:flex-row sm:items-center sm:justify-between">
                        <div>
                            <h2 class="text-sm font-bold">{{ activePage.label }} page</h2>
                            <p class="mt-1 text-[11px] text-[#717171]">{{ activePage.description }}</p>
                        </div>

                        <span class="w-fit rounded-full bg-emerald-500/10 px-2.5 py-1 text-[9px] font-bold uppercase tracking-wide text-emerald-400">
                            Published
                        </span>
                    </div>

                    <form class="p-5 sm:p-6" @submit.prevent>
                        <!-- Home -->
                        <div v-if="selectedPage === 'home'" class="space-y-7">
                            <ContentSection
                                title="Hero section"
                                description="The first content visitors see on the homepage"
                            >
                                <div class="grid gap-4 sm:grid-cols-2">
                                    <div class="sm:col-span-2">
                                        <label for="home-heading" :class="labelClass">Main heading</label>
                                        <input id="home-heading" v-model="content.home.heading" :class="fieldClass" />
                                    </div>

                                    <div class="sm:col-span-2">
                                        <label for="home-description" :class="labelClass">Description</label>
                                        <textarea id="home-description" v-model="content.home.description" rows="4" :class="textareaClass" />
                                    </div>

                                    <div>
                                        <label for="home-button" :class="labelClass">Button label</label>
                                        <input id="home-button" v-model="content.home.buttonLabel" :class="fieldClass" />
                                    </div>

                                    <div>
                                        <label for="home-link" :class="labelClass">Button link</label>
                                        <input id="home-link" v-model="content.home.buttonLink" :class="fieldClass" />
                                    </div>
                                </div>
                            </ContentSection>

                            <ContentSection
                                title="Featured fleet"
                                description="Text displayed above the featured vehicles"
                            >
                                <div class="grid gap-4 sm:grid-cols-2">
                                    <div>
                                        <label for="fleet-heading" :class="labelClass">Section heading</label>
                                        <input id="fleet-heading" v-model="content.home.fleetHeading" :class="fieldClass" />
                                    </div>
                                    <div>
                                        <label for="fleet-description" :class="labelClass">Short description</label>
                                        <input id="fleet-description" v-model="content.home.fleetDescription" :class="fieldClass" />
                                    </div>
                                </div>
                            </ContentSection>
                        </div>

                        <!-- About -->
                        <div v-else-if="selectedPage === 'about'" class="space-y-7">
                            <ContentSection
                                title="Page introduction"
                                description="Main heading and introduction for the About page"
                            >
                                <div class="space-y-4">
                                    <div>
                                        <label for="about-heading" :class="labelClass">Page heading</label>
                                        <input id="about-heading" v-model="content.about.heading" :class="fieldClass" />
                                    </div>
                                    <div>
                                        <label for="about-introduction" :class="labelClass">Introduction</label>
                                        <textarea id="about-introduction" v-model="content.about.introduction" rows="4" :class="textareaClass" />
                                    </div>
                                </div>
                            </ContentSection>

                            <ContentSection
                                title="Our story"
                                description="Background information about DriveEase"
                            >
                                <div class="space-y-4">
                                    <div>
                                        <label for="story-heading" :class="labelClass">Section heading</label>
                                        <input id="story-heading" v-model="content.about.storyHeading" :class="fieldClass" />
                                    </div>
                                    <div>
                                        <label for="story-content" :class="labelClass">Story</label>
                                        <textarea id="story-content" v-model="content.about.story" rows="6" :class="textareaClass" />
                                    </div>
                                </div>
                            </ContentSection>
                        </div>

                        <!-- Contact -->
                        <div v-else class="space-y-7">
                            <ContentSection
                                title="Contact introduction"
                                description="Heading and message shown above the contact form"
                            >
                                <div class="space-y-4">
                                    <div>
                                        <label for="contact-heading" :class="labelClass">Page heading</label>
                                        <input id="contact-heading" v-model="content.contact.heading" :class="fieldClass" />
                                    </div>
                                    <div>
                                        <label for="contact-description" :class="labelClass">Description</label>
                                        <textarea id="contact-description" v-model="content.contact.description" rows="4" :class="textareaClass" />
                                    </div>
                                </div>
                            </ContentSection>

                            <ContentSection
                                title="Contact details"
                                description="Public business information shown to customers"
                            >
                                <div class="grid gap-4 sm:grid-cols-2">
                                    <div>
                                        <label for="contact-email" :class="labelClass">Email address</label>
                                        <input id="contact-email" v-model="content.contact.email" type="email" :class="fieldClass" />
                                    </div>
                                    <div>
                                        <label for="contact-phone" :class="labelClass">Phone number</label>
                                        <input id="contact-phone" v-model="content.contact.phone" :class="fieldClass" />
                                    </div>
                                    <div class="sm:col-span-2">
                                        <label for="contact-address" :class="labelClass">Business address</label>
                                        <input id="contact-address" v-model="content.contact.address" :class="fieldClass" />
                                    </div>
                                    <div>
                                        <label for="weekday-hours" :class="labelClass">Weekday hours</label>
                                        <input id="weekday-hours" v-model="content.contact.weekdayHours" :class="fieldClass" />
                                    </div>
                                    <div>
                                        <label for="weekend-hours" :class="labelClass">Weekend hours</label>
                                        <input id="weekend-hours" v-model="content.contact.weekendHours" :class="fieldClass" />
                                    </div>
                                </div>
                            </ContentSection>
                        </div>

                        <div class="mt-7 flex justify-end gap-2.5 border-t border-[#252525] pt-5">
                            <button
                                type="button"
                                class="rounded-lg border border-[#303030] px-4 py-2.5 text-xs text-[#aaa] transition hover:border-[#4a4a4a] hover:text-white"
                            >
                                Reset
                            </button>
                            <button
                                type="submit"
                                class="rounded-lg bg-[#C1121F] px-5 py-2.5 text-xs font-semibold text-white transition hover:bg-[#aa101b]"
                            >
                                Save changes
                            </button>
                        </div>
                    </form>
                </section>
            </main>
        </div>
    </div>
</template>

<script setup lang="ts">
type ContentPage = 'home' | 'about' | 'contact'

const { isLoggedIn } = useAuth()
const { user } = useCurrentUser()

const sidebarOpen = ref(false)
const selectedPage = ref<ContentPage>('home')

const pages = [
    {
        id: 'home' as const,
        label: 'Home',
        description: 'Manage homepage headings, descriptions, and featured content.',
    },
    {
        id: 'about' as const,
        label: 'About',
        description: 'Manage your company introduction and story.',
    },
    {
        id: 'contact' as const,
        label: 'Contact',
        description: 'Manage contact-page text and business details.',
    },
]

const activePage = computed(() =>
    pages.find(page => page.id === selectedPage.value) ?? pages[0]!
)

// Temporary local values. These can be replaced with API data later.
const content = reactive({
    home: {
        heading: 'Your journey starts with the right car',
        description: 'Reliable vehicles for city drives, business trips, and weekend escapes.',
        buttonLabel: 'Explore our fleet',
        buttonLink: '/client/fleet',
        fleetHeading: 'Find the perfect car',
        fleetDescription: 'Browse our most popular rental vehicles.',
    },
    about: {
        heading: 'About DriveEase',
        introduction: 'We make car rentals simple, reliable, and accessible for every journey.',
        storyHeading: 'Our story',
        story: 'DriveEase was created to give customers a faster and more convenient way to find dependable rental vehicles.',
    },
    contact: {
        heading: 'Get in touch',
        description: 'Have a question about a vehicle or booking? Our team is ready to help.',
        email: 'support@driveease.com',
        phone: '+63 900 000 0000',
        address: 'Cagayan de Oro City, Philippines',
        weekdayHours: 'Monday–Friday, 8:00 AM–6:00 PM',
        weekendHours: 'Saturday–Sunday, 9:00 AM–4:00 PM',
    },
})

const currentDate = new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
})

const fieldClass = `
    w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f]
    px-3.5 py-2.5 text-[13px] text-[#d4d4d4]
    outline-none transition-colors placeholder:text-[#555]
    focus:border-[#C1121F]
`
const textareaClass = `${fieldClass} resize-none leading-5`
const labelClass = 'mb-1.5 block text-[11px] text-neutral-400'

onMounted(() => document.documentElement.classList.add('admin-page'))
onBeforeUnmount(() => document.documentElement.classList.remove('admin-page'))
</script>
