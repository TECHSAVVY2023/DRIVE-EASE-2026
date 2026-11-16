import type { ContactPageContent, HomepageContentResult } from '~/utils/types/content'

export const useContactPageContentEdit = () => {
    const { updateContactPageContent } = useContactPageContent()
    const { $swal } = useNuxtApp()

    const handleUpdateContactPageContent = async (
        form: ContactPageContent
    ): Promise<HomepageContentResult> => {
        const required = [
            form.form_heading, form.form_description, form.phone, 
            form.email, form.address, ...form.opening_hours.flatMap(item => [item.day, item.time]),
        ]
        if (required.some(value => !String(value ?? '').trim())) {
            await $swal.fire({ icon: 'warning', title: 'Incomplete Form', text: 'Please complete all required Contact page fields.', confirmButtonColor: '#C1121F', background: '#1a1a1a', color: '#ffffff' })
            return { success: false, message: 'Incomplete Contact page fields.' }
        }

        $swal.fire({ title: 'Saving changes...', text: 'Please wait.', background: '#1a1a1a', color: '#ffffff', allowOutsideClick: false, allowEscapeKey: false, didOpen: () => $swal.showLoading() })
        try {
            await updateContactPageContent({
                form_heading: form.form_heading.trim(),
                form_description: form.form_description.trim(),
                phone: form.phone.trim(),
                email: form.email.trim(),
                address: form.address.trim(),
                facebook_url: form.facebook_url.trim(),
                instagram_url: form.instagram_url.trim(),
                x_url: form.x_url.trim(),
                tiktok_url: form.tiktok_url.trim(),
                opening_hours: form.opening_hours.map((item, order) => ({ ...item, day: item.day.trim(), time: item.time.trim(), order })),
            })
            await $swal.fire({ icon: 'success', title: 'Success', text: 'Contact page content updated successfully.', confirmButtonColor: '#C1121F', background: '#1a1a1a', color: '#ffffff' })
            return { success: true, message: 'Contact page content updated successfully.' }
        } catch (error) {
            console.error('Failed to update Contact page content:', error)
            await $swal.fire({ icon: 'error', title: 'Error', text: 'Failed to update Contact page content.', confirmButtonColor: '#C1121F', background: '#1a1a1a', color: '#ffffff' })
            return { success: false, message: 'Failed to update Contact page content.' }
        }
    }

    return { handleUpdateContactPageContent }
}
