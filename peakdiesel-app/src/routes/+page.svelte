<script lang="ts">
	import { dev } from '$app/environment';
	import { formatRank, formatDate } from '$lib/format.js';

	let { data } = $props();

	let previewPeak = $state(false);

	function previewPeakClick() {
		previewPeak = !previewPeak;
	}

	let dieselPrices = $derived(data.prices);
	let peakDieselPrice = $derived(dieselPrices.find((p) => p.price_rank == 1) ?? dieselPrices[0]);
	let latestPrice = $derived(!previewPeak ? dieselPrices[0] : peakDieselPrice);
	let latestDate = $derived(formatDate(latestPrice.Date));
	let isPeak = $derived(latestPrice.price_rank == 1);
</script>

<main
	class="flex min-h-screen flex-col justify-center gap-10 px-8 py-8 text-center text-white"
	class:bg-orange-800={isPeak}
	class:bg-blue-700={!isPeak}
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
			ranks as the {!isPeak ? formatRank(latestPrice.price_rank) : ''} highest price on record in the
			United States.
		</p>
		<p class="opacity-80">National diesel weekly price update reported on {latestDate}.</p>
	</div>

	{#if dev}
		<button
			onclick={previewPeakClick}
			class="fixed right-4 bottom-4 rounded bg-black px-4 py-2 text-sm text-white"
			type="button"
			name="Preview peak"
		>
			{!previewPeak ? 'See peak price' : 'See latest price'}</button
		>
	{/if}
</main>
