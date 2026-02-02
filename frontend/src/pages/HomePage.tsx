import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'

export function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 to-white">
      <div className="container mx-auto px-4 py-16">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center"
        >
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            수학 테스트
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            재미있게 배우고, 빠르게 성장하세요!
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/login">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="btn-primary px-8 py-4 text-lg"
              >
                시작하기
              </motion.button>
            </Link>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3, duration: 0.5 }}
          className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8"
        >
          <FeatureCard
            icon="📚"
            title="개념 테스트"
            description="수학 개념을 확실하게 이해했는지 테스트해보세요"
          />
          <FeatureCard
            icon="🧮"
            title="연산 연습"
            description="반복 연습으로 연산 속도를 높여보세요"
          />
          <FeatureCard
            icon="📊"
            title="학습 통계"
            description="나의 성장 과정을 한눈에 확인하세요"
          />
        </motion.div>
      </div>
    </div>
  )
}

interface FeatureCardProps {
  icon: string
  title: string
  description: string
}

function FeatureCard({ icon, title, description }: FeatureCardProps) {
  return (
    <motion.div
      whileHover={{ y: -5 }}
      className="card p-6 text-center"
    >
      <div className="text-4xl mb-4">{icon}</div>
      <h3 className="text-xl font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </motion.div>
  )
}
