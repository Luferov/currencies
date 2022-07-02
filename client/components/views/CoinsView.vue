<script lang="ts" setup>
import { defineProps } from 'vue-demi'
import { useClipboard } from '@vueuse/core'
import moment from 'moment'
import { Value } from '~/types'
import { oks } from '~/services'

const props = defineProps<{
  values: Value[]
}>()

// server/apps/coins.services write_values_to_file
const headers: { name: string, value: string }[] = [
  { name: 'Код', value: 'rate.code' },
  { name: 'Название', value: 'rate.name' },
  { name: 'Цена', value: 'value' },
  { name: 'Дата', value: 'date' },
  { name: 'Номинал', value: 'rate.nominal' },
  { name: 'Код валюты', value: 'num_code' },
  { name: 'Символьный код валюты', value: 'char_code' },
]

const { copy } = useClipboard()
</script>

<template lang="pug">
v-table.coins_table(fixed-header height="calc(100vh - 164px)")
  thead
    tr
      th.text-center(v-for="header in headers" :key="header.value") {{ header.name }}
  tbody.coins__body
    tr(v-for="value in values" :key="value.id")
      td(v-for="header in headers" :key="header.value" :class="{ 'text-center': header.value !== 'rate.name' }")
        template(v-if="header.value === 'value'")
          v-tooltip(location="top")
            template(#activator="{ props }")
              .coins_value(v-bind="props" @click="copy(value.value)") {{ value.value }}
            span Нажмите, чтобы скопировать
        template(v-else-if="header.value === 'date'") {{ moment(value.date, 'YYYY-MM-DD').format('DD.MM.YYYY') }}
        template(v-else) {{ oks(value, header.value) }}
</template>

<style lang="sass">
.coins_value
  font-size: 16px
  font-weight: bold
  cursor: pointer
</style>
