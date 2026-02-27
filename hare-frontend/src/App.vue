<template>
  <div class="min-h-screen flex flex-col bg-background text-text-primary">
    <header class="sticky top-0 z-50 bg-primary text-text-inverse shadow-md">
      <nav class="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
        <router-link to="/" class="font-serif text-xl font-bold text-text-inverse hover:text-accent transition">
          HARE Pro
        </router-link>
        <div class="flex items-center gap-6">
          <router-link to="/" class="text-white/90 hover:text-accent transition">Accueil</router-link>
          <router-link to="/quiz" class="text-white/90 hover:text-accent transition">Quiz</router-link>
          <router-link to="/results" class="text-white/90 hover:text-accent transition">Mes recos</router-link>
          <router-link to="/admin" class="text-accent text-sm font-medium hover:text-gold-light transition">Admin</router-link>
        </div>
      </nav>
    </header>
    <main class="flex-1">
      <router-view />
    </main>
    <footer class="bg-primary text-text-inverse py-8">
      <div class="mx-auto max-w-6xl px-4 flex flex-wrap items-center justify-between gap-4">
        <span class="font-serif font-semibold text-accent">HARE Pro</span>
        <span class="text-white/90 text-sm">Recommandations capillaires pour salon haut de gamme</span>
      </div>
    </footer>
    <Chatbot v-if="!isAdminRoute" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Chatbot from '@/components/Chatbot.vue'

const route = useRoute()
const isAdminRoute = computed(() => route.path.startsWith('/admin'))
</script>
