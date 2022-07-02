<script lang="ts" setup>
import { defineEmits, defineProps } from 'vue-demi'
import { ref } from '#imports'
import moment from 'moment'


const props = defineProps<{
  modelValue: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', date: string)
}>()

const active = ref<boolean>(false)
const date = ref<string>(props.modelValue)

const apply = () => {
  emit('update:modelValue', date.value)
  active.value = false
}
</script>
<template lang="pug">
v-menu(v-model="active" :close-on-content-click="false")
  template(#activator="{ props }")
    v-chip(v-bind="props") {{ moment(modelValue, 'YYYY-MM-DD').format('DD.MM.YYYY') }}
  v-card
    v-card-text
      label(for="choiceDate")
        = 'Выбрать дату: '
      input(v-model="date" :max="moment().format('YYYY-MM-DD')" type="date" id="choiceDate" required)
    v-card-actions
      v-btn(@click="active = false") Закрыть
      v-spacer
      v-btn(@click="apply" color="success") Применить
</template>
