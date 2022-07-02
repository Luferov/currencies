<script lang="ts" setup>
import moment from 'moment'
import { Rate} from '~/types'
import { computed, ref, unref, useDataFetch, watchEffect } from '#imports'


const props = withDefaults(defineProps<{
    current_date?: string,
    choice?: string[],
  }>(),
  {
    current_date: () => (moment().format('YYYY-MM-DD')),
    choice: () => ([])
  }
)

const emit = defineEmits<{
  (e: 'update', chosen: string[]): void
}>()


const rates = ref<Rate[]>([])

const active = ref<boolean>(false)
const selected = ref<string[]>(props.choice)
const search = ref<string>('')

watchEffect(async () => {
  const result = await useDataFetch<Rate[]>('/coins/rates/', {
    params: { date: moment(props.current_date, 'YYYY-MM-DD').format('MM/DD/YYYY') }
  })
  rates.value = unref(result.data)
})

const selectedAll = computed({
  get: () => (selected.value.length === rates.value.length),
  set: (value: boolean) => {
    selected.value = value && rates ? rates.value.map(rate => rate.code) : []
  }
})

const titleText = computed<string>(() => {
  if (!rates.value.length) {
    return 'Получение котировок для этой даты невозможно'
  }
  if (selectedAll.value) {
    return 'Выбраны все валюты'
  }
  if (selected.value.length === 0) {
    return 'Не выбрано ни одной валюты'
  } else {
    const firstRate = rates.value.find(rate => rate.code === selected.value[0])
    return selected.value.length === 1
      ? `Выбран ${firstRate.name}`
      : `Выбран ${firstRate.name} и еще ${selected.value.length - 1} валюта(ы)`
  }
})

const searchRates = computed(() => {
  if (search.value.length < 2) {
    return rates.value
  }
  const lowerSearch = search.value.toLowerCase()
  return (rates.value as Rate[]).filter(
    rate => rate.code.toLowerCase().includes(lowerSearch) || rate.name.toLowerCase().includes(lowerSearch)
  )
})

const apply = () => {
  emit('update', selected.value)
  search.value = ''
  active.value = false
}

</script>
<template lang="pug">
v-menu(v-model="active" :close-on-content-click="false")
  template(#activator="{ props }")
    v-chip(v-bind="props") {{ titleText }}
  v-card
    v-text-field(v-model="search" :hint="`Валют: ${rates.length}`" label="Поиск" clearable persistent-hint )
    v-card-text(style="overflow-y: auto; height: 300px")
      v-list
        v-list-item.cursor_pointer
          // Используем нативные shadow компоненты, если важна производительность
          // input(v-model="selectedAll" type="checkbox" id="chosenAllCodes")
          // label.ml-2(for="chosenAllCodes") Все валюты
          v-checkbox(v-model="selectedAll" label="Все валюты" hide-details density)
        v-list-item.cursor_pointer(v-for="rate in searchRates" :key="rate.code")
          // Используем нативные shadow компоненты, если важна производительность
          // input(v-model="selected" type="checkbox" :value="rate.code" :id="rate.code")
          // label.ml-2(:for="rate.code") {{ rate.name }}
          v-checkbox(v-model="selected" multiple :label="rate.name" :value="rate.code" hide-details density)
    v-card-actions
      v-btn(@click="active = false") Закрыть
      v-spacer
      v-btn(@click="apply" color="success") Применить
</template>

<style>
.cursor_pointer > input, .cursor_pointer > label {
  cursor: pointer !important;
}
</style>
