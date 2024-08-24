import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import '@/assets/style.css'
import 'vue3-toastify/dist/index.css'
import App from '@/App.vue'
import Vue3Toasity from 'vue3-toastify'

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(router)
app.use(Vue3Toasity, {
  limit: 5,
  pauseOnFocusLoss: false
})
app.mount('#app')
