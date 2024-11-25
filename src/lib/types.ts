import type { DefaultArcObject } from 'd3-shape';

export interface Data {
  location: string
  type: string
  value: number
}

export interface DonutData extends DefaultArcObject {
  value: number;
  type: string
  location: string

}