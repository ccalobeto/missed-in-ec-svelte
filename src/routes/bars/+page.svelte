<script lang="ts">
	import { scaleBand } from 'd3-scale';

	import { format, PeriodType } from '@layerstack/utils';
	import { createDateSeries } from '$lib/assets/utils/genData';

	import { Bars, Axis, Chart, Highlight, RectClipPath, Svg, Tooltip } from 'layerchart';

	const data = createDateSeries({
		count: 10,
		min: 20,
		max: 100,
		value: 'integer',
		keys: ['value', 'baseline']
	});
</script>

<div class="h-[300px] p-4 border rounded group">
	<Chart
		{data}
		x="value"
		xDomain={[0, null]}
		xNice
		y="date"
		yScale={scaleBand().padding(0.4)}
		padding={{ left: 16, bottom: 24 }}
		tooltip={{ mode: 'band' }}
	>
		<Svg>
			<Axis placement="bottom" grid rule />
			<Axis placement="left" format={(d) => format(d, PeriodType.Day, { variant: 'short' })} rule />
			<Bars strokeWidth={1} class="fill-primary group-hover:fill-gray-300 transition-colors" />
			<Highlight area>
				<svelte:fragment slot="area" let:area>
					<RectClipPath x={area.x} y={area.y} width={area.width} height={area.height} spring>
						<Bars strokeWidth={1} class="fill-primary" />
					</RectClipPath>
				</svelte:fragment>
			</Highlight>
		</Svg>
		<Tooltip.Root let:data>
			<Tooltip.Header
				>{format(data.date, PeriodType.Custom, {
					custom: 'eee, MMMM do'
				})}</Tooltip.Header
			>
			<Tooltip.List>
				<Tooltip.Item label="value" value={data.value} />
			</Tooltip.List>
		</Tooltip.Root>
	</Chart>
</div>
