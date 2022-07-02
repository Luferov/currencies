<template lang="pug">
v-card.card_no_choice
  v-card-text.text-center
    v-img.mx-auto.my-8(src="/icon.png" width="70")
    h3 Не выбрана ни одна валюта
</template>
<style lang="sass">
@media (max-width: 990px)
  .card_no_choice
    width: 100%

@media (min-width: 991px)
  .card_no_choice
    width: 50vw
    margin: 0 auto
</style>
