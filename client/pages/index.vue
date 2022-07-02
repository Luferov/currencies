<script lang="ts" setup>
import moment from 'moment'
import { ref, unref, useDataFetch, watchEffect } from '#imports'
import CoinFilter from '~/components/CoinFilter.vue'
import CoinUnload from '~/components/CoinUnload.vue'
import DateFilter from '~/components/DateFilter.vue'
import NoChoiceCoinsView from '~/components/views/NoChoiceCoinsView.vue'
import OneChoiceCoinsView from '~/components/views/OneChoiceCoinsView.vue'
import CoinsView from '~/components/views/CoinsView.vue'
import { Value } from '~/types'

const choiceCoins = ref<string[]>([])
const date = ref<string | null>(moment().format('YYYY-MM-DD'))

const values = ref<Value[]>([])
const loading = ref<boolean>(false)

watchEffect(async () => {
  if (choiceCoins.value.length) {
    loading.value = true
    getValues(unref(date), unref(choiceCoins)).then(({ data }) => {
      values.value = unref(data)
      loading.value = false
    })
  } else {
    values.value = []
  }
})

/**
 * Функция получения значений
 * Хорошо, если она лежит в сервисном слое, но для этой задачи это излишне
 * @param d
 * @param coins
 */
const getValues = async (d: string, coins: string[]) => {
  return useDataFetch<Value[]>(`/coins/values/`, {
    params: {
      date: moment(d, 'YYYY-MM-DD').format('MM/DD/YYYY'),
      'rate__code': coins.join(',')
    },
    default: () => ([])
  })
}
</script>

<template lang="pug">
v-container
  v-row
    v-col.filters(cols="10")
      date-filter(v-model="date" key="dateFilter")
      coin-filter(@update="choiceCoins = $event" key="coinFilter" :choice="choiceCoins" :current_date="date")
    v-col.text-right(v-show="choiceCoins.length" :choice="choiceCoins" cols="2")
      coin-unload(:choice="choiceCoins" :current_date="date")
  v-row
    v-col
      v-progress-linear(v-show="loading" indeterminate color="primary")
      no-choice-coins-view(v-if="values.length === 0")
      one-choice-coins-view(v-else-if="values.length === 1" :value="values[0]")
      coins-view(v-else :values="values")
</template>

<style lang="sass">
.filters > span
  margin: 0 2px
.filters > span:first-child
  margin-right: 2px
  margin-left: 0
.filters > span:last-child
  margin-left: 2px
  margin-right: 0
</style>
