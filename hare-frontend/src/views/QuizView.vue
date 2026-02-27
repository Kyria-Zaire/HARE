<template>
  <div class="mx-auto max-w-2xl px-4 py-12">
    <h1 class="font-serif text-3xl font-bold text-primary">Quiz capillaire</h1>
    <p class="mt-2 text-secondary">Étape {{ store.currentStep }} / {{ store.TOTAL_STEPS }}</p>
    <div class="mt-6 h-2 w-full rounded-full bg-cream-light">
      <div
        class="h-full rounded-full bg-accent transition-all duration-300"
        :style="{ width: store.progressPercent + '%' }"
      />
    </div>
    <div class="mt-12 rounded-xl border-2 border-primary/20 bg-cream-light p-8 shadow-sm">
      <QuizStep :step="store.currentStep" />
      <div class="mt-8 flex justify-between">
        <button
          v-if="!store.isFirstStep"
          type="button"
          class="rounded-lg border-2 border-secondary/30 px-6 py-2 text-secondary hover:bg-white/50"
          @click="store.prevStep()"
        >
          Précédent
        </button>
        <div v-else />
        <button
          v-if="!store.isLastStep"
          type="button"
          class="rounded-lg bg-primary px-6 py-2 text-text-inverse hover:bg-bordeaux-dark"
          @click="store.nextStep()"
        >
          Suivant
        </button>
        <button
          v-else
          type="button"
          class="rounded-lg bg-primary px-6 py-2 text-text-inverse hover:bg-bordeaux-dark disabled:opacity-50"
          :disabled="store.isLoading"
          @click="onSubmit"
        >
          {{ store.isLoading ? 'Envoi…' : 'Voir mes recommandations' }}
        </button>
      </div>
    </div>
    <p v-if="store.error" class="mt-4 text-primary font-medium">{{ store.error }}</p>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useQuizStore } from '@/stores/quiz'
import QuizStep from '@/components/QuizStep.vue'

const store = useQuizStore()
const router = useRouter()

async function onSubmit() {
  const ok = await store.submitQuiz()
  if (ok) router.push('/results')
}
</script>
