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

                    <form class="p-5 sm:p-6" @submit.prevent="handleContentSubmit">
                        <!-- Home -->
                        <div v-if="selectedPage === 'home'" class="space-y-7">

                            <AdminContentHeroSection
                                v-if="home"
                                :form="form"
                                @update:newImageFile="newImageFile = $event"
                            />

                            <AdminContentWhyTrustus
                                v-if="home"
                                :form="form"
                            />

                            <AdminContentFeaturedCars
                                v-if="home"
                                :form="form"
                                v-model:featured-image-files="featuredImageFiles"
                            />

                            <AdminContentFaqSection
                                v-if="home"
                                :form="form"
                            />
                        </div>

                        <!-- About -->
                        <AdminContentAboutPage
                            v-else-if="selectedPage === 'about'"
                            :form="form1"
                            :users="aboutTeamUsers"
                            @update:newImageFile="newAboutImageFile = $event"
                        />

                        <!-- Contact -->
                        <AdminContentContactPage
                            v-else
                            :form="contactForm"
                        />

                        <div class="mt-7 flex justify-end gap-2.5 border-t border-[#252525] pt-5">
                            <button
                                type="button"
                                class="rounded-lg border border-[#303030] px-4 py-2.5 text-xs text-[#aaa] transition hover:border-[#4a4a4a] hover:text-white"
                            >
                                Reset
                            </button>
                            <button
                                type="submit"
                                class="rounded-lg bg-[#C1121F] px-5 py-2.5 text-xs font-semibold text-white transition hover:bg-[#9B0E18] disabled:cursor-not-allowed disabled:bg-[#4a1a1e] disabled:text-[#999]"
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
import type {
    HomepageContent,
    AboutUsPageContent,
    ContactPageContent,
    AboutTeamUserOption,
} from '~/utils/types/content'
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

const currentDate = new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
})

const form = ref<HomepageContent>({ id: 0, hero_heading1: '', hero_heading2: '', hero_tagline: '',
    hero_image: '', fleet_heading: '', fleet_description: '', trust_heading: '',
    trust_items: [], faq_heading: '', faq_highlight: '', faq_description: '', featured_cars: [],
    faqs: [], created_at: '', updated_at: '', cars: []
})

const form1 = ref<AboutUsPageContent>({ id: 0, content_reference: '', wwr_heading: '', wwr_description: '', wwr_image: null,
    mission_heading: '', mission_description: '', vission_heading: '', vission_description: '',
    wwr_stats: [], team: [], journey: [], updated_at: ''
})

const contactForm = ref<ContactPageContent>({
    id: 0, content_reference: '', form_heading: '', form_description: '', 
    phone: '', email: '', address: '', facebook_url: '', 
    instagram_url: '', x_url: '', tiktok_url: '',
    opening_hours: [], updated_at: '',
})

const aboutTeamUsers = ref<AboutTeamUserOption[]>([])

const newImageFile = ref<File | null>(null)
const originalImageUrl = ref<string | null>(null)
const newAboutImageFile = ref<File | null>(null)
const originalAboutImageUrl = ref<string | null>(null)
const originalFeaturedImages = ref<Array<{
    id: number
    image: string | null
}>>([])
const featuredImageFiles = ref<(File | null)[]>([])

const { home, loadHomepageContent } = useHomepageContentLoader()
const { about, loadAboutUsPageContent } = useAboutUsPageContentLoad()
const { fetchAboutTeamUsers } = useAboutUsPageContent()
const { contact, loadContactPageContent } = useContactPageContentLoad()

const {
    handleUpdateHomepageContent: updateHomepageContent
} = useHomepageContentEdit()
const {
    handleUpdateAboutUsPageContent: updateAboutUsPageContent
} = useAboutUsPageContentEdit()
const {
    handleUpdateContactPageContent: updateContactPageContent
} = useContactPageContentEdit()

watch(
    home,
    (homeValue) => {
        if (!homeValue) return
        form.value = structuredClone(toRaw(homeValue))
        originalImageUrl.value = homeValue.hero_image
        // Preserve originals by record id so removing/reordering stays safe.
        originalFeaturedImages.value = homeValue.featured_cars.map(car => ({
            id: car.id,
            image: car.featured_image,
        }))
        featuredImageFiles.value = homeValue.featured_cars.map(() => null)
    },
    { immediate: true }
)

watch(about, (value) => {
    if (!value) return
    form1.value = structuredClone(toRaw(value))
    originalAboutImageUrl.value = value.wwr_image
    newAboutImageFile.value = null
}, { immediate: true })

watch(contact, (value) => {
    if (value) contactForm.value = structuredClone(toRaw(value))
}, { immediate: true })

async function handleSaveHomepageContent(form: HomepageContent) {
    const result = await updateHomepageContent(
        form,
        newImageFile.value,
        featuredImageFiles.value,
        originalImageUrl.value,
        originalFeaturedImages.value
    )

    if (!result.success) return

    newImageFile.value = null
    window.location.reload()
}

async function handleContentSubmit(): Promise<void> {
    switch (selectedPage.value) {
        case 'home':
            await handleSaveHomepageContent(form.value)
            break

        case 'about':
            if ((await updateAboutUsPageContent(
                form1.value,
                newAboutImageFile.value,
                originalAboutImageUrl.value,
            )).success) {
                newAboutImageFile.value = null
                await loadAboutUsPageContent(true)
            }
            window.location.reload()
            break

        case 'contact':
            if ((await updateContactPageContent(contactForm.value)).success) {
                await loadContactPageContent(true)
            }
            window.location.reload()
            break
    }
}

onMounted(() => {
    loadHomepageContent()
    loadAboutUsPageContent()
    loadContactPageContent()
    fetchAboutTeamUsers().then((users) => {
        aboutTeamUsers.value = users
    }).catch((error) => {
        console.error('Failed to load About team users:', error)
    })
})

const fieldClass = `
    w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f]
    px-3.5 py-2.5 text-[13px] text-[#d4d4d4]
    outline-none transition-colors placeholder:text-[#555]
    focus:border-[#C1121F]
`

const compactFieldClass = `${fieldClass} px-3 py-2 text-xs`

onMounted(() => document.documentElement.classList.add('admin-page'))
onBeforeUnmount(() => document.documentElement.classList.remove('admin-page'))
</script>
