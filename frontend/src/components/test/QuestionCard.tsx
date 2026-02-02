// 문제 카드 컴포넌트

import { motion } from 'framer-motion'
import { clsx } from 'clsx'
import type { Question, QuestionCategory, QuestionOption } from '../../types'
import { MathText } from '../common/MathText'

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
      {/* 문제 번호 & 카테고리 & 난이도 */}
      <div className="mb-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="rounded-full bg-primary-100 px-3 py-1 text-sm font-medium text-primary-700">
            {questionNumber}번 문제
          </span>
          {question.category && (
            <CategoryBadge category={question.category} />
          )}
        </div>
        <DifficultyBadge difficulty={question.difficulty} />
      </div>

      {/* 문제 내용 */}
      <div className="mb-6">
        <p className="text-lg font-medium text-gray-900">
          <MathText text={question.content} />
        </p>
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
      <span className="flex-1 text-gray-800">
        <MathText text={option.text} />
      </span>
    </motion.button>
  )
}

interface CategoryBadgeProps {
  category: QuestionCategory
}

function CategoryBadge({ category }: CategoryBadgeProps) {
  const isComputation = category === 'computation'
  return (
    <span
      className={clsx(
        'rounded-full px-2.5 py-0.5 text-xs font-medium',
        isComputation ? 'bg-blue-100 text-blue-700' : 'bg-emerald-100 text-emerald-700'
      )}
    >
      {isComputation ? '연산' : '개념'}
    </span>
  )
}

interface DifficultyBadgeProps {
  difficulty: number | string
}

function DifficultyBadge({ difficulty }: DifficultyBadgeProps) {
  const lv = typeof difficulty === 'number' ? difficulty : parseInt(difficulty, 10) || 5

  const getConfig = (level: number) => {
    if (level <= 2) return { color: 'bg-green-100 text-green-700' }
    if (level <= 4) return { color: 'bg-emerald-100 text-emerald-700' }
    if (level <= 6) return { color: 'bg-yellow-100 text-yellow-700' }
    if (level <= 8) return { color: 'bg-orange-100 text-orange-700' }
    return { color: 'bg-red-100 text-red-700' }
  }

  const { color } = getConfig(lv)

  return (
    <span className={clsx('rounded-full px-3 py-1 text-sm font-medium', color)}>
      Lv.{lv}
    </span>
  )
}
