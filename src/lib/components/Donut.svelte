<script lang="ts">
	import { arc, pie } from 'd3-shape';
	import { scaleOrdinal } from 'd3-scale';
	import { ascending, sort } from 'd3-array';
	import { fade } from 'svelte/transition';
	import { transformData } from '$lib/assets/utils/transforming';
	import { schemePastel1 } from 'd3-scale-chromatic';

	import type { Data, DonutData } from '$lib/types';

	interface Props {
		data: Data[] | undefined;
		donutOptions: any;
	}

	let { data, donutOptions }: Props = $props();

	let el: SVGGElement | null = $state(null);
	let width = $state(0);
	const height = 340;

	let dataToDisplay: Data[] = $state([]);

	let location = donutOptions.donutCenter;
	let cardinalities: string[] | undefined = data?.map((d) => d.cardinality);

	// sort the data so we will place the biggest slices first starting from 12 o'clock position.
	if (data) {
		dataToDisplay = sort(
			data.filter((d) => d.location === location),
			(a, b) => a.value - b.value
		);
	}
	const colorScale: (cardinality: string) => string = scaleOrdinal()
		.domain((cardinalities || []).sort(ascending))
		.range(schemePastel1) as unknown as (cardinality: string) => string;

	const pieAccesor = (row: any) => {
		if (typeof row === 'object' && 'value' in row) {
			return row.value;
		} else {
			return row;
		}
	};

	const pieGenerator = pie<DonutData>().value(pieAccesor);

	// lets make pieData reactive so if we change the data the function will also be updated
	let pieData = $derived.by(() => {
		return pieGenerator(transformData(dataToDisplay));
	});

	const arcGenerator = arc()
		.startAngle((d) => d.startAngle)
		.endAngle((d) => d.endAngle)
		// 60% of the full radius gives a nice appearance (0.6)
		// To see a pie chart, just change this to zero
		.innerRadius((0.6 * height) / 2.4)
		// Outer radius is less than the full radius because our labels will sit outside of the donut
		.outerRadius((0.85 * height) / 2.2)
		.padRadius(40)
		.cornerRadius(4);

	const labelArcs = arc()
		.innerRadius((0.7 * height) / 2)
		.outerRadius((0.96 * height) / 2);
</script>

<div class="chart-container flex flex-col items-center justify-around md:flex-row">
	<div class="svg-container w-[500px]" bind:clientWidth={width}>
		{#if width}
			<svg {width} {height} class="chart">
				<g
					bind:this={el}
					class="donut-container"
					transform="translate({width / 2 - 5} {height / 2 + 20})"
				>
					{#each pieData as d, i (d.data.cardinality)}
						{#if typeof d.data === 'object' && 'cardinality' in d.data}
							{#each [d.data] as item}
								<path
									class={i.toString()}
									pointer-events="all"
									cursor="pointer"
									d={arcGenerator({
										startAngle: d.startAngle,
										endAngle: d.endAngle,
										innerRadius: (0.6 * height) / 2.4,
										outerRadius: (0.85 * height) / 2.2
									})}
									fill={colorScale(item.cardinality as string)}
								/>
								<text
									in:fade={{ delay: 100, duration: 1000 }}
									x="0"
									y="0"
									text-anchor="middle"
									font-size="0.8em"
									class="fill-gray-100"
									transform="translate({labelArcs
										.centroid({
											startAngle: d.startAngle,
											endAngle: d.endAngle,
											innerRadius: (0.96 * height) / 2,
											outerRadius: (0.96 * height) / 2
										})
										.join(' ')})"
									>{item.cardinality}
								</text>
								<text
									x="0"
									y="1.2em"
									text-anchor="middle"
									font-size="0.8em"
									font-weight="700"
									class="fill-gray-100"
									transform="translate({labelArcs
										.centroid({
											startAngle: d.startAngle,
											endAngle: d.endAngle,
											innerRadius: (0.96 * height) / 2,
											outerRadius: (0.96 * height) / 2
										})
										.join(' ')})"
									>{item.value + ' ' + donutOptions.units}
								</text>
							{/each}
						{/if}
					{/each}
				</g>
				<g transform="translate({width / 2 - 5} {height / 2 + 20})">
					<text
						x="0"
						y="0.5em"
						font-weight="bold"
						text-anchor="middle"
						font-size="2em"
						class="fill-gray-100"
						>{location}
					</text>
				</g>
			</svg>
		{/if}
	</div>
</div>
