import { uploadFile } from "~/utils/api/upload";
import type { HomepageContent, HomepageContentResult } from "~/utils/types/content";

interface OriginalFeaturedImage {
    id: number
    image: string | null
}

export const useHomepageContentEdit = () => {
    const {
        updateHomepageContent,
    } = useHomepageContent()
    const { $swal } = useNuxtApp()

    const validateForm = (form: HomepageContent): HomepageContentResult => {
        const requiredFields = [
            form.hero_heading1,
            form.hero_heading2,
            form.hero_tagline,
            form.trust_heading,
            form.faq_heading,
            form.faq_button_label,
            form.faq_button_link,
            ...form.trust_items.flatMap(item => [item.value, item.label]),
            ...form.faqs.flatMap(item => [item.question, item.answer]),
        ]

        if (requiredFields.some(field => !String(field ?? '').trim())) {
            return {
                success: false,
                message: 'Please complete all required content fields.',
            }
        }

        return {
            success: true,
            message: '',
        }
    }

    const handleUpdateHomepageContent = async (
        form: HomepageContent,
        newImageFile: File | null,
        newFeaturedImageFiles: (File | null)[],
        originalImageUrl: string | null,
        originalFeaturedImages: OriginalFeaturedImage[],
    ): Promise<HomepageContentResult> => {

        const validation = validateForm(form)

        if (!validation.success) {
            await $swal.fire({
                icon: 'warning',
                title: 'Incomplete Form',
                text: validation.message,
                background: '#1a1a1a',
                confirmButtonColor: '#C1121F',
                color: '#ffffff',
            })

            return validation
        }

        $swal.fire({
            title: 'Saving changes...',
            text: 'Please wait.',
            background: '#1a1a1a',
            color: '#ffffff',
            allowOutsideClick: false,
            allowEscapeKey: false,
            didOpen: () => $swal.showLoading(),
        })

        try {
            // Keep the current image unless a replacement was selected.
            let heroImageUrl = form.hero_image
            if (newImageFile) {
                heroImageUrl = await uploadFile(newImageFile)
            }

            const featuredImageUrls = await Promise.all(
                form.featured_cars.map(async (car, index) => {
                    const file = newFeaturedImageFiles[index]

                    return file
                        ? await uploadFile(file)
                        : car.featured_image
                })
            )

            const currentFeaturedIds = new Set(
                form.featured_cars
                    .map(item => item.id)
                    .filter(id => id > 0)
            )
            const originalImageById = new Map(
                originalFeaturedImages.map(item => [item.id, item.image])
            )

            // Track old images by database id instead of array index. Removing
            // or reordering cards must not delete another vehicle's image.
            const deletedFeaturedImages = new Set<string>()

            originalFeaturedImages.forEach(({ id, image }) => {
                if (!currentFeaturedIds.has(id) && image) {
                    deletedFeaturedImages.add(image)
                }
            })

            form.featured_cars.forEach((item, index) => {
                if (!newFeaturedImageFiles[index] || item.id <= 0) return

                const oldImage = originalImageById.get(item.id)
                if (oldImage) deletedFeaturedImages.add(oldImage)
            })

            const body = {
                hero_heading1: form.hero_heading1,
                hero_heading2: form.hero_heading2,
                hero_tagline: form.hero_tagline,
                fleet_heading: form.fleet_heading,
                fleet_description: form.fleet_description,
                trust_heading: form.trust_heading,
                faq_heading: form.faq_heading,
                faq_highlight: form.faq_highlight,
                faq_description: form.faq_description,
                faq_button_label: form.faq_button_label,
                faq_button_link: form.faq_button_link,
                hero_image: heroImageUrl,
                deleted_image: newImageFile ? originalImageUrl : null,
                deleted_featured_images: [...deletedFeaturedImages],
                trust_items: form.trust_items.map((item, index) => ({
                    id: item.id,
                    value: item.value.trim(),
                    label: item.label.trim(),
                    order: index,
                })),
                featured_cars: form.featured_cars.map((item, index) => ({
                    id: item.id,
                    car: item.car,
                    featured_image: featuredImageUrls[index] ?? item.featured_image,
                    order: index,
                })),
                faqs: form.faqs.map((item, index) => ({
                    id: item.id,
                    question: item.question.trim(),
                    answer: item.answer.trim(),
                    order: index,
                })),
            }

            await updateHomepageContent(body)

            $swal.close()

            await $swal.fire({
                icon: 'success',
                title: 'Success',
                text: 'Homepage content updated successfully.',
                confirmButtonColor: '#C1121F',
                background: '#1a1a1a',
                color: '#ffffff',
                allowOutsideClick: false,
                allowEscapeKey: false,
                scrollbarPadding: false,
            })

            return {
                success: true,
                message: 'Homepage content updated successfully.',
            }

        } catch (error) {
            console.error('Failed to update homepage content:', error)

            $swal.close()

            await $swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Failed to update homepage content.',
                confirmButtonColor: '#C1121F',
                background: '#1a1a1a',
                color: '#ffffff',
            })

            return {
                success: false,
                message: 'Failed to update homepage content.',
            }
        }
    }
    
    return {
        handleUpdateHomepageContent,
    }
}
