<script lang="ts">
	import Donut from '$lib/components/Donut.svelte';
	import dataset from '$lib/data/data_summaries.json';

	import type { Data } from '$lib/types';
	import { onMount } from 'svelte';

	let isLoading = true;

	let data: Data[] = dataset[4].data.map((d) => {
		return {
			location: d.country,
			cardinality: d.cardinality,
			value: parseFloat(d.percentage.toFixed(1))
		};
	});

	let donutOptions = {
		donutCenter: 'ECU',
		units: '%'
	};

	onMount(async () => {
		isLoading = false;
	});
</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>

{#if isLoading}
	<p>Loading...</p>
{:else if data}
	<Donut {data} {donutOptions} />
{:else}
	<p style="color: red">Error loading data</p>
{/if}
