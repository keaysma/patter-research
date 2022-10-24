import { Fill, GroupBy } from "./types";
import { useMemo } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export const options = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top' as const,
    },
    title: {
      display: true,
      text: 'PnL',
    },
  },
};

const divisorByGroupBy: Record<GroupBy, number> = {
    [GroupBy.SECONDS_1]: 1000,
    [GroupBy.MINUTES_1]: 60000,
    [GroupBy.MINUTES_5]: 300000,
    [GroupBy.HOURS_1]: 3600000,
    [GroupBy.DAYS_1]: 86400000,
}

export const Chart = ({ rawData, groupBy }: { rawData : Fill[], groupBy: GroupBy }) => {
    const { data, labels } = useMemo(() => {
        // Group and aggregate fills into PnL
        const bucketedData = rawData.reduce(
            (acc, fill) => {
                // Determine grouping bucket, based on nearest timestamp by granularity
                const date = new Date(fill.timestamp)
                const divisor = divisorByGroupBy[groupBy]
                const key = new Date((Math.floor(date.getTime() / divisor) * divisor)).toISOString()

                // Aggregate data for timestamp
                acc[key] = (acc[key] || 0) + (fill.side === 'BUY' ? fill.fill_price : -fill.fill_price) - fill.fees
                return acc
            },
            {/* key is the time group, value is the PnL */} as Record<string, number>
        )
        return {
            data: Object.values(bucketedData),
            labels: Object.keys(bucketedData)
        }
    }, [rawData, groupBy])
    return (
        <Bar 
            options={options} 
            data={{
                labels,
                datasets: [{
                    label: '',
                    data,
                }]
        }} 
        />
    );
}