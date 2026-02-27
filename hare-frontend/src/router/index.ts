import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import { useQuizStore } from '@/stores/quiz'

const routes: RouteRecordRaw[] = [
  { path: '/', name: 'Home', component: HomeView },
  {
    path: '/quiz',
    name: 'Quiz',
    component: () => import('@/views/QuizView.vue'),
  },
  {
    path: '/results',
    name: 'Results',
    component: () => import('@/views/ResultsView.vue'),
    beforeEnter(_to, _from, next) {
      const store = useQuizStore()
      if (!store.lastResult?.recommended_products?.length) {
        next({ path: '/quiz' })
      } else {
        next()
      }
    },
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('@/views/AdminDashboard.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
