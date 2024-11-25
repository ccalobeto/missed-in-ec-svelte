<script lang="ts">
	import Donut from '$lib/components/Donut.svelte';
	import { colors, categories } from '$lib/assets/utils/constants';
	import { csv } from 'd3-fetch';

	import type { PageData } from './$types';
	import type { Data } from '$lib/types';
	import { onMount } from 'svelte';

	// interface Props {
	// 	data: PageData;
	// }

	// let { data }: Props = $props();
	// /src/lib/data/missed.csv'
	let data: Data[] | undefined = $state([]);

	onMount(async () => {
		data = await csv('/src/lib/data/missed.csv', (row) => ({
			location: row.location,
			type: row.type,
			value: +row.value
		}));
	});

	// async function fetchCSV(url: string): Promise<Data[] | undefined> {
	// 	try {
	// 		const response = await fetch(url);
	// 		const data = await response.text();
	// 		const parsedData = data
	// 			.split('\n')
	// 			.slice(1)
	// 			.map((row) => {
	// 				const [location, type, value] = row.split(',');
	// 				return { location, type, value: +value };
	// 			});
	// 		return parsedData;
	// 	} catch (error) {
	// 		console.error('Error fetching:', error);
	// 	}
	// }

	// onMount(async () => {
	// 	data = await fetchCSV(
	// 		'https://raw.githubusercontent.com/ccalobeto/missed-in-ec-svelte/refs/heads/main/src/lib/data/missed.csv'
	// 	);
	// });

	// let data_ = loadData().then((data) => data);

	// let missed: Data[] = data.missed.map((d) => ({ ...d, value: +d.value }));
	// let missed = $derived(() => data.map((d) => ({ ...d, value: +d.value })));
	$inspect(data).with(console.trace);
	// console.log('missed: ', missed);
</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>

<!-- <Donut {data} {colors} {categories} /> -->

{#await data}
	<p>Loading...</p>
{:then data}
	<Donut {data} {colors} {categories} />
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}
