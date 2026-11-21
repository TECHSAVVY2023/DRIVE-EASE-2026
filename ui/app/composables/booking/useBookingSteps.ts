export function useBookingSteps(
    steps: { title: string; subtitle: string }[],
    currentStep: Ref<number>,
    validateStepOne: Function,
    validateStepTwo: Function
) {

    async function nextStep(
        form: any,
        existingIdImages: string[],
        uploadedIdFiles: File[],
        car: Car | null,
    ) {
        if (currentStep.value === 1) {
            const valid = await validateStepOne(
                form,
                existingIdImages,
                uploadedIdFiles
            )

            if (!valid) return false
        }

        if (currentStep.value === 2) {
            const valid = await validateStepTwo(form, car)

            if (!valid) return false
        }

        if (currentStep.value < steps.length) {
            currentStep.value++
            return true
        }

        return false
    }

    return {
        nextStep,
    }
}
import type { Car } from '~/utils/types/fleet'
