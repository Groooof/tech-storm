import { createRouter, createWebHistory } from 'vue-router'
import { useViewerData } from '@/stores/viewer.js'
import DialogView from '@/views/DialogView.vue'
import LoginView from '@/views/LoginView.vue'

const routes = [
  {
    path: '/',
    component: DialogView,
    name: 'main'
  },
  {
    path: '/login',
    component: LoginView,
    name: 'login'
  }
]

const router = createRouter({
  routes: routes,
  history: createWebHistory()
})

router.beforeEach((to, from, next) => {
  const { isAuthenticated } = useViewerData()
  if (to.name === 'login' && isAuthenticated) next({ name: 'main' })
  else if (to.name !== 'login' && !isAuthenticated) next({ name: 'login' })
  else next()
})

export default router