import type { DieselPrice } from '$lib/types.js';
import type { PageLoad } from './$types.js';

export const load: PageLoad = async ({ fetch }) => {
  const res = await fetch("/weekly_diesel_prices.json")
  const prices: DieselPrice[] = await res.json();
  return { prices }
}
