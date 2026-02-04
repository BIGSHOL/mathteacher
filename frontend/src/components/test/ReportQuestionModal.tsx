/**
 * 문제 신고 모달 컴포넌트.
 */

import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { createQuestionReport, type ReportType } from '../../services/reportService'

const REPORT_OPTIONS: { value: ReportType; label: string; description: string }[] = [
  { value: 'wrong_answer', label: '정답 오류', description: '정답이 틀립니다' },
  { value: 'wrong_options', label: '보기 오류', description: '보기 내용이 잘못되었습니다' },
  { value: 'question_error', label: '문제 오류', description: '문제 내용이 잘못되었습니다' },
  { value: 'other', label: '기타', description: '그 외 문제가 있습니다' },
]

interface ReportQuestionModalProps {
  isOpen: boolean
  questionId: string
  onClose: () => void
}

export function ReportQuestionModal({ isOpen, questionId, onClose }: ReportQuestionModalProps) {
  const [reportType, setReportType] = useState<ReportType | null>(null)
  const [comment, setComment] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [result, setResult] = useState<'success' | 'error' | null>(null)

  // ESC 키로 닫기
  useEffect(() => {
    if (!isOpen) return
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && !submitting) handleClose()
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [isOpen, submitting])

  const handleSubmit = async () => {
    if (!reportType || !comment.trim() || submitting) return
    setSubmitting(true)
    try {
      await createQuestionReport({
        question_id: questionId,
        report_type: reportType,
        comment: comment.trim(),
      })
      setResult('success')
    } catch {
      setResult('error')
    } finally {
      setSubmitting(false)
    }
  }

  const handleClose = () => {
    if (submitting) return
    setReportType(null)
    setComment('')
    setResult(null)
    onClose()
  }

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* 배경 */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[70] bg-black/50"
            onClick={handleClose}
          />

          {/* 모달 */}
          <motion.div
            role="dialog"
            aria-modal="true"
            aria-labelledby="report-modal-title"
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{ type: 'spring', duration: 0.4 }}
            className="fixed inset-x-4 top-1/2 z-[71] mx-auto max-w-md -translate-y-1/2 overflow-hidden rounded-2xl bg-white shadow-2xl"
          >
            {/* 결과 화면 */}
            {result ? (
              <div className="p-6 text-center">
                <div className="mb-3 text-5xl">
                  {result === 'success' ? '✅' : '❌'}
                </div>
                <h3 className="mb-2 text-lg font-bold text-gray-900">
                  {result === 'success' ? '신고가 접수되었습니다' : '신고 접수에 실패했습니다'}
                </h3>
                <p className="mb-6 text-sm text-gray-500">
                  {result === 'success'
                    ? '검토 후 처리 결과를 알려드리겠습니다.'
                    : '잠시 후 다시 시도해 주세요.'}
                </p>
                <div className="flex gap-3">
                  {result === 'error' && (
                    <button
                      onClick={() => setResult(null)}
                      className="flex-1 rounded-xl border border-gray-300 py-3 font-semibold text-gray-700 transition-colors hover:bg-gray-50"
                    >
                      다시 시도
                    </button>
                  )}
                  <button
                    onClick={handleClose}
                    className="flex-1 rounded-xl bg-brand-500 py-3 font-semibold text-white transition-colors hover:bg-brand-600"
                  >
                    확인
                  </button>
                </div>
              </div>
            ) : (
              <>
                {/* 헤더 */}
                <div className="flex items-center justify-between border-b px-5 py-4">
                  <h3 id="report-modal-title" className="text-lg font-bold text-gray-900">문제 신고</h3>
                  <button
                    onClick={handleClose}
                    aria-label="닫기"
                    className="rounded-lg p-1 text-gray-400 transition-colors hover:bg-gray-100 hover:text-gray-600"
                  >
                    <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>

                {/* 본문 */}
                <div className="p-5">
                  {/* 신고 유형 */}
                  <div className="mb-4">
                    <label className="mb-2 block text-sm font-medium text-gray-700">신고 유형</label>
                    <div className="grid grid-cols-2 gap-2">
                      {REPORT_OPTIONS.map((opt) => (
                        <button
                          key={opt.value}
                          type="button"
                          onClick={() => setReportType(opt.value)}
                          className={`rounded-xl border-2 px-3 py-2.5 text-left transition-all ${
                            reportType === opt.value
                              ? 'border-brand-500 bg-brand-50 text-brand-700'
                              : 'border-gray-200 bg-white text-gray-700 hover:border-gray-300'
                          }`}
                        >
                          <div className="text-sm font-semibold">{opt.label}</div>
                          <div className="mt-0.5 text-xs text-gray-500">{opt.description}</div>
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* 코멘트 */}
                  <div className="mb-5">
                    <label className="mb-2 block text-sm font-medium text-gray-700">
                      상세 내용 <span className="text-red-500">*</span>
                    </label>
                    <textarea
                      value={comment}
                      onChange={(e) => setComment(e.target.value)}
                      placeholder="어떤 문제가 있는지 설명해 주세요..."
                      maxLength={2000}
                      rows={3}
                      className="w-full resize-none rounded-xl border border-gray-300 px-4 py-3 text-sm transition-colors focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
                    />
                    <div className="mt-1 text-right text-xs text-gray-400">
                      {comment.length}/2000
                    </div>
                  </div>

                  {/* 제출 */}
                  <button
                    onClick={handleSubmit}
                    disabled={!reportType || !comment.trim() || submitting}
                    className="w-full rounded-xl bg-red-500 py-3 font-semibold text-white transition-colors hover:bg-red-600 disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    {submitting ? '접수 중...' : '신고 접수'}
                  </button>
                </div>
              </>
            )}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
