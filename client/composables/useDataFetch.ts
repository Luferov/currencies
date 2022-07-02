import { useFetch, UseFetchOptions, useRuntimeConfig } from '#app'

/**
 * Пришлось сделать замыкание. Так как axios в nuxt3 нет
 * @param url
 * @param options
 */
export const useDataFetch = async <DateT>(url: string | Request, options?: UseFetchOptions<DateT>) => {
  const { public: { API_URL } } = useRuntimeConfig()
  const apiUrl = API_URL + url
  return useFetch<DateT>(apiUrl, options as unknown)
}
