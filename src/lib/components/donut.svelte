<script lang="ts">
	import { arc, pie } from 'd3-shape';
	import { scaleOrdinal } from 'd3-scale';
	import { ascending, sort } from 'd3-array';

	import type Data from '$lib/types';
	import data from '$lib/data/meat';

	let el: SVGGElement | null = $state(null);
	let width = $state(0);
	const height = 340;

	let countryData: Data[] = $state([]);

	let value = $state('USA');

	const pieAccessor = (data: object | { valueOf: number }) => {
		if (typeof data === 'object') {
			return (data as { value: number }).value;
		} else {
			return data;
		}
	};

	// sort the data so we will place the biggest slices first starting from 12 o'clock position.
	if (data) {
		countryData = sort(
			data.filter((d) => d.location === value).map((d) => ({ ...d, value: parseFloat(d.value) })),
			(a, b) => ascending(a.type, b.type)
		);
	}

	const colorScale = scaleOrdinal()
		.domain(['Beef', 'Pig', 'Poultry', 'Sheep'].sort(ascending))
		.range(['#A8a1ff', '#FFF84A', '#45FFC8', '#ff0266']);

	const pieGenerator = pie().value((d) => pieAccessor(d.valueOf));

	// lets make pieData reactive so if we change the data the function will also be updated
	let pieData = $derived.by(() => {
		return pieGenerator(countryData.map((d) => d.value));
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
		.innerRadius((0.96 * height) / 2)
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
					{#each pieData as d, i}
						{#if typeof d.data === 'object'}
							{#each [d.data] as item}
								<path
									class={i.toString()}
									pointer-events="all"
									cursor="pointer"
									d={arcGenerator(d) || ''}
									fill={colorScale(item.type)}
								/>
								<!-- labels -->
								<text
									in:fly={{ delay: 100, duration: 1000 }}
									x="0"
									y="0"
									text-anchor="middle"
									font-size="0.8em"
									class="fill-gray-100"
									transform="translate({labelArcs.centroid(d).join(' ')})"
									>{item.type}
								</text>
								<text
									x="0"
									y="1.2em"
									text-anchor="middle"
									font-size="0.8em"
									font-weight="700"
									class="fill-gray-100"
									transform="translate({labelArcs.centroid(d).join(' ')})"
									>{item.value + ' kg'}
								</text>
							{/each}
						{/if}
					{/each}
				</g>
				<!-- chart title -->
				<g transform="translate({width / 2 - 5} {height / 2 + 20})">
					<text
						x="0"
						y="0.5em"
						font-weight="bold"
						text-anchor="middle"
						font-size="2em"
						class="fill-gray-100"
						>{value}
					</text>
				</g>
			</svg>
		{/if}
	</div>
</div>
