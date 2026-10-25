import type { RouterConfig } from '@nuxt/schema'

export default <RouterConfig>{
    scrollBehavior(to, _from, savedPosition) {
        if (savedPosition) return savedPosition

        // OAuth credentials temporarily use the fragment so browsers and
        // proxies do not send them as part of the HTTP request. They are not
        // an element id and must not be passed to querySelector by Vue Router.
        if (to.hash.startsWith('#access=')) {
            return { left: 0, top: 0 }
        }

        if (to.hash) {
            return { el: to.hash, behavior: 'smooth' }
        }

        return { left: 0, top: 0 }
    },
}
