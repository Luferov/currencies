<script lang="ts" setup>
import { ref, unref, useDataFetch } from '#imports'
import moment from "moment";


const props = defineProps<{
  current_date: string,
  choice: string[],
}>()


const active = ref<boolean>(false)
const unloadTypes: { key: string, name: string, icon: string }[] = [
  { key: 'csv', name: 'Выгрузить в csv', icon: 'file-delimited' },
  { key: 'xlsx', name: 'Выгрузить в xlsx', icon: 'file-excel-box' },
  { key: 'pdf', name: 'Выгрузить в pdf', icon: 'file-pdf-box' },
]

/**
 * Функция выгрузки файла
 * @param fileType
 */
const unload = async (fileType: string): Promise<void> => {
  const { data } = await useDataFetch<{ src: string }>(`/coins/unload/${fileType}/`, {
    method: 'post',
    body: {
      date: moment(props.current_date, 'YYYY-MM-DD').format('MM/DD/YYYY'),
      codes: props.choice.join(',')
    }
  })
  const { src } = unref(data)
  window.location.href = src
}

</script>
<template lang="pug">
v-menu(v-model="active" location="start")
  template(#activator="{ props }")
    v-btn(v-bind="props" icon flat)
      v-icon(color="success") mdi-download
  v-list
    v-list-item(
      v-for="unloadType in unloadTypes"
      @click="unload(unloadType.key)"
      :key="unloadType.key"
    )
      v-list-item-icon(:icon="`mdi-${unloadType.icon}`" start)
      v-list-item-title {{ unloadType.name }}
</template>
