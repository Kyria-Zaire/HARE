<template>
  <div>
    <p v-if="step === 1" class="text-stone-600">Sélectionnez votre type de cheveux (1A à 4C).</p>
    <p v-if="step === 2" class="text-stone-600">Quelles sont vos préoccupations ? (sécheresse, frisottis, etc.)</p>
    <p v-if="step === 3" class="text-stone-600">Quelle est votre porosité ? (haute, moyenne, basse)</p>
    <p v-if="step === 4" class="text-stone-600">Quels sont vos objectifs ? (hydratation, volume, réparation…)</p>
    <p v-if="step === 5" class="text-stone-600">Type de cuir chevelu (optionnel).</p>
    <p v-if="step >= 6" class="text-stone-600">Récapitulatif et envoi.</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{ step: number }>()
</script>
