<script lang="ts">
	import { formatRank } from '$lib/formatRank.js';

	let { data } = $props();

	let dieselPrices = $derived(data.prices);

	let latestPrice = $derived(data.prices[0]);
</script>

<h2>Have we reached peak diesel prices?</h2>
{#if latestPrice.price_rank == 1}
	<h1>Yes</h1>
	<!-- content here -->
{:else}
	<h1>No</h1>
	<!-- content here -->
{/if}

<p>
	The latest weekly update had diesel at ${latestPrice.Price} per gallon, adjusted for inflation this
	ranks as the {formatRank(latestPrice.price_rank)} highest price on record in the United States.
</p>
<p>National diesel weekly price update reported on {latestPrice.Date}</p>

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
