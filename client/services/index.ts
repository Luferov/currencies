
export const oks = (o: object, k: string, sep: string = '.') => {
  if (!k.length) { return o }
  const keys = k.split(sep)
  return oks(o[keys[0]], keys.slice(1).join(sep))
}
