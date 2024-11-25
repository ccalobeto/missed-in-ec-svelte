<script lang="ts">
	import Donut from '$lib/components/Donut.svelte';
	import type { PageData } from './$types';
	import type Data from '$lib/types';

	interface Props {
		data: PageData;
	}

	let { data }: Props = $props();

	let missed: Data[] = data.missed.map((d) => ({ ...d, value: +d.value }));
</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>

<Donut data={missed} />
