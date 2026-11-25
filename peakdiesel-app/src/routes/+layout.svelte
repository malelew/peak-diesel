<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';
	import '../styles/app.css';
	import '@fontsource-variable/source-sans-3';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

{@render children()}
