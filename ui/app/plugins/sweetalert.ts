import Swal from 'sweetalert2'

export default defineNuxtPlugin(() => {

    const swal = Swal.mixin({
        heightAuto: false,
        scrollbarPadding: false, // important in modern SweetAlert2
    })
    
    return {
        provide: {
        swal: swal
        }
    }
})