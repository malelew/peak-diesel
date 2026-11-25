<script lang="ts">
	import { formatRank, formatDate } from '$lib/format.js';

	let { data } = $props();

	let dieselPrices = $derived(data.prices);
	let latestPrice = $derived(dieselPrices[0]);
	let latestDate = $derived(formatDate(latestPrice.Date));
	let isPeak = $derived(latestPrice.price_rank == 1);
</script>

<main
	class="flex min-h-screen flex-col justify-center gap-10 px-8 py-8 text-center"
	class:bg-orange-500={isPeak}
	class:bg-blue-700={!isPeak}
	class:text-white={!isPeak}
>
	<header class="space-y-1">
		<h2 class="text-xl text-balance">Have we reached peak diesel prices?</h2>
		<h1 class="text-8xl font-black tracking-tight">
			{isPeak ? 'Yes' : 'No'}
		</h1>
	</header>
	<div class="mx-auto max-w-prose space-y-3 text-left">
		<p>
			The latest weekly update had diesel at ${latestPrice.Price} per gallon, adjusted for inflation this
			ranks as the {formatRank(latestPrice.price_rank)} highest price on record in the United States.
		</p>
		<p class="opacity-80">National diesel weekly price update reported on {latestDate}.</p>
	</div>
</main>
