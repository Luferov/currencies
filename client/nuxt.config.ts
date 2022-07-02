import { defineNuxtConfig } from 'nuxt'

// https://v3.nuxtjs.org/api/configuration/nuxt.config
export default defineNuxtConfig({
  // @ts-ignore
  vite: false,
  css: [
    'vuetify/lib/styles/main.css',
    'mdi/css/materialdesignicons.min.css'
  ],
  runtimeConfig: {
    public: {
      API_URL: process.env.NUXT_API_URL
    }
  },
  build: {
    transpile: ['vuetify']
  }
})
