import { Chart } from './chart';
import { useEffect, useState } from 'react';
import { FillList, GroupBy, LoadingState } from './types';
import { Divider, Group, Select, Stack, Table, Text, TextInput } from '@mantine/core';
import { DatePicker, TimeInput } from '@mantine/dates';

export const Content = () => {
    const [loading, setLoading] = useState<LoadingState>(LoadingState.UNSUBMITTED)
    const [data, setData] = useState<FillList>()

    const [startDate, setStartDate] = useState<Date | null>(new Date())
    const [startTime, setStartTime] = useState<Date | null>(new Date())
    const [endDate, setEndDate] = useState<Date | null>(new Date())
    const [endTime, setEndTime] = useState<Date | null>(new Date())

    const [exchangeOptions, setExchangeOptions] = useState<string[]>([])
    const [exchange, setExchange] = useState<string | null>()

    const [symbolOptions, setSymbolOptions] = useState<string[]>([])
    const [symbol, setSymbol] = useState<string | null>()

    const [groupBy, setGroupBy] = useState<GroupBy>(GroupBy.MINUTES_5)

    useEffect(() => {
        if(!startDate || !startTime || !endDate || !endTime) return

        const start = new Date(startDate)
        start.setHours(startTime.getHours())
        start.setMinutes(startTime.getMinutes())

        const end = new Date(endDate)
        end.setHours(endTime.getHours())
        end.setMinutes(endTime.getMinutes())

        setLoading(LoadingState.LOADING)
        fetch(`http://api.pattern.test/fills?start=${start.getTime() * 1000}&end=${end.getTime() * 1000}&exchange=${exchange || ''}&symbol=${symbol || ''}`)
            .then(res => res.json())
            .then((payload: FillList) => {
                const exchangeValues = new Set(payload.fills.map(({ exchange }) => exchange))
                setExchangeOptions(Array.from(exchangeValues.values()))

                const symbolValues = new Set(payload.fills.map(({ symbol }) => symbol))
                setSymbolOptions(Array.from(symbolValues.values()))

                setData(payload)
                setLoading(LoadingState.SUCCESS)
            })
            .catch(() => {
                setLoading(LoadingState.FAILED)
            })
    }, [startDate, startTime, endDate, endTime, exchange, symbol])


    return (
        <>
            <Group>
                <Stack>
                    <DatePicker
                        label="Start date"
                        value={startDate}
                        onChange={setStartDate}
                    />
                    <TimeInput
                        label="Start time"
                        value={startTime}
                        onChange={setStartTime}
                    />
                    <DatePicker
                        label="End date"
                        value={endDate}
                        onChange={setEndDate}
                    />
                    <TimeInput
                        label="End time"
                        value={endTime}
                        onChange={setEndTime}
                    />
                    <Select
                        label="Group by"
                        value={groupBy}
                        onChange={(value) => value && setGroupBy(value as GroupBy)}
                        data={[
                            ... Object.values(GroupBy)
                        ]}
                    />
                    <Divider orientation='horizontal'/>
                    <Select
                        label="Filter by Exchange"
                        clearable
                        data={exchangeOptions}
                        value={exchange}
                        onChange={(value) => setExchange(value)}
                    />
                    <Select
                        label="Filter by Symbol"
                        clearable
                        data={symbolOptions}
                        value={symbol}
                        onChange={(value) => setSymbol(value)}
                    />
                </Stack>
                <div style={{ width: '80vw' }}>
                    {
                        loading === LoadingState.SUCCESS && data
                        ? (
                            <Chart rawData={data.fills} groupBy={groupBy} />
                        )
                        : (
                            <Text>Loading...</Text>
                        )
                    }
                </div>
            </Group>
            <Stack mx="md">
                <h2>All Results ({data?.count || 0})</h2>
                <Table highlightOnHover withColumnBorders>
                    <thead>
                    <tr>
                        <th>Order Id</th>
                        <th>Fill Price</th>
                        <th>Fees</th>
                        <th>Fill Quantity</th>
                        <th>Buy/Sell</th>
                        <th>Exchange</th>
                        <th>Symbol</th>
                        <th>Timestamp</th>
                    </tr>
                    </thead>
                    <tbody>
                    {
                        data?.fills && data.fills.map(
                            (fill) => {
                                return (
                                    <tr>
                                        <td>{fill.order_id}</td>
                                        <td>{fill.fill_price}</td>
                                        <td>{fill.fees}</td>
                                        <td>{fill.fill_quantity}</td>
                                        <td>{fill.side}</td>
                                        <td>{fill.exchange}</td>
                                        <td>{fill.symbol}</td>
                                        <td>{fill.timestamp}</td>
                                    </tr>
                                )
                            }
                        )
                    }
                    </tbody>
                </Table>
            </Stack>
        </>
    )
}
