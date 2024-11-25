import type { Data, DonutData } from '$lib/types';

export function transformData(data: Data[]): DonutData[] {
  return data.map((data) => ({
    ...data,
    innerRadius: 0, 
    outerRadius: 0, 
    startAngle: 0, 
    endAngle: 0, 
  }));
}