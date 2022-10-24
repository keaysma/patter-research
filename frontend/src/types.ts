type datetime = string

export enum LoadingState {
    UNSUBMITTED,
    LOADING,
    FAILED,
    SUCCESS
}

export enum GroupBy {
    SECONDS_1 = '1 Second',
    MINUTES_1 = '1 Minute',
    MINUTES_5 = '5 Minutes',
    HOURS_1 = '1 Hour',
    DAYS_1 = '1 Day',
}

export interface Fill {
    order_id: number
    fill_price: number
    fill_quantity: number
    side: 'BUY' | 'SELL' 
    exchange: string
    symbol: string
    fees: number
    timestamp: datetime

}
export interface FillList {
    fills: Fill[]
    count: number
}

export type FillGroup = [number, number, string]

export interface FillData {
    groups: FillGroup[]
}