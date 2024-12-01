import type { DefaultArcObject } from 'd3-shape';

export interface Data {
  location: string
  cardinality: string
  value: number
}

export interface DonutData extends DefaultArcObject {
  value: number;
  cardinality: string
  location: string

}