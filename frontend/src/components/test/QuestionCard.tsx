// 문제 카드 컴포넌트

import { motion } from 'framer-motion'
import { clsx } from 'clsx'
import type { Question, QuestionOption } from '../../types'

interface QuestionCardProps {
  question: Question
  questionNumber: number
  selectedAnswer: string | null
  onSelectAnswer: (answer: string) => void
  disabled?: boolean
}

export function QuestionCard({
  question,
  questionNumber,
  selectedAnswer,
  onSelectAnswer,
  disabled = false,
}: QuestionCardProps) {
  return (
    <div className="card p-6">
      {/* 문제 번호 & 난이도 */}
      <div className="mb-4 flex items-center justify-between">
        <span className="rounded-full bg-primary-100 px-3 py-1 text-sm font-medium text-primary-700">
          {questionNumber}번 문제
        </span>
        <DifficultyBadge difficulty={question.difficulty} />
      </div>

      {/* 문제 내용 */}
      <div className="mb-6">
        <p className="text-lg font-medium text-gray-900">{question.content}</p>
      </div>

      {/* 선택지 */}
      {question.options && (
        <div className="space-y-3">
          {question.options.map((option) => (
            <AnswerOption
              key={option.id}
              option={option}
              isSelected={selectedAnswer === option.label}
              onSelect={() => onSelectAnswer(option.label)}
              disabled={disabled}
            />
          ))}
        </div>
      )}

      {/* 단답형 (추후 구현) */}
      {question.question_type === 'short_answer' && (
        <input
          type="text"
          placeholder="정답을 입력하세요"
          className="input mt-4"
          disabled={disabled}
          onChange={(e) => onSelectAnswer(e.target.value)}
        />
      )}
    </div>
  )
}

interface AnswerOptionProps {
  option: QuestionOption
  isSelected: boolean
  onSelect: () => void
  disabled: boolean
}

function AnswerOption({ option, isSelected, onSelect, disabled }: AnswerOptionProps) {
  return (
    <motion.button
      whileHover={!disabled ? { scale: 1.01 } : undefined}
      whileTap={!disabled ? { scale: 0.99 } : undefined}
      onClick={onSelect}
      disabled={disabled}
      className={clsx(
        'flex w-full items-center gap-4 rounded-xl border-2 p-4 text-left transition-all',
        isSelected
          ? 'border-primary-500 bg-primary-50'
          : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50',
        disabled && 'cursor-not-allowed opacity-70'
      )}
    >
      <span
        className={clsx(
          'flex h-10 w-10 items-center justify-center rounded-full text-lg font-bold',
          isSelected ? 'bg-primary-500 text-white' : 'bg-gray-100 text-gray-600'
        )}
      >
        {option.label}
      </span>
      <span className="flex-1 text-gray-800">{option.text}</span>
    </motion.button>
  )
}

interface DifficultyBadgeProps {
  difficulty: string
}

function DifficultyBadge({ difficulty }: DifficultyBadgeProps) {
  const config = {
    easy: { label: '쉬움', color: 'bg-green-100 text-green-700' },
    medium: { label: '보통', color: 'bg-yellow-100 text-yellow-700' },
    hard: { label: '어려움', color: 'bg-red-100 text-red-700' },
  }

  const { label, color } = config[difficulty as keyof typeof config] || config.medium

  return (
    <span className={clsx('rounded-full px-3 py-1 text-sm font-medium', color)}>
      {label}
    </span>
  )
}
