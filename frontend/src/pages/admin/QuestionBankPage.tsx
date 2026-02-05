// 문제 은행 페이지 (admin/master 전용)

import { useEffect, useState, useCallback, useRef, useMemo } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import api from '../../lib/api'
import type { Grade, QuestionCategory, QuestionType, ProblemPart, PaginatedResponse } from '../../types'

interface QuestionItem {
  id: string
  concept_id: string
  concept_name: string
  grade?: string
  chapter_name?: string
  category: QuestionCategory
  part: ProblemPart
  question_type: QuestionType
  difficulty: number
  content: string
  options?: { id: string; label: string; text: string }[]
  correct_answer: string
  explanation: string
  points: number
  blank_config?: Record<string, unknown>
}

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
}

const GRADE_OPTIONS: { value: Grade; label: string }[] = [
  { value: 'elementary_1', label: '초1' },
  { value: 'elementary_2', label: '초2' },
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

const CATEGORY_OPTIONS = [
  { value: 'computation', label: '연산' },
  { value: 'concept', label: '개념' },
]

const TYPE_OPTIONS = [
  { value: 'multiple_choice', label: '객관식' },
  { value: 'true_false', label: 'O/X' },
  { value: 'short_answer', label: '단답형' },
  { value: 'fill_in_blank', label: '빈칸채우기' },
]

const PART_OPTIONS = [
  { value: 'calc', label: '수와 연산' },
  { value: 'algebra', label: '문자와 식' },
  { value: 'func', label: '함수' },
  { value: 'geo', label: '도형' },
  { value: 'data', label: '자료와 확률' },
  { value: 'word', label: '서술형' },
]

const DIFFICULTY_OPTIONS = Array.from({ length: 10 }, (_, i) => ({
  value: i + 1,
  label: `Lv.${i + 1}`,
}))

const CATEGORY_BADGE: Record<string, string> = {
  computation: 'bg-blue-100 text-blue-700',
  concept: 'bg-emerald-100 text-emerald-700',
}

const TYPE_BADGE: Record<string, string> = {
  multiple_choice: 'bg-purple-100 text-purple-700',
  true_false: 'bg-amber-100 text-amber-700',
  short_answer: 'bg-pink-100 text-pink-700',
  fill_in_blank: 'bg-cyan-100 text-cyan-700',
}

const TYPE_LABEL: Record<string, string> = {
  multiple_choice: '객관식',
  true_false: 'O/X',
  short_answer: '단답형',
  fill_in_blank: '빈칸',
}

const CATEGORY_LABEL: Record<string, string> = {
  computation: '연산',
  concept: '개념',
}

const GRADE_LABEL: Record<string, string> = {
  elementary_1: '초1', elementary_2: '초2', elementary_3: '초3',
  elementary_4: '초4', elementary_5: '초5', elementary_6: '초6',
  middle_1: '중1', middle_2: '중2', middle_3: '중3',
  high_1: '공통수학1', high_2: '공통수학2',
}

// 학년별 실제 학기 구분 (2022 개정 교육과정 가이드 기반)
const SEMESTER_STRUCTURE: Record<string, { semester1: number[]; semester2: number[] } | null> = {
  elementary_3: { semester1: [1, 2, 3, 4, 5, 6], semester2: [7, 8, 9, 10, 11, 12] },
  elementary_4: { semester1: [1, 2, 3, 4, 5, 6], semester2: [7, 8, 9, 10, 11, 12] },
  elementary_5: { semester1: [1, 2, 3, 4, 5, 6], semester2: [7, 8, 9, 10, 11, 12] },
  elementary_6: { semester1: [1, 2, 3, 4, 5, 6], semester2: [7, 8, 9, 10, 11, 12] },
  middle_1: { semester1: [1, 2, 3], semester2: [4, 5, 6] },
  middle_2: { semester1: [1, 2, 3], semester2: [4, 5, 6] },
  middle_3: { semester1: [1, 2, 3, 4], semester2: [5, 6, 7] },
  high_1: null, // 공통수학1 - 학기 구분 없음
  high_2: null, // 공통수학2 - 학기 구분 없음
}

/** 단원 이름에서 선행 "N. " 접두사 제거 */
function stripChapterNum(name: string): string {
  return name.replace(/^\d+\.\s*/, '')
}

export function QuestionBankPage() {
  const [questions, setQuestions] = useState<QuestionItem[]>([])
  const [total, setTotal] = useState(0)
  const [totalPages, setTotalPages] = useState(0)
  const [page, setPage] = useState(1)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  // 필터
  const [gradeFilter, setGradeFilter] = useState<Grade | ''>('')
  const [categoryFilter, setCategoryFilter] = useState<QuestionCategory | ''>('')
  const [typeFilter, setTypeFilter] = useState<QuestionType | ''>('')
  const [partFilter, setPartFilter] = useState<ProblemPart | ''>('')
  const [difficultyFilter, setDifficultyFilter] = useState<number | ''>('')
  const [chapterFilter, setChapterFilter] = useState('')
  const [conceptFilter, setConceptFilter] = useState('')
  const [searchQuery, setSearchQuery] = useState('')

  // 동적 드롭다운 데이터
  const [chapters, setChapters] = useState<ChapterItem[]>([])
  const [concepts, setConcepts] = useState<ConceptItem[]>([])
  const [chaptersLoading, setChaptersLoading] = useState(false)
  const [conceptsLoading, setConceptsLoading] = useState(false)

  // 상세 모달
  const [selectedQuestion, setSelectedQuestion] = useState<QuestionItem | null>(null)

  // 검색어 디바운스
  const [debouncedSearch, setDebouncedSearch] = useState('')
  const searchTimerRef = useRef<ReturnType<typeof setTimeout>>()

  useEffect(() => {
    searchTimerRef.current = setTimeout(() => setDebouncedSearch(searchQuery), 300)
    return () => clearTimeout(searchTimerRef.current)
  }, [searchQuery])

  // 학년 전체 개념 목록 (캐시): 학년 변경 시 한 번 로드
  const allConceptsRef = useRef<ConceptItem[]>([])

  // 학년 변경 시 단원+개념 한 번에 로드 (단일 API 호출)
  useEffect(() => {
    setChapterFilter('')
    setConceptFilter('')
    if (gradeFilter) {
      const controller = new AbortController()
      setChaptersLoading(true)
      setConceptsLoading(true)
      api
        .get<{ success: boolean; data: { chapters: ChapterItem[]; concepts: ConceptItem[] } }>(
          `/api/v1/questions/filter-options?grade=${gradeFilter}`,
          { timeout: 10000, signal: controller.signal },
        )
        .then((res) => {
          setChapters(res.data.data.chapters)
          setConcepts(res.data.data.concepts)
          allConceptsRef.current = res.data.data.concepts
        })
        .catch(() => {
          if (!controller.signal.aborted) {
            setChapters([])
            setConcepts([])
            allConceptsRef.current = []
          }
        })
        .finally(() => {
          if (!controller.signal.aborted) {
            setChaptersLoading(false)
            setConceptsLoading(false)
          }
        })
      return () => controller.abort()
    } else {
      setChapters([])
      setConcepts([])
      allConceptsRef.current = []
      setChaptersLoading(false)
      setConceptsLoading(false)
    }
  }, [gradeFilter])

  // 단원 변경 시 개념 필터링 (로컬, API 호출 없음)
  useEffect(() => {
    setConceptFilter('')
    if (chapterFilter) {
      const ch = chapters.find((c) => c.id === chapterFilter)
      if (ch && ch.concept_ids.length > 0) {
        const ids = new Set(ch.concept_ids)
        setConcepts(allConceptsRef.current.filter((c) => ids.has(c.id)))
      } else {
        setConcepts([])
      }
    } else {
      // 단원 미선택 → 학년 전체 개념 복원
      setConcepts(allConceptsRef.current)
    }
  }, [chapterFilter, chapters])

  // 학기별 개념 그룹 (optgroup용)
  const conceptGroups = useMemo(() => {
    if (chapters.length === 0 || concepts.length === 0) return undefined
    if (chapterFilter) return undefined // 단원 선택 시 flat
    if (!gradeFilter) return undefined

    const conceptMap = new Map(concepts.map((c) => [c.id, c]))
    const semesterInfo = SEMESTER_STRUCTURE[gradeFilter]

    type Entry = { chNum: number; value: string; label: string }
    const entries: Entry[] = []
    const assigned = new Set<string>()

    // 단원별로 개념 매핑 및 표시 번호 결정
    for (const ch of chapters) {
      let displayNum = ch.chapter_number

      // 2학기 단원인 경우 표시 번호 재계산
      if (semesterInfo && semesterInfo.semester2.includes(ch.chapter_number)) {
        displayNum = semesterInfo.semester2.indexOf(ch.chapter_number) + 1
      }

      for (const cid of ch.concept_ids) {
        const c = conceptMap.get(cid)
        if (c) {
          entries.push({ chNum: ch.chapter_number, value: c.id, label: `${displayNum}. ${c.name}` })
          assigned.add(cid)
        }
      }
    }

    // 단원에 속하지 않은 개념들
    for (const c of concepts) {
      if (!assigned.has(c.id)) entries.push({ chNum: 999, value: c.id, label: c.name })
    }

    // 학기별 그룹 생성
    if (semesterInfo) {
      const s1Set = new Set(semesterInfo.semester1)
      const s2Set = new Set(semesterInfo.semester2)
      const s1 = entries.filter((e) => s1Set.has(e.chNum))
      const s2 = entries.filter((e) => s2Set.has(e.chNum))
      const etc = entries.filter((e) => e.chNum === 999)

      const groups: { label: string; options: { value: string; label: string }[] }[] = []
      if (s1.length > 0) groups.push({ label: '1학기', options: s1 })
      if (s2.length > 0) groups.push({ label: '2학기', options: s2 })
      if (etc.length > 0) groups.push({ label: '기타', options: etc })
      return groups.length > 0 ? groups : undefined
    }

    // 고등(공통수학1/2): 학기 구분 없음 → flat
    return undefined
  }, [chapters, concepts, chapterFilter, gradeFilter])

  // flat용 개념 옵션 (그룹 미적용 시: 단원 선택됨 or 고등)
  const conceptOptionsFlat = useMemo(() => {
    if (conceptGroups) return undefined // 그룹 사용 시 불필요
    if (concepts.length === 0) return []
    if (chapterFilter) {
      // 단원 선택 시: 단순 개념 이름만
      return concepts.map((c) => ({ value: c.id, label: c.name }))
    }
    // 고등: 단원번호 prefix
    const conceptToChNum = new Map<string, number>()
    for (const ch of chapters) {
      for (const cid of ch.concept_ids) conceptToChNum.set(cid, ch.chapter_number)
    }
    return concepts.map((c) => {
      const raw = conceptToChNum.get(c.id)
      const num = raw ? (raw <= 6 ? raw : raw - 6) : 0
      return { value: c.id, label: num > 0 ? `${num}. ${c.name}` : c.name }
    })
  }, [conceptGroups, concepts, chapters, chapterFilter])

  // 학기별 단원 그룹 (optgroup용)
  const chapterGroups = useMemo(() => {
    if (chapters.length === 0) return undefined
    if (!gradeFilter) return undefined

    const semesterInfo = SEMESTER_STRUCTURE[gradeFilter]
    if (!semesterInfo) {
      // 고등(공통수학1/2): 학기 구분 없음 → flat
      return undefined
    }

    // 실제 교육과정 기반 학기 구분
    const s1Set = new Set(semesterInfo.semester1)
    const s2Set = new Set(semesterInfo.semester2)
    const s1 = chapters.filter((ch) => s1Set.has(ch.chapter_number))
    const s2 = chapters.filter((ch) => s2Set.has(ch.chapter_number))

    const groups: { label: string; options: { value: string; label: string }[] }[] = []
    if (s1.length > 0) {
      groups.push({
        label: '1학기',
        options: s1.map((ch) => ({
          value: ch.id,
          label: `${ch.chapter_number}. ${stripChapterNum(ch.name)}`
        }))
      })
    }
    if (s2.length > 0) {
      // 2학기 번호 재정렬 (1부터 시작)
      groups.push({
        label: '2학기',
        options: s2.map((ch, idx) => ({
          value: ch.id,
          label: `${idx + 1}. ${stripChapterNum(ch.name)}`
        }))
      })
    }
    return groups.length > 0 ? groups : undefined
  }, [chapters, gradeFilter])

  // flat용 단원 옵션 (고등 등 그룹 미적용 시)
  const chapterOptionsFlat = useMemo(() => {
    if (chapterGroups) return undefined
    return chapters.map((ch) => ({ value: ch.id, label: `${ch.chapter_number}. ${stripChapterNum(ch.name)}` }))
  }, [chapterGroups, chapters])

  // 문제 목록 fetch
  const fetchRef = useRef(0)
  const fetchQuestionsRef = useRef<(targetPage: number) => Promise<void>>()

  const fetchQuestions = useCallback(async (targetPage: number) => {
    const fetchId = ++fetchRef.current
    try {
      setIsLoading(true)
      setError('')
      const params = new URLSearchParams({ page: targetPage.toString(), page_size: '30' })
      if (gradeFilter) params.append('grade', gradeFilter)
      if (categoryFilter) params.append('category', categoryFilter)
      if (typeFilter) params.append('question_type', typeFilter)
      if (partFilter) params.append('part', partFilter)
      if (difficultyFilter) params.append('difficulty', difficultyFilter.toString())
      if (chapterFilter) params.append('chapter_id', chapterFilter)
      if (conceptFilter) params.append('concept_id', conceptFilter)
      if (debouncedSearch.trim()) params.append('search', debouncedSearch.trim())

      const res = await api.get<{
        success: boolean
        data: PaginatedResponse<QuestionItem>
      }>(`/api/v1/questions?${params}`, { timeout: 15000 })

      if (fetchId !== fetchRef.current) return

      setQuestions(res.data.data.items)
      setTotal(res.data.data.total)
      setTotalPages(res.data.data.total_pages)
    } catch {
      if (fetchId !== fetchRef.current) return
      setError('문제 목록을 불러오는데 실패했습니다.')
    } finally {
      if (fetchId === fetchRef.current) setIsLoading(false)
    }
  }, [gradeFilter, categoryFilter, typeFilter, partFilter, difficultyFilter, chapterFilter, conceptFilter, debouncedSearch])
  fetchQuestionsRef.current = fetchQuestions

  // 필터 변경 → 페이지 1로 리셋 + fetch
  useEffect(() => {
    setPage(1)
    fetchQuestions(1)
  }, [fetchQuestions])

  // 페이지 변경 핸들러 (버튼 클릭 전용, effect 불필요)
  const handlePageChange = useCallback((newPage: number) => {
    setPage(newPage)
    fetchQuestionsRef.current?.(newPage)
  }, [])

  const resetFilters = () => {
    setGradeFilter('')
    setCategoryFilter('')
    setTypeFilter('')
    setPartFilter('')
    setDifficultyFilter('')
    setChapterFilter('')
    setConceptFilter('')
    setSearchQuery('')
    setDebouncedSearch('')
    setPage(1)
  }

  const hasActiveFilters =
    gradeFilter || categoryFilter || typeFilter || partFilter || difficultyFilter || chapterFilter || conceptFilter || searchQuery

  return (
    <div className="min-h-screen bg-gray-50 py-4 sm:py-6">
      <div className="container mx-auto max-w-7xl px-4 space-y-4">
        {/* 헤더 */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <div className="flex items-center justify-between">
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xl">📦</span>
                <h1 className="text-xl font-bold text-gray-900">문제 은행</h1>
                <span className="rounded-full bg-gray-200 px-2 py-0.5 text-xs font-medium text-gray-600">
                  {total}문제
                </span>
              </div>
              <p className="text-xs text-gray-500 mt-0.5 ml-8">시드 데이터의 모든 문제를 조회합니다</p>
            </div>
            {hasActiveFilters && (
              <button
                onClick={resetFilters}
                className="rounded-lg bg-gray-200 px-3 py-1.5 text-xs font-medium text-gray-600 hover:bg-gray-300 transition-colors"
              >
                필터 초기화
              </button>
            )}
          </div>
        </motion.div>

        {/* 필터 패널 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="rounded-xl bg-white p-4 shadow-sm"
        >
          <div className="grid gap-2.5 grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5">
            {/* 학년 */}
            <FilterSelect
              label="학년"
              value={gradeFilter}
              onChange={(v) => setGradeFilter(v as Grade | '')}
              options={GRADE_OPTIONS}
            />
            {/* 단원 */}
            <FilterSelect
              label="단원"
              value={chapterFilter}
              onChange={setChapterFilter}
              options={chapterOptionsFlat}
              groups={chapterGroups}
              disabled={!gradeFilter}
              loading={chaptersLoading}
            />
            {/* 개념 */}
            <FilterSelect
              label="개념"
              value={conceptFilter}
              onChange={setConceptFilter}
              options={conceptOptionsFlat}
              groups={conceptGroups}
              disabled={!gradeFilter}
              loading={conceptsLoading}
            />
            {/* 카테고리 */}
            <FilterSelect
              label="카테고리"
              value={categoryFilter}
              onChange={(v) => setCategoryFilter(v as QuestionCategory | '')}
              options={CATEGORY_OPTIONS}
            />
            {/* 유형 */}
            <FilterSelect
              label="문제 유형"
              value={typeFilter}
              onChange={(v) => setTypeFilter(v as QuestionType | '')}
              options={TYPE_OPTIONS}
            />
            {/* 파트 */}
            <FilterSelect
              label="파트"
              value={partFilter}
              onChange={(v) => setPartFilter(v as ProblemPart | '')}
              options={PART_OPTIONS}
            />
            {/* 난이도 */}
            <FilterSelect
              label="난이도"
              value={difficultyFilter}
              onChange={(v) => setDifficultyFilter(v ? Number(v) : '')}
              options={DIFFICULTY_OPTIONS}
            />
            {/* 검색 */}
            <div className="col-span-2 sm:col-span-1 lg:col-span-2">
              <label className="mb-1 block text-[10px] font-medium text-gray-500">내용 검색</label>
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="문제 내용으로 검색..."
                className="w-full rounded-lg border border-gray-200 px-3 py-1.5 text-sm focus:border-primary-400 focus:outline-none focus:ring-1 focus:ring-primary-400"
              />
            </div>
          </div>
        </motion.div>

        {/* 에러 */}
        {error && (
          <div className="rounded-lg bg-red-50 p-3 text-sm text-red-600">{error}</div>
        )}

        {/* 테이블 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="overflow-hidden rounded-xl bg-white shadow-sm"
        >
          {isLoading ? (
            <div className="flex items-center justify-center py-20">
              <div className="h-8 w-8 animate-spin rounded-full border-3 border-primary-500 border-t-transparent" />
            </div>
          ) : questions.length === 0 ? (
            <div className="py-20 text-center text-sm text-gray-400">
              {hasActiveFilters ? '조건에 맞는 문제가 없습니다.' : '문제가 없습니다.'}
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b bg-gray-50 text-left">
                    <th className="px-3 py-3 font-medium text-gray-600">학년</th>
                    <th className="px-3 py-3 font-medium text-gray-600">단원</th>
                    <th className="px-4 py-3 font-medium text-gray-600 w-[30%]">내용</th>
                    <th className="px-3 py-3 font-medium text-gray-600">개념</th>
                    <th className="px-3 py-3 font-medium text-gray-600">카테고리</th>
                    <th className="px-3 py-3 font-medium text-gray-600">유형</th>
                    <th className="px-3 py-3 font-medium text-gray-600 text-center">난이도</th>
                    <th className="px-3 py-3 font-medium text-gray-600">정답</th>
                  </tr>
                </thead>
                <tbody>
                  {questions.map((q, i) => (
                    <tr
                      key={q.id}
                      onClick={() => setSelectedQuestion(q)}
                      className={`cursor-pointer border-b transition-colors hover:bg-primary-50 ${
                        i % 2 === 0 ? 'bg-white' : 'bg-gray-50/50'
                      }`}
                    >
                      <td className="px-3 py-3">
                        {q.grade ? (
                          <span className="inline-block whitespace-nowrap rounded-full bg-indigo-100 px-2 py-0.5 text-[10px] font-medium text-indigo-700">
                            {GRADE_LABEL[q.grade] || q.grade}
                          </span>
                        ) : (
                          <span className="text-xs text-gray-400">-</span>
                        )}
                      </td>
                      <td className="px-3 py-3">
                        <span className="text-xs text-gray-600 line-clamp-1" title={q.chapter_name || ''}>
                          {q.chapter_name || '-'}
                        </span>
                      </td>
                      <td className="px-4 py-3">
                        <p className="line-clamp-2 text-gray-900">{q.content}</p>
                      </td>
                      <td className="px-3 py-3">
                        <span className="text-xs text-gray-600">{q.concept_name || '-'}</span>
                      </td>
                      <td className="px-3 py-3">
                        <span className={`inline-block rounded-full px-2 py-0.5 text-[10px] font-medium ${CATEGORY_BADGE[q.category] || 'bg-gray-100 text-gray-600'}`}>
                          {CATEGORY_LABEL[q.category] || q.category}
                        </span>
                      </td>
                      <td className="px-3 py-3">
                        <span className={`inline-block rounded-full px-2 py-0.5 text-[10px] font-medium ${TYPE_BADGE[q.question_type] || 'bg-gray-100 text-gray-600'}`}>
                          {TYPE_LABEL[q.question_type] || q.question_type}
                        </span>
                      </td>
                      <td className="px-3 py-3 text-center">
                        <span className="font-math text-xs font-bold text-gray-700">Lv.{q.difficulty}</span>
                      </td>
                      <td className="px-3 py-3">
                        <span className="text-xs font-medium text-green-700 bg-green-50 rounded px-1.5 py-0.5 max-w-[120px] truncate inline-block">
                          {q.correct_answer}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* 페이지네이션 */}
          {totalPages > 1 && (
            <div className="flex items-center justify-between border-t px-4 py-3">
              <span className="text-xs text-gray-500">
                {total}개 중 {(page - 1) * 30 + 1}-{Math.min(page * 30, total)}
              </span>
              <div className="flex gap-1">
                <button
                  onClick={() => handlePageChange(Math.max(1, page - 1))}
                  disabled={page <= 1}
                  className="rounded-lg border px-3 py-1 text-xs disabled:opacity-40 hover:bg-gray-50"
                >
                  이전
                </button>
                {Array.from({ length: Math.min(totalPages, 7) }, (_, i) => {
                  let p: number
                  if (totalPages <= 7) {
                    p = i + 1
                  } else if (page <= 4) {
                    p = i + 1
                  } else if (page >= totalPages - 3) {
                    p = totalPages - 6 + i
                  } else {
                    p = page - 3 + i
                  }
                  return (
                    <button
                      key={p}
                      onClick={() => handlePageChange(p)}
                      className={`rounded-lg px-3 py-1 text-xs font-medium ${
                        p === page
                          ? 'bg-primary-500 text-white'
                          : 'border hover:bg-gray-50'
                      }`}
                    >
                      {p}
                    </button>
                  )
                })}
                <button
                  onClick={() => handlePageChange(Math.min(totalPages, page + 1))}
                  disabled={page >= totalPages}
                  className="rounded-lg border px-3 py-1 text-xs disabled:opacity-40 hover:bg-gray-50"
                >
                  다음
                </button>
              </div>
            </div>
          )}
        </motion.div>
      </div>

      {/* 상세 모달 */}
      <AnimatePresence>
        {selectedQuestion && (
          <QuestionDetailModal
            question={selectedQuestion}
            onClose={() => setSelectedQuestion(null)}
          />
        )}
      </AnimatePresence>
    </div>
  )
}

// 필터 셀렉트 컴포넌트
function FilterSelect({
  label,
  value,
  onChange,
  options,
  groups,
  disabled,
  loading,
}: {
  label: string
  value: string | number
  onChange: (v: string) => void
  options?: { value: string | number; label: string }[]
  groups?: { label: string; options: { value: string | number; label: string }[] }[]
  disabled?: boolean
  loading?: boolean
}) {
  return (
    <div>
      <label className="mb-1 block text-[10px] font-medium text-gray-500">{label}</label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled || loading}
        className="w-full rounded-lg border border-gray-200 px-2.5 py-1.5 text-sm focus:border-primary-400 focus:outline-none focus:ring-1 focus:ring-primary-400 disabled:bg-gray-100 disabled:text-gray-400"
      >
        <option value="">{loading ? '불러오는 중...' : '전체'}</option>
        {groups
          ? groups.map((g) => (
              <optgroup key={g.label} label={g.label}>
                {g.options.map((o) => (
                  <option key={o.value} value={o.value}>{o.label}</option>
                ))}
              </optgroup>
            ))
          : options?.map((o) => (
              <option key={o.value} value={o.value}>{o.label}</option>
            ))}
      </select>
    </div>
  )
}

// 문제 상세 모달
function QuestionDetailModal({
  question: q,
  onClose,
}: {
  question: QuestionItem
  onClose: () => void
}) {
  return (
    <>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 bg-black/50"
        onClick={onClose}
      />
      <motion.div
        initial={{ opacity: 0, scale: 0.95, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.95, y: 20 }}
        className="fixed left-1/2 top-1/2 z-50 w-[92%] max-w-2xl -translate-x-1/2 -translate-y-1/2 rounded-2xl bg-white p-6 shadow-2xl max-h-[85vh] overflow-y-auto"
      >
        {/* 헤더 */}
        <div className="mb-4 flex items-start justify-between">
          <div className="flex flex-wrap items-center gap-2">
            <span className={`rounded-full px-2.5 py-0.5 text-xs font-medium ${CATEGORY_BADGE[q.category]}`}>
              {CATEGORY_LABEL[q.category]}
            </span>
            <span className={`rounded-full px-2.5 py-0.5 text-xs font-medium ${TYPE_BADGE[q.question_type]}`}>
              {TYPE_LABEL[q.question_type]}
            </span>
            <span className="rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium text-gray-600">
              Lv.{q.difficulty}
            </span>
            <span className="rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium text-gray-600">
              {q.points}점
            </span>
          </div>
          <button
            onClick={onClose}
            className="flex h-8 w-8 items-center justify-center rounded-lg text-gray-400 hover:bg-gray-100 hover:text-gray-600"
          >
            X
          </button>
        </div>

        {/* 학년 / 단원 */}
        {q.grade && (
          <div className="mb-2 flex items-center gap-2 text-xs text-gray-500">
            <span className="rounded bg-indigo-50 px-2 py-0.5 font-medium text-indigo-700">
              {GRADE_LABEL[q.grade] || q.grade}
            </span>
            {q.chapter_name && (
              <>
                <span className="text-gray-300">/</span>
                <span className="font-medium text-gray-700">{q.chapter_name}</span>
              </>
            )}
          </div>
        )}

        {/* 개념 */}
        {q.concept_name && (
          <div className="mb-3 text-xs text-gray-500">
            개념: <span className="font-medium text-gray-700">{q.concept_name}</span>
          </div>
        )}

        {/* 문제 내용 */}
        <div className="mb-4 rounded-lg bg-gray-50 p-4">
          <p className="whitespace-pre-wrap text-sm leading-relaxed text-gray-900">{q.content}</p>
        </div>

        {/* 선택지 */}
        {q.options && q.options.length > 0 && (
          <div className="mb-4 space-y-2">
            <p className="text-xs font-medium text-gray-500">선택지</p>
            {q.options.map((opt) => (
              <div
                key={opt.id}
                className={`rounded-lg border px-3 py-2 text-sm ${
                  opt.id === q.correct_answer
                    ? 'border-green-300 bg-green-50 font-medium text-green-800'
                    : 'border-gray-200 text-gray-700'
                }`}
              >
                <span className="mr-2 font-bold">{opt.label}.</span>
                {opt.text}
                {opt.id === q.correct_answer && (
                  <span className="ml-2 text-xs text-green-600">&#10003; 정답</span>
                )}
              </div>
            ))}
          </div>
        )}

        {/* 정답 (객관식 아닌 경우) */}
        {(!q.options || q.options.length === 0) && (
          <div className="mb-4">
            <p className="text-xs font-medium text-gray-500 mb-1">정답</p>
            <div className="rounded-lg border border-green-200 bg-green-50 px-3 py-2 text-sm font-medium text-green-800">
              {q.correct_answer}
            </div>
          </div>
        )}

        {/* 해설 */}
        {q.explanation && (
          <div className="mb-4">
            <p className="text-xs font-medium text-gray-500 mb-1">해설</p>
            <div className="rounded-lg bg-blue-50 px-3 py-2 text-sm text-gray-700 whitespace-pre-wrap">
              {q.explanation}
            </div>
          </div>
        )}

        {/* 메타 정보 */}
        <div className="border-t pt-3 text-[10px] text-gray-400">
          ID: {q.id} | concept_id: {q.concept_id}
        </div>
      </motion.div>
    </>
  )
}
