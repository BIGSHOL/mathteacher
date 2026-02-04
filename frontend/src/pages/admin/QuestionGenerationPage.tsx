// AI 문제 대량 생성 페이지 (master 전용)

import { useEffect, useState, useCallback, useMemo } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../../lib/api'
import {
  generateQuestionsAI,
  saveGeneratedQuestions,
  deriveFillBlank,
} from '../../services/questionService'
import type { Grade } from '../../types'

interface ChapterItem {
  id: string
  name: string
  grade: string
  chapter_number: number
  concept_ids: string[]
}

interface ConceptItem {
  id: string
  name: string
  grade: string
  category?: string
}

type Strategy = 'ai' | 'fb_derive'
type Step = 'config' | 'generating' | 'review' | 'saving' | 'done'

const GRADE_OPTIONS: { value: Grade; label: string }[] = [
  { value: 'elementary_3', label: '초3' },
  { value: 'elementary_4', label: '초4' },
  { value: 'elementary_5', label: '초5' },
  { value: 'elementary_6', label: '초6' },
  { value: 'middle_1', label: '중1' },
  { value: 'middle_2', label: '중2' },
  { value: 'middle_3', label: '중3' },
  { value: 'high_1', label: '고1' },
  { value: 'high_2', label: '고2' },
]

export function QuestionGenerationPage() {
  const navigate = useNavigate()

  // Step 관리
  const [step, setStep] = useState<Step>('config')
  const [error, setError] = useState('')

  // 전략 선택
  const [strategy, setStrategy] = useState<Strategy>('ai')

  // 설정
  const [grade, setGrade] = useState<Grade | ''>('')
  const [chapters, setChapters] = useState<ChapterItem[]>([])
  const [concepts, setConcepts] = useState<ConceptItem[]>([])
  const [conceptId, setConceptId] = useState('')
  const [questionType, setQuestionType] = useState('multiple_choice')
  const [count, setCount] = useState(10)
  const [diffMin, setDiffMin] = useState(1)
  const [diffMax, setDiffMax] = useState(10)
  const [maxPerMc, setMaxPerMc] = useState(3)

  // 생성 결과
  const [generated, setGenerated] = useState<Record<string, unknown>[]>([])
  const [selected, setSelected] = useState<Set<number>>(new Set())
  const [savedCount, setSavedCount] = useState(0)

  const [conceptsLoading, setConceptsLoading] = useState(false)

  // 학년 변경 시 단원+개념 한 번에 로드
  useEffect(() => {
    setConceptId('')
    if (grade) {
      const controller = new AbortController()
      setConceptsLoading(true)
      api
        .get<{ success: boolean; data: { chapters: ChapterItem[]; concepts: ConceptItem[] } }>(
          `/api/v1/questions/filter-options?grade=${grade}`,
          { timeout: 10000, signal: controller.signal },
        )
        .then((res) => {
          setChapters(res.data.data.chapters)
          setConcepts(res.data.data.concepts)
        })
        .catch(() => {
          if (!controller.signal.aborted) {
            setChapters([])
            setConcepts([])
          }
        })
        .finally(() => { if (!controller.signal.aborted) setConceptsLoading(false) })
      return () => controller.abort()
    } else {
      setChapters([])
      setConcepts([])
      setConceptsLoading(false)
    }
  }, [grade])

  // 학기별 개념 그룹 (초~중3: 1학기/2학기, 고등: 전체)
  const semesterGroups = useMemo(() => {
    if (chapters.length === 0 || concepts.length === 0) return []
    const conceptMap = new Map(concepts.map((c) => [c.id, c]))
    const useSemester = grade && !grade.startsWith('high_')

    // 단원별 개념 매핑 (chapter_number 순서 유지)
    type Entry = { chNum: number; chName: string; concept: ConceptItem }
    const entries: Entry[] = []
    const assigned = new Set<string>()
    for (const ch of chapters) {
      for (const cid of ch.concept_ids) {
        const c = conceptMap.get(cid)
        if (c) {
          entries.push({ chNum: ch.chapter_number, chName: ch.name, concept: c })
          assigned.add(cid)
        }
      }
    }
    // 미배정 개념
    for (const c of concepts) {
      if (!assigned.has(c.id)) entries.push({ chNum: 999, chName: '기타', concept: c })
    }

    if (useSemester) {
      const s1 = entries.filter((e) => e.chNum <= 6)
      const s2 = entries.filter((e) => e.chNum > 6 && e.chNum < 999)
      const etc = entries.filter((e) => e.chNum === 999)
      const groups: { label: string; items: Entry[] }[] = []
      if (s1.length > 0) groups.push({ label: '1학기', items: s1 })
      if (s2.length > 0) groups.push({ label: '2학기', items: s2 })
      if (etc.length > 0) groups.push({ label: '기타', items: etc })
      return groups
    }
    return [{ label: '전체', items: entries }]
  }, [chapters, concepts, grade])

  // 전체 선택/해제
  const toggleAll = useCallback(() => {
    if (selected.size === generated.length) {
      setSelected(new Set())
    } else {
      setSelected(new Set(generated.map((_, i) => i)))
    }
  }, [selected.size, generated.length])

  // 개별 선택/해제
  const toggleOne = useCallback((idx: number) => {
    setSelected((prev) => {
      const next = new Set(prev)
      if (next.has(idx)) next.delete(idx)
      else next.add(idx)
      return next
    })
  }, [])

  // AI 생성 실행
  const handleGenerate = async () => {
    if (!conceptId) {
      setError('개념을 선택하세요.')
      return
    }
    setError('')
    setStep('generating')

    try {
      if (strategy === 'ai') {
        const result = await generateQuestionsAI({
          concept_id: conceptId,
          count,
          question_type: questionType,
          difficulty_min: diffMin,
          difficulty_max: diffMax,
        })
        setGenerated(result.generated)
        setSelected(new Set(result.generated.map((_, i) => i)))
      } else {
        const result = await deriveFillBlank({
          concept_id: conceptId,
          max_per_mc: maxPerMc,
        })
        setGenerated(result.derived_questions)
        setSelected(new Set(result.derived_questions.map((_, i) => i)))
      }
      setStep('review')
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'AI 생성 실패'
      setError(msg)
      setStep('config')
    }
  }

  // 선택된 문제 저장
  const handleSave = async () => {
    const toSave = generated.filter((_, i) => selected.has(i))
    if (toSave.length === 0) {
      setError('저장할 문제를 선택하세요.')
      return
    }
    setError('')
    setStep('saving')

    try {
      const result = await saveGeneratedQuestions(toSave)
      setSavedCount(result.saved_count)
      setStep('done')
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : '저장 실패'
      setError(msg)
      setStep('review')
    }
  }

  // 선택한 개념 이름
  const selectedConceptName =
    concepts.find((c) => c.id === conceptId)?.name || ''

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-6">
      <div className="mx-auto max-w-5xl">
        {/* 헤더 */}
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              문제 대량 생성
            </h1>
            <p className="mt-1 text-sm text-gray-500">
              AI로 개념 문제를 생성하거나, MC에서 빈칸 문제를 파생합니다
            </p>
          </div>
          <button
            onClick={() => navigate('/admin/questions')}
            className="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            문제은행
          </button>
        </div>

        {/* Step 1: 설정 */}
        {(step === 'config' || step === 'generating') && (
          <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
            <h2 className="mb-4 text-lg font-semibold text-gray-800">
              생성 설정
            </h2>

            {/* 전략 선택 */}
            <div className="mb-5">
              <label className="mb-2 block text-sm font-medium text-gray-700">
                생성 전략
              </label>
              <div className="flex gap-3">
                <label
                  className={`flex cursor-pointer items-center gap-2 rounded-lg border-2 px-4 py-2.5 text-sm font-medium transition-colors ${
                    strategy === 'ai'
                      ? 'border-indigo-500 bg-indigo-50 text-indigo-700'
                      : 'border-gray-200 bg-white text-gray-600 hover:border-gray-300'
                  }`}
                >
                  <input
                    type="radio"
                    name="strategy"
                    value="ai"
                    checked={strategy === 'ai'}
                    onChange={() => setStrategy('ai')}
                    className="hidden"
                  />
                  AI 생성
                </label>
                <label
                  className={`flex cursor-pointer items-center gap-2 rounded-lg border-2 px-4 py-2.5 text-sm font-medium transition-colors ${
                    strategy === 'fb_derive'
                      ? 'border-indigo-500 bg-indigo-50 text-indigo-700'
                      : 'border-gray-200 bg-white text-gray-600 hover:border-gray-300'
                  }`}
                >
                  <input
                    type="radio"
                    name="strategy"
                    value="fb_derive"
                    checked={strategy === 'fb_derive'}
                    onChange={() => setStrategy('fb_derive')}
                    className="hidden"
                  />
                  FB 파생
                </label>
              </div>
            </div>

            {/* 학년 + 개념 */}
            <div className="mb-4 grid grid-cols-1 gap-4 md:grid-cols-2">
              <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                  학년
                </label>
                <select
                  value={grade}
                  onChange={(e) => setGrade(e.target.value as Grade)}
                  className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:ring-indigo-500"
                >
                  <option value="">선택</option>
                  {GRADE_OPTIONS.map((g) => (
                    <option key={g.value} value={g.value}>
                      {g.label}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                  개념
                </label>
                <select
                  value={conceptId}
                  onChange={(e) => setConceptId(e.target.value)}
                  className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:ring-indigo-500"
                  disabled={!grade || conceptsLoading}
                >
                  <option value="">
                    {conceptsLoading ? '불러오는 중...' : grade ? '개념 선택' : '학년을 먼저 선택'}
                  </option>
                  {semesterGroups.map((g) => (
                    <optgroup key={g.label} label={g.label}>
                      {g.items.map((e) => {
                        const displayNum = e.chNum <= 6 ? e.chNum : e.chNum < 999 ? e.chNum - 6 : 0
                        return (
                          <option key={e.concept.id} value={e.concept.id}>
                            {displayNum > 0 ? `${displayNum}. ${e.concept.name}` : e.concept.name}
                          </option>
                        )
                      })}
                    </optgroup>
                  ))}
                </select>
              </div>
            </div>

            {/* AI 전략 옵션 */}
            {strategy === 'ai' && (
              <div className="mb-4 grid grid-cols-1 gap-4 md:grid-cols-3">
                <div>
                  <label className="mb-1 block text-sm font-medium text-gray-700">
                    문제 유형
                  </label>
                  <select
                    value={questionType}
                    onChange={(e) => setQuestionType(e.target.value)}
                    className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
                  >
                    <option value="multiple_choice">객관식 (MC)</option>
                    <option value="fill_in_blank">빈칸 채우기 (FB)</option>
                  </select>
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium text-gray-700">
                    생성 수량
                  </label>
                  <select
                    value={count}
                    onChange={(e) => setCount(Number(e.target.value))}
                    className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
                  >
                    {[5, 10, 20, 30, 50].map((n) => (
                      <option key={n} value={n}>
                        {n}문제
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium text-gray-700">
                    난이도 범위
                  </label>
                  <div className="flex items-center gap-2">
                    <select
                      value={diffMin}
                      onChange={(e) => setDiffMin(Number(e.target.value))}
                      className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
                    >
                      {Array.from({ length: 10 }, (_, i) => i + 1).map((n) => (
                        <option key={n} value={n}>
                          Lv.{n}
                        </option>
                      ))}
                    </select>
                    <span className="text-gray-400">~</span>
                    <select
                      value={diffMax}
                      onChange={(e) => setDiffMax(Number(e.target.value))}
                      className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
                    >
                      {Array.from({ length: 10 }, (_, i) => i + 1).map((n) => (
                        <option key={n} value={n}>
                          Lv.{n}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>
            )}

            {/* FB 파생 옵션 */}
            {strategy === 'fb_derive' && (
              <div className="mb-4">
                <label className="mb-1 block text-sm font-medium text-gray-700">
                  MC 1문제당 최대 파생 수
                </label>
                <select
                  value={maxPerMc}
                  onChange={(e) => setMaxPerMc(Number(e.target.value))}
                  className="w-48 rounded-lg border border-gray-300 px-3 py-2 text-sm"
                >
                  {[1, 2, 3, 4, 5].map((n) => (
                    <option key={n} value={n}>
                      {n}개
                    </option>
                  ))}
                </select>
              </div>
            )}

            {error && (
              <div className="mb-4 rounded-lg bg-red-50 p-3 text-sm text-red-600">
                {error}
              </div>
            )}

            <button
              onClick={handleGenerate}
              disabled={step === 'generating' || !conceptId}
              className="mt-2 rounded-lg bg-indigo-600 px-6 py-2.5 text-sm font-medium text-white hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {step === 'generating' ? (
                <span className="flex items-center gap-2">
                  <svg
                    className="h-4 w-4 animate-spin"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    />
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                    />
                  </svg>
                  {strategy === 'ai' ? 'AI 생성중...' : 'FB 파생중...'}
                </span>
              ) : strategy === 'ai' ? (
                'AI 생성하기'
              ) : (
                'FB 파생하기'
              )}
            </button>
          </div>
        )}

        {/* Step 2: 검토 */}
        {step === 'review' && (
          <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-lg font-semibold text-gray-800">
                생성 결과 검토
                <span className="ml-2 rounded-full bg-indigo-100 px-2.5 py-0.5 text-sm text-indigo-700">
                  {generated.length}문제
                </span>
                {selectedConceptName && (
                  <span className="ml-2 text-sm font-normal text-gray-500">
                    - {selectedConceptName}
                  </span>
                )}
              </h2>
              <div className="flex gap-2">
                <button
                  onClick={() => {
                    setStep('config')
                    setGenerated([])
                    setSelected(new Set())
                  }}
                  className="rounded-lg border border-gray-300 bg-white px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-50"
                >
                  다시 설정
                </button>
              </div>
            </div>

            {error && (
              <div className="mb-4 rounded-lg bg-red-50 p-3 text-sm text-red-600">
                {error}
              </div>
            )}

            {/* 테이블 */}
            <div className="mb-4 max-h-[60vh] overflow-auto rounded-lg border border-gray-200">
              <table className="w-full table-fixed text-left text-sm">
                <colgroup>
                  <col className="w-10" />
                  <col className="w-10" />
                  <col />
                  <col className="w-20" />
                  <col className="w-16" />
                  <col className="w-32" />
                </colgroup>
                <thead className="sticky top-0 bg-gray-50">
                  <tr>
                    <th className="px-3 py-2">
                      <input
                        type="checkbox"
                        checked={selected.size === generated.length}
                        onChange={toggleAll}
                        className="rounded border-gray-300"
                      />
                    </th>
                    <th className="px-3 py-2 text-gray-600">#</th>
                    <th className="px-3 py-2 text-gray-600">문제 내용</th>
                    <th className="px-3 py-2 text-gray-600">유형</th>
                    <th className="px-3 py-2 text-gray-600">난이도</th>
                    <th className="px-3 py-2 text-gray-600">정답</th>
                  </tr>
                </thead>
                <tbody>
                  {generated.map((q, idx) => (
                    <tr
                      key={idx}
                      className={`border-t border-gray-100 ${
                        selected.has(idx)
                          ? 'bg-indigo-50/50'
                          : 'hover:bg-gray-50'
                      }`}
                    >
                      <td className="px-3 py-2">
                        <input
                          type="checkbox"
                          checked={selected.has(idx)}
                          onChange={() => toggleOne(idx)}
                          className="rounded border-gray-300"
                        />
                      </td>
                      <td className="px-3 py-2 text-gray-400">{idx + 1}</td>
                      <td className="px-3 py-2">
                        <div className="line-clamp-2 text-gray-800">
                          {String(q.content || '')}
                        </div>
                      </td>
                      <td className="whitespace-nowrap px-3 py-2">
                        <span
                          className={`rounded-full px-2 py-0.5 text-xs font-medium ${
                            q.question_type === 'fill_in_blank'
                              ? 'bg-cyan-100 text-cyan-700'
                              : 'bg-purple-100 text-purple-700'
                          }`}
                        >
                          {q.question_type === 'fill_in_blank'
                            ? '빈칸'
                            : '객관식'}
                        </span>
                      </td>
                      <td className="whitespace-nowrap px-3 py-2">
                        <span className="rounded bg-gray-100 px-1.5 py-0.5 text-xs font-medium text-gray-600">
                          Lv.{String(q.difficulty || '?')}
                        </span>
                      </td>
                      <td className="truncate px-3 py-2 font-mono text-xs text-gray-600">
                        {String(q.correct_answer || '')}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* 액션 버튼 */}
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-500">
                {selected.size}개 선택됨
              </span>
              <button
                onClick={handleSave}
                disabled={selected.size === 0}
                className="rounded-lg bg-green-600 px-6 py-2.5 text-sm font-medium text-white hover:bg-green-700 disabled:cursor-not-allowed disabled:opacity-50"
              >
                선택한 {selected.size}개 저장
              </button>
            </div>
          </div>
        )}

        {/* 저장 중 */}
        {step === 'saving' && (
          <div className="flex flex-col items-center justify-center rounded-xl border border-gray-200 bg-white p-12 shadow-sm">
            <svg
              className="mb-4 h-8 w-8 animate-spin text-indigo-600"
              viewBox="0 0 24 24"
              fill="none"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
              />
            </svg>
            <p className="text-gray-600">저장 중...</p>
          </div>
        )}

        {/* Step 3: 완료 */}
        {step === 'done' && (
          <div className="flex flex-col items-center justify-center rounded-xl border border-gray-200 bg-white p-12 shadow-sm">
            <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-green-100">
              <svg
                className="h-8 w-8 text-green-600"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth="2"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M4.5 12.75l6 6 9-13.5"
                />
              </svg>
            </div>
            <h2 className="mb-2 text-xl font-bold text-gray-900">
              {savedCount}개 문제 저장 완료
            </h2>
            <p className="mb-6 text-sm text-gray-500">
              문제 은행에서 확인할 수 있습니다
            </p>
            <div className="flex gap-3">
              <button
                onClick={() => navigate('/admin/questions')}
                className="rounded-lg border border-gray-300 bg-white px-5 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
              >
                문제은행으로
              </button>
              <button
                onClick={() => {
                  setStep('config')
                  setGenerated([])
                  setSelected(new Set())
                  setSavedCount(0)
                  setError('')
                }}
                className="rounded-lg bg-indigo-600 px-5 py-2 text-sm font-medium text-white hover:bg-indigo-700"
              >
                추가 생성
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
