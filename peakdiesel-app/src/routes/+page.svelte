<script lang="ts">
	import { formatRank, formatDate } from '$lib/format.js';

	let { data } = $props();

	let dieselPrices = $derived(data.prices);
	let latestPrice = $derived(dieselPrices[0]);
	let latestDate = $derived(formatDate(latestPrice.Date));
</script>

<h2>Have we reached peak diesel prices?</h2>
{#if latestPrice.price_rank == 1}
	<h1>Yes</h1>
{:else}
	<h1>No</h1>
{/if}

<p>
	The latest weekly update had diesel at ${latestPrice.Price} per gallon, adjusted for inflation this
	ranks as the {formatRank(latestPrice.price_rank)} highest price on record in the United States.
</p>
<p>National diesel weekly price update reported on {latestDate}.</p>

<style>
	h1 {
		text-align: center;
	}

	h2 {
		text-align: center;
	}

	p {
		text-align: center;
	}
</style>
