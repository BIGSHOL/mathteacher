// 진행 바 컴포넌트

import { motion } from 'framer-motion'

interface ProgressBarProps {
  current: number
  total: number
}

export function ProgressBar({ current, total }: ProgressBarProps) {
  const progress = (current / total) * 100

  return (
    <div className="mt-3">
      <div className="mb-1 flex justify-between text-sm">
        <span className="text-gray-600">
          <span className="font-semibold text-primary-500">{current}</span> / {total}
        </span>
        <span className="text-gray-500">{Math.round(progress)}%</span>
      </div>
      <div className="h-2 overflow-hidden rounded-full bg-gray-200">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${progress}%` }}
          transition={{ duration: 0.3 }}
          className="h-full rounded-full bg-primary-500"
        />
      </div>
    </div>
  )
}
