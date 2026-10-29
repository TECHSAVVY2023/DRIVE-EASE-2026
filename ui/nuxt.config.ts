import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",

  ssr: true,

  nitro: {
    prerender: {
      crawlLinks: false,
      routes: ['/'],
    },
  },

  experimental: {
    appManifest: false,
  },

  srcDir: 'app',
  dir: {
    public: '../public',
  },
  imports: {
    dirs: [
      'composables',
      'composables/**'
    ]
  },
  devtools: { enabled: true },
  css: ['./app/assets/css/main.css'],
  vite: {
    plugins: [
      tailwindcss(),
    ],
  },
  app: {
    head: {
      link: [
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600;700;800&display=swap'
        },
        {
          rel: 'icon',
          type: 'image/x-icon',
          href: '/favicon.ico?v=20261025'
        }
      ]
    }
  },
  runtimeConfig: {
    // Public keys (exposed to client)
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE,
      apiApp: process.env.NUXT_PUBLIC_APP_URL,
    }
  }
});
