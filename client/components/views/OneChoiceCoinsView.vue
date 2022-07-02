<script lang="ts" setup>
import moment from 'moment'
import { useClipboard } from '@vueuse/core'
import { defineProps } from 'vue-demi'
import { Value } from '~/types'
import { oks } from '~/services'

const props = defineProps<{
  value: Value
}>()

type NamesType = { name: string, key: string }

const headers: NamesType[] = [
  { name: 'Код валюты', key: 'num_code' },
  { name: 'Символьный код', key: 'char_code' },
  { name: 'Номинал', key: 'rate.nominal' },
  { name: 'Код', key: 'rate.code' },
]

console.log(props.value.value)

const { copy, copied } = useClipboard()

</script>

<template lang="pug">
v-card.mx-auto.coin__container
  v-card-title
    v-icon.mr-2 mdi-coins
    | {{ value.rate.name }}
  v-card-subtitle На {{ moment(value.date, 'YYYY-MM-DD').format('DD.MM.YYYY') }}
  v-card-text.text-center.my-8.coin__block
    v-tooltip(location="top")
      template(#activator="{ props }")
        .coin__header(v-bind="props" @click="copy(value.value)") {{ value.value }}
      span Нажмите, чтобы скопировать
    span.coin__hint(v-show="copied") Скопировано!
  v-divider
  v-card-text
    v-list
      v-list-item(v-for="header in headers" :key="header.key")
        v-list-item-content
          v-list-item-title {{ oks(value, header.key) }}
          v-list-item-subtitle {{ header.name }}
</template>

<style lang="sass">
.coin__block
  height: 40px
.coin__header
  font-weight: bold
  font-size: 32px
  cursor: pointer
.coin__hint
  margin-top: 5px
  color: green

@media (max-width: 900px)
  .coin__container
    width: 100%
@media (max-width: 1699px) and (min-width: 900px)
  .coin__container
    width: 60vw
@media (min-width: 1700px)
  .coin__container
    width: 30vw
</style>
