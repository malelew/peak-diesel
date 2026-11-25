<script lang="ts">
	import { formatRank, formatDate } from '$lib/format.js';

	let { data } = $props();

	let dieselPrices = $derived(data.prices);
	let latestPrice = $derived(dieselPrices[0]);
	let latestDate = $derived(formatDate(latestPrice.Date));
	let isPeak = $derived(latestPrice.price_rank == 1);
</script>

<main
	class="min-h-screen px-2 py-8 text-center"
	class:bg-orange-500={isPeak}
	class:bg-blue-700={!isPeak}
	class:text-white={!isPeak}
>
	<h2 class="text-lg">Have we reached peak diesel prices?</h2>
	<h1 class="text-8xl font-black tracking-tight">
		{isPeak ? 'Yes' : 'No'}
	</h1>

	<div class="mx-auto max-w-prose text-left">
		<p>
			The latest weekly update had diesel at ${latestPrice.Price} per gallon, adjusted for inflation this
			ranks as the {formatRank(latestPrice.price_rank)} highest price on record in the United States.
		</p>
		<p>National diesel weekly price update reported on {latestDate}.</p>
	</div>
</main>
