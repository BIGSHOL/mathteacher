import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    Legend,
} from 'recharts'

interface TrendData {
    date: string
    solved: number
    accuracy: number
}

interface LearningTrendChartProps {
    data: TrendData[]
}

export function LearningTrendChart({ data }: LearningTrendChartProps) {
    if (!data || data.length === 0) {
        return <div className="text-center text-gray-500 py-10">데이터가 없습니다.</div>
    }

    return (
        <div className="w-full h-64">
            <ResponsiveContainer width="100%" height="100%">
                <LineChart
                    data={data}
                    margin={{
                        top: 5,
                        right: 30,
                        left: 20,
                        bottom: 5,
                    }}
                >
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
                    <XAxis
                        dataKey="date"
                        tick={{ fontSize: 12, fill: '#6B7280' }}
                        tickLine={false}
                        axisLine={{ stroke: '#E5E7EB' }}
                        tickFormatter={(value) => value.slice(5)} // MM-DD only
                    />
                    <YAxis
                        yAxisId="left"
                        tick={{ fontSize: 12, fill: '#6B7280' }}
                        tickLine={false}
                        axisLine={false}
                    />
                    <YAxis
                        yAxisId="right"
                        orientation="right"
                        domain={[0, 100]}
                        tick={{ fontSize: 12, fill: '#6B7280' }}
                        tickLine={false}
                        axisLine={false}
                        unit="%"
                    />
                    <Tooltip
                        contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                    />
                    <Legend />
                    <Line
                        yAxisId="left"
                        type="monotone"
                        dataKey="solved"
                        name="문제 풀이"
                        stroke="#8B5CF6"
                        strokeWidth={2}
                        activeDot={{ r: 6, fill: '#8B5CF6' }}
                        dot={{ fill: '#8B5CF6', r: 3 }}
                    />
                    <Line
                        yAxisId="right"
                        type="monotone"
                        dataKey="accuracy"
                        name="정답률"
                        stroke="#10B981"
                        strokeWidth={2}
                        dot={{ fill: '#10B981', r: 3 }}
                    />
                </LineChart>
            </ResponsiveContainer>
        </div>
    )
}
