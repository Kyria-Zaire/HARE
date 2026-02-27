<template>
  <div class="mx-auto max-w-6xl px-4 py-12">
    <h1 class="font-serif text-3xl font-bold text-primary transition-all duration-300">Vos recommandations</h1>
    <p class="mt-2 text-secondary">{{ store.lastResult?.message }}</p>
    <div class="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <ProductCard
        v-for="(product, i) in store.lastResult?.recommended_products"
        :key="product.id ?? product.name"
        :product="product"
        class="animate-fade-in"
        :style="{ animationDelay: `${i * 50}ms` }"
      />
    </div>
    <div class="mt-12 flex flex-wrap gap-4">
      <button
        class="rounded-lg bg-primary px-6 py-3 text-text-inverse shadow-lg transition hover:scale-[1.02] hover:bg-bordeaux-dark hover:shadow-xl"
        @click="store.downloadReportPDF()"
      >
        Télécharger le rapport PDF
      </button>
    </div>

    <!-- Newsletter : section élégante bordeaux + or -->
    <section
      v-if="!newsletterOk"
      class="mt-20 overflow-hidden rounded-2xl border-2 border-primary/30 bg-gradient-to-br from-primary/5 to-accent/10 shadow-xl transition hover:shadow-2xl"
    >
      <div class="p-8 md:p-10">
        <div class="flex items-center gap-3">
          <span class="flex h-12 w-12 items-center justify-center rounded-full bg-primary/20 text-2xl">✉️</span>
          <div>
            <h2 class="font-serif text-2xl font-bold text-primary">Restez informée</h2>
            <p class="text-secondary">Conseils capillaires, offres salon et actualités dans votre boîte mail.</p>
          </div>
        </div>
        <form class="mt-6 flex flex-col gap-4 sm:flex-row sm:items-end" @submit.prevent="onNewsletterSubmit">
          <div class="flex-1">
            <input
              v-model="newsletterEmail"
              type="email"
              placeholder="votre@email.fr"
              required
              class="w-full rounded-xl border-2 border-primary/20 bg-white px-4 py-3 focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent/30 transition"
            />
          </div>
          <label class="flex cursor-pointer items-center gap-2 text-secondary sm:whitespace-nowrap">
            <input v-model="wantPdfByEmail" type="checkbox" class="h-4 w-4 rounded border-primary/30 text-accent focus:ring-accent" />
            <span>Recevoir le PDF par email (bonus)</span>
          </label>
          <button
            type="submit"
            class="rounded-xl bg-accent px-8 py-3 font-semibold text-secondary shadow transition hover:scale-[1.02] hover:bg-gold-light"
          >
            S'inscrire
          </button>
        </form>
        <p v-if="newsletterMessage" class="mt-4 text-sm font-medium" :class="newsletterOk ? 'text-green-700' : 'text-primary'">
          {{ newsletterMessage }}
        </p>
      </div>
    </section>
    <section v-else class="mt-20 rounded-2xl border-2 border-accent/40 bg-accent/10 p-8 text-center">
      <p class="font-serif text-xl font-bold text-primary">✓ Inscription enregistrée</p>
      <p class="mt-2 text-secondary">Merci ! Vous recevrez nos conseils capillaires par email.</p>
      <p v-if="wantPdfByEmail" class="mt-2 text-sm text-secondary">Le PDF vous sera envoyé par email sous peu.</p>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { useQuizStore } from '@/stores/quiz'
import ProductCard from '@/components/ProductCard.vue'

const store = useQuizStore()
const newsletterEmail = ref('')
const newsletterMessage = ref('')
const newsletterOk = ref(false)
const wantPdfByEmail = ref(false)

async function onNewsletterSubmit() {
  try {
    await axios.post('/api/v1/newsletter/subscribe', {
      email: newsletterEmail.value,
      quiz_profile: { ...store.answers, want_pdf_by_email: wantPdfByEmail.value },
      source: 'results_page',
      want_pdf_by_email: wantPdfByEmail.value,
    })
    newsletterMessage.value = 'Inscription enregistrée. Merci !'
    newsletterOk.value = true
  } catch {
    newsletterMessage.value = 'Erreur ou email déjà inscrit.'
    newsletterOk.value = false
  }
}
</script>

<style scoped>
@keyframes fade-in {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: fade-in 0.4s ease-out forwards;
}
</style>
