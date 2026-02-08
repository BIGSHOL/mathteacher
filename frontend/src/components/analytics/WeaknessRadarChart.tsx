import {
    Radar,
    RadarChart,
    PolarGrid,
    PolarAngleAxis,
    PolarRadiusAxis,
    ResponsiveContainer,
    Tooltip,
} from 'recharts'

interface RadarData {
    subject: string
    score: number
    fullMark: number
}

interface WeaknessRadarChartProps {
    data: RadarData[]
}

export function WeaknessRadarChart({ data }: WeaknessRadarChartProps) {
    if (!data || data.length === 0) {
        return <div className="text-center text-gray-500 py-10">데이터가 부족합니다.</div>
    }

    return (
        <div className="w-full h-64">
            <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
                    <PolarGrid stroke="#E5E7EB" />
                    <PolarAngleAxis
                        dataKey="subject"
                        tick={{ fill: '#4B5563', fontSize: 12 }}
                    />
                    <PolarRadiusAxis
                        angle={30}
                        domain={[0, 100]}
                        tick={false}
                        axisLine={false}
                    />
                    <Radar
                        name="숙련도"
                        dataKey="score"
                        stroke="#3B82F6"
                        fill="#3B82F6"
                        fillOpacity={0.4}
                    />
                    <Tooltip />
                </RadarChart>
            </ResponsiveContainer>
        </div>
    )
}
