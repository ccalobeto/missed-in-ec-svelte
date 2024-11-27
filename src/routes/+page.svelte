<script lang="ts">
	import Donut from '$lib/components/Donut.svelte';
	import { colors, categories } from '$lib/assets/utils/constants';
	import { csv } from 'd3-fetch';

	import type { Data } from '$lib/types';
	import { onMount } from 'svelte';

	let data: Data[] | undefined;
	let isLoading = true;

	onMount(async () => {
		data = await csv('/data/missed.csv').then((d) => {
			return d.map((row) => ({
				location: row.location,
				type: row.type,
				value: parseFloat(parseFloat(row.value).toFixed(1))
			}));
		});

		isLoading = false;
	});
</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>

{#if isLoading}
	<p>Loading...</p>
{:else if data}
	<Donut {data} {colors} {categories} />
{:else}
	<p style="color: red">Error loading data</p>
{/if}
