import { useEffect, useRef } from 'react'
import { clsx } from 'clsx'
import { MathText } from '../common/MathText'

interface FillInBlankInputProps {
  displayContent: string
  blankAnswers: Record<string, { answer: string; position: number }>
  values: Record<string, string>
  onChange: (blankId: string, value: string) => void
  disabled?: boolean
  showCorrectAnswers?: boolean
}

export function FillInBlankInput({
  displayContent,
  blankAnswers,
  values,
  onChange,
  disabled = false,
  showCorrectAnswers = false,
}: FillInBlankInputProps) {
  const inputRefs = useRef<Record<string, HTMLInputElement | null>>({})

  // 첫 번째 빈칸에 자동 포커스
  useEffect(() => {
    const blankIds = Object.keys(blankAnswers)
    if (blankIds.length > 0 && !disabled) {
      const firstBlankId = blankIds[0]
      if (firstBlankId) {
        inputRefs.current[firstBlankId]?.focus()
      }
    }
  }, [blankAnswers, disabled])

  // displayContent를 파싱하여 텍스트와 빈칸 위치 추출
  const parts = displayContent.split('___')
  const blankIds = Object.keys(blankAnswers).sort()

  const handleKeyDown = (
    e: React.KeyboardEvent<HTMLInputElement>,
    currentBlankId: string
  ) => {
    // Tab 키로 다음 빈칸으로 이동
    if (e.key === 'Tab') {
      e.preventDefault()
      const currentIndex = blankIds.indexOf(currentBlankId)
      const nextIndex = e.shiftKey ? currentIndex - 1 : currentIndex + 1

      if (nextIndex >= 0 && nextIndex < blankIds.length) {
        const nextBlankId = blankIds[nextIndex]
        if (nextBlankId) {
          inputRefs.current[nextBlankId]?.focus()
        }
      }
    }
  }

  const getInputStyle = (blankId: string) => {
    if (!showCorrectAnswers) {
      return 'border-gray-300 focus:border-primary-500 focus:ring-primary-500'
    }

    const userAnswer = values[blankId]?.trim().toUpperCase()
    const correctAnswer = blankAnswers[blankId]?.answer?.trim().toUpperCase()
    const isCorrect = userAnswer === correctAnswer

    if (isCorrect) {
      return 'border-green-500 bg-green-50'
    }
    return 'border-red-500 bg-red-50'
  }

  return (
    <div className="fill-in-blank-container space-y-4">
      <div className="text-lg leading-relaxed">
        {parts.map((part, index) => {
          const blankId = blankIds[index]
          return (
            <span key={index}>
              <span className="whitespace-pre-wrap"><MathText text={part} /></span>
              {index < blankIds.length && blankId && (
                <span className="inline-flex items-baseline mx-1">
                  <input
                    ref={(el) => {
                      inputRefs.current[blankId] = el
                    }}
                    type="text"
                    value={values[blankId] || ''}
                    onChange={(e) => onChange(blankId, e.target.value)}
                    onKeyDown={(e) => handleKeyDown(e, blankId)}
                    disabled={disabled}
                    className={clsx(
                      'inline-block w-24 px-2 py-1 text-center border-b-2 bg-transparent transition-colors',
                      'focus:outline-none',
                      getInputStyle(blankId)
                    )}
                    placeholder="___"
                  />
                </span>
              )}
            </span>
          )
        })}
      </div>

      {showCorrectAnswers && (
        <div className="mt-4 rounded-lg bg-gray-50 p-4">
          <h4 className="mb-2 text-sm font-semibold text-gray-700">정답:</h4>
          <div className="space-y-1">
            {blankIds.map((blankId) => {
              const userAnswer = values[blankId]?.trim()
              const correctAnswer = blankAnswers[blankId]?.answer
              const isCorrect =
                userAnswer?.toUpperCase() === correctAnswer?.toUpperCase()

              return (
                <div key={blankId} className="flex items-center gap-2 text-sm">
                  <span
                    className={clsx(
                      'font-medium',
                      isCorrect ? 'text-green-600' : 'text-red-600'
                    )}
                  >
                    {isCorrect ? '✓' : '✗'}
                  </span>
                  <span className="text-gray-600">빈칸 {blankIds.indexOf(blankId) + 1}:</span>
                  {!isCorrect && userAnswer && (
                    <span className="text-red-600 line-through">{userAnswer}</span>
                  )}
                  <span className="font-semibold text-gray-900">{correctAnswer}</span>
                </div>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}
