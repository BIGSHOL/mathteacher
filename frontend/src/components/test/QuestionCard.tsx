// 문제 카드 컴포넌트

import { motion, AnimatePresence } from 'framer-motion'
import { clsx } from 'clsx'
import { useState } from 'react'
import type { Question, QuestionCategory, QuestionOption } from '../../types'
import { MathText } from '../common/MathText'
import { FillInBlankInput } from './FillInBlankInput'

interface QuestionCardProps {
  question: Question
  questionNumber: number
  selectedAnswer: string | null
  onSelectAnswer: (answer: string) => void
  disabled?: boolean
  blankValues?: Record<string, string>
  onBlankChange?: (blankId: string, value: string) => void
  showExplanation?: boolean
  isCorrect?: boolean
  previousAnswer?: string
  headerRight?: React.ReactNode
}

export function QuestionCard({
  question,
  questionNumber,
  selectedAnswer,
  onSelectAnswer,
  disabled = false,
  blankValues = {},
  onBlankChange = () => { },
  showExplanation = false,
  isCorrect = false,
  previousAnswer,
  headerRight,
}: QuestionCardProps) {
  const [showHint, setShowHint] = useState(false)

  return (
    <div className="card p-4 sm:p-6">
      {/* 문제 번호 & 카테고리 & 난이도 */}
      <div className="mb-4 flex items-center justify-between">
        <div className="flex items-center gap-2 flex-wrap">
          <span className="rounded-full bg-primary-100 px-3 py-1 text-sm font-medium text-primary-700">
            {questionNumber}번 문제
          </span>
          {question.category && (
            <CategoryBadge category={question.category} />
          )}
          {question.concept_name && (
            <span className="rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium text-gray-600">
              {question.concept_name}
            </span>
          )}
        </div>
        <div className="flex items-center gap-2">
          {headerRight}
          <DifficultyBadge difficulty={question.difficulty} />
        </div>
      </div>

      {/* 문제 내용 (blank_config 있으면 FillInBlankInput이 텍스트를 대체 표시) */}
      {question.question_type === 'fill_in_blank' && question.blank_config ? (
        <div className="mb-6">
          <FillInBlankInput
            displayContent={question.blank_config.display_content}
            blankAnswers={question.blank_config.blank_answers}
            values={blankValues}
            onChange={onBlankChange}
            disabled={disabled}
          />
        </div>
      ) : (
        <div className="mb-6">
          <p className="text-lg font-medium text-gray-900 whitespace-pre-wrap">
            <MathText text={question.content} />
          </p>
        </div>
      )}

      {/* 선택지 */}
      {question.options && (
        <div className="space-y-3">
          {question.options.map((option) => (
            <AnswerOption
              key={option.id}
              option={option}
              isSelected={selectedAnswer === option.label}
              isPreviousAnswer={previousAnswer === option.label}
              onSelect={() => onSelectAnswer(option.label)}
              disabled={disabled}
            />
          ))}
        </div>
      )}

      {/* 단답형 / 빈칸 채우기 (blank_config 없을 때) */}
      {(question.question_type === 'short_answer' ||
        (question.question_type === 'fill_in_blank' && !question.blank_config)) && (
          <input
            type="text"
            placeholder="정답을 입력하세요"
            className="input mt-4"
            disabled={disabled}
            autoComplete="off"
            onChange={(e) => onSelectAnswer(e.target.value)}
          />
        )}

      {/* 힌트 토글 (hint가 존재할 때만 표시) */}
      {question.hint && (
        <div className="mt-4">
          <button
            onClick={() => setShowHint(!showHint)}
            className="flex items-center gap-2 text-sm font-medium text-amber-600 hover:text-amber-700 transition-colors"
          >
            <span className="text-lg">💡</span>
            {showHint ? '힌트 숨기기' : '힌트 보기'}
            <svg
              className={`h-4 w-4 transition-transform ${showHint ? 'rotate-180' : ''}`}
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <AnimatePresence>
            {showHint && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="overflow-hidden"
              >
                <div className="mt-2 rounded-xl bg-amber-50 p-4 text-sm text-amber-900 border border-amber-100">
                  <div className="flex gap-2">
                    <span className="shrink-0">💡</span>
                    <span><MathText text={question.hint} /></span>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      )}

      {/* 정답 및 해설 표시 (외부에서 제어) */}
      {showExplanation && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-6"
        >
          <div className={clsx(
            "rounded-xl p-5 border",
            isCorrect ? "bg-green-50 border-green-100" : "bg-red-50 border-red-100"
          )}>
            <div className="flex items-center gap-2 mb-2">
              <span className={clsx(
                "flex h-6 w-6 items-center justify-center rounded-full text-white text-xs font-bold",
                isCorrect ? "bg-green-500" : "bg-red-500"
              )}>
                {isCorrect ? '✓' : '✕'}
              </span>
              <span className={clsx(
                "font-bold",
                isCorrect ? "text-green-700" : "text-red-700"
              )}>
                {isCorrect ? '정답입니다!' : '오답입니다'}
              </span>
            </div>

            <div className="text-gray-700 leading-relaxed">
              {!isCorrect && question.correct_answer && (
                <div className="mb-2 text-sm">
                  <span className="font-semibold text-gray-500 mr-2">정답:</span>
                  <span className="font-bold text-gray-900">{question.correct_answer}</span>
                </div>
              )}
              <div className="text-sm sm:text-base">
                <MathText text={question.explanation} />
              </div>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  )
}

interface AnswerOptionProps {
  option: QuestionOption
  isSelected: boolean
  isPreviousAnswer?: boolean
  onSelect: () => void
  disabled: boolean
}

function AnswerOption({ option, isSelected, isPreviousAnswer, onSelect, disabled }: AnswerOptionProps) {
  return (
    <motion.button
      whileHover={!disabled ? { scale: 1.01 } : undefined}
      whileTap={!disabled ? { scale: 0.99 } : undefined}
      onClick={onSelect}
      disabled={disabled}
      className={clsx(
        'flex w-full items-center gap-4 rounded-xl border-2 p-4 text-left transition-all min-h-[3.5rem]',
        isSelected
          ? 'border-primary-500 bg-primary-50'
          : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50',
        disabled && 'cursor-default opacity-80'
      )}
    >
      <span
        className={clsx(
          'flex h-10 w-10 shrink-0 items-center justify-center rounded-full text-lg font-bold',
          isSelected ? 'bg-primary-500 text-white' : 'bg-gray-100 text-gray-600'
        )}
      >
        {option.label}
      </span>
      <span className="flex-1 text-gray-800 leading-relaxed">
        <MathText text={option.text} />
      </span>
      {isPreviousAnswer && !isSelected && (
        <span className="ml-2 text-xs text-gray-400 font-medium">지난번 선택</span>
      )}
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
