// 학생용 도움말 페이지

import { useState } from 'react'
import { Link } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'

interface SectionProps {
  id: string
  icon: string
  title: string
  isOpen: boolean
  onToggle: () => void
  children: React.ReactNode
}

function Section({ icon, title, isOpen, onToggle, children }: SectionProps) {
  return (
    <div className="overflow-hidden rounded-2xl bg-white shadow-sm">
      <button
        onClick={onToggle}
        className="flex w-full items-center justify-between px-6 py-5 text-left transition-colors hover:bg-gray-50"
      >
        <div className="flex items-center gap-3">
          <span className="text-2xl">{icon}</span>
          <span className="text-lg font-semibold text-gray-900">{title}</span>
        </div>
        <motion.span
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ duration: 0.2 }}
          className="text-gray-400"
        >
          <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" clipRule="evenodd" />
          </svg>
        </motion.span>
      </button>
      <AnimatePresence initial={false}>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25 }}
          >
            <div className="border-t border-gray-100 px-6 py-5 text-gray-700 leading-relaxed">
              {children}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

function StepItem({ number, children }: { number: number; children: React.ReactNode }) {
  return (
    <div className="flex gap-3">
      <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-primary-100 text-sm font-bold text-primary-600">
        {number}
      </span>
      <div className="pt-0.5">{children}</div>
    </div>
  )
}

function Tip({ children }: { children: React.ReactNode }) {
  return (
    <div className="mt-4 rounded-xl bg-amber-50 border border-amber-200 px-4 py-3 text-sm text-amber-800">
      <span className="font-semibold">TIP</span> {children}
    </div>
  )
}

function NavButton({ to, label, icon }: { to: string; label: string; icon: string }) {
  return (
    <Link
      to={to}
      className="inline-flex items-center gap-1.5 rounded-lg bg-primary-50 px-3 py-1.5 text-sm font-medium text-primary-700 transition-colors hover:bg-primary-100"
    >
      <span>{icon}</span>
      <span>{label}</span>
    </Link>
  )
}

export function HelpPage() {
  const [openSections, setOpenSections] = useState<Set<string>>(new Set(['overview']))

  const toggleSection = (id: string) => {
    setOpenSections((prev) => {
      const next = new Set(prev)
      if (next.has(id)) {
        next.delete(id)
      } else {
        next.add(id)
      }
      return next
    })
  }

  const expandAll = () => {
    setOpenSections(new Set([
      'overview', 'login', 'test-list', 'test-play', 'result',
      'practice', 'review', 'stats', 'level', 'adaptive', 'tips',
    ]))
  }

  const collapseAll = () => {
    setOpenSections(new Set())
  }

  return (
    <div className="min-h-screen bg-gray-50 py-6 sm:py-8">
      <div className="container mx-auto max-w-3xl px-4 space-y-5">
        {/* 헤더 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="flex items-center gap-3 mb-1">
            <span className="text-3xl">📖</span>
            <h1 className="text-3xl font-bold text-gray-900">도움말</h1>
          </div>
          <p className="text-gray-500 ml-12">처음 사용하는 학생도 쉽게 따라할 수 있는 가이드</p>
          <div className="mt-3 ml-12 flex gap-2">
            <button
              onClick={expandAll}
              className="rounded-lg bg-gray-100 px-3 py-1.5 text-xs font-medium text-gray-600 hover:bg-gray-200 transition-colors"
            >
              모두 펼치기
            </button>
            <button
              onClick={collapseAll}
              className="rounded-lg bg-gray-100 px-3 py-1.5 text-xs font-medium text-gray-600 hover:bg-gray-200 transition-colors"
            >
              모두 접기
            </button>
          </div>
        </motion.div>

        {/* 전체 흐름 한눈에 보기 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.05 }}
        >
          <Section
            id="overview"
            icon="🗺️"
            title="전체 흐름 한눈에 보기"
            isOpen={openSections.has('overview')}
            onToggle={() => toggleSection('overview')}
          >
            <p className="mb-4">이 앱에서 수학 공부하는 전체 흐름이에요.</p>
            <div className="flex flex-col gap-2">
              <div className="flex items-center gap-2 rounded-xl bg-gray-50 px-4 py-3">
                <span className="text-lg">1️⃣</span>
                <span><b>로그인</b> - 선생님이 알려준 이메일과 비밀번호로 접속</span>
              </div>
              <div className="flex items-center gap-2 rounded-xl bg-gray-50 px-4 py-3">
                <span className="text-lg">2️⃣</span>
                <span><b>테스트 선택</b> - 테스트 목록에서 풀 문제 고르기</span>
              </div>
              <div className="flex items-center gap-2 rounded-xl bg-gray-50 px-4 py-3">
                <span className="text-lg">3️⃣</span>
                <span><b>문제 풀기</b> - 제한시간 안에 정답 고르기</span>
              </div>
              <div className="flex items-center gap-2 rounded-xl bg-gray-50 px-4 py-3">
                <span className="text-lg">4️⃣</span>
                <span><b>결과 확인</b> - 점수와 등급, XP 획득</span>
              </div>
              <div className="flex items-center gap-2 rounded-xl bg-gray-50 px-4 py-3">
                <span className="text-lg">5️⃣</span>
                <span><b>복습 & 반복</b> - 틀린 문제 복습하고 다시 도전</span>
              </div>
            </div>
          </Section>
        </motion.div>

        {/* 1. 로그인하기 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <Section
            id="login"
            icon="🔐"
            title="1. 로그인하기"
            isOpen={openSections.has('login')}
            onToggle={() => toggleSection('login')}
          >
            <div className="space-y-3">
              <StepItem number={1}>
                <p>앱에 접속하면 로그인 화면이 나옵니다.</p>
              </StepItem>
              <StepItem number={2}>
                <p>선생님이 알려준 <b>이메일</b>과 <b>비밀번호</b>를 입력하세요.</p>
              </StepItem>
              <StepItem number={3}>
                <p><b>로그인</b> 버튼을 누르면 테스트 목록으로 이동합니다.</p>
              </StepItem>
            </div>
            <Tip>
              비밀번호를 잊었다면 선생님에게 문의하세요.
            </Tip>
          </Section>
        </motion.div>

        {/* 2. 테스트 목록 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15 }}
        >
          <Section
            id="test-list"
            icon="📋"
            title="2. 테스트 고르기"
            isOpen={openSections.has('test-list')}
            onToggle={() => toggleSection('test-list')}
          >
            <p className="mb-4">로그인하면 가장 먼저 보이는 화면이에요.</p>
            <div className="space-y-3">
              <StepItem number={1}>
                <p>하단의 <b>테스트</b> 탭(또는 상단 메뉴)을 눌러 테스트 목록으로 이동하세요.</p>
              </StepItem>
              <StepItem number={2}>
                <p>상단 필터로 유형을 선택할 수 있어요.</p>
                <div className="mt-2 flex flex-wrap gap-2">
                  <span className="rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-700">📋 전체</span>
                  <span className="rounded-full bg-rose-100 px-3 py-1 text-xs font-medium text-rose-700">🧮 연산</span>
                  <span className="rounded-full bg-blue-100 px-3 py-1 text-xs font-medium text-blue-700">📚 개념</span>
                </div>
              </StepItem>
              <StepItem number={3}>
                <p>각 테스트 카드에는 다음 정보가 표시됩니다.</p>
                <ul className="mt-2 space-y-1 text-sm text-gray-600">
                  <li>- <b>문제 수</b>: 몇 문제인지</li>
                  <li>- <b>제한 시간</b>: 시간이 있는 테스트인지</li>
                  <li>- <b>적응형</b> 뱃지: 난이도가 자동 조절되는 테스트</li>
                  <li>- <b>완료</b> 뱃지: 이미 풀어본 테스트</li>
                  <li>- <b>최고 점수</b>: 이전에 가장 잘한 기록</li>
                </ul>
              </StepItem>
              <StepItem number={4}>
                <p><b>시작하기</b>(또는 <b>다시 풀기</b>) 버튼을 눌러 테스트를 선택하세요.</p>
              </StepItem>
            </div>
            <div className="mt-4">
              <NavButton to="/tests" label="테스트 목록 바로가기" icon="📝" />
            </div>
          </Section>
        </motion.div>

        {/* 3. 문제 풀기 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <Section
            id="test-play"
            icon="✏️"
            title="3. 문제 풀기"
            isOpen={openSections.has('test-play')}
            onToggle={() => toggleSection('test-play')}
          >
            <p className="mb-4">테스트를 선택하면 안내 화면이 나오고, <b>테스트 시작하기</b>를 누르면 문제 풀이가 시작됩니다.</p>

            <h4 className="font-semibold text-gray-900 mb-2">문제 풀이 화면 구성</h4>
            <div className="mb-4 space-y-2 text-sm">
              <div className="flex items-center gap-2 rounded-lg bg-gray-50 px-3 py-2">
                <span className="font-semibold text-gray-700 w-24 shrink-0">상단 바</span>
                <span>테스트 이름, 진행률(몇 번째 문제인지), 점수, 콤보</span>
              </div>
              <div className="flex items-center gap-2 rounded-lg bg-gray-50 px-3 py-2">
                <span className="font-semibold text-gray-700 w-24 shrink-0">카운트다운</span>
                <span>연산 20초, 개념 60초 - 시간 안에 풀어야 해요</span>
              </div>
              <div className="flex items-center gap-2 rounded-lg bg-gray-50 px-3 py-2">
                <span className="font-semibold text-gray-700 w-24 shrink-0">문제 영역</span>
                <span>문제 내용과 보기(4지선다 또는 빈칸 채우기)</span>
              </div>
              <div className="flex items-center gap-2 rounded-lg bg-gray-50 px-3 py-2">
                <span className="font-semibold text-gray-700 w-24 shrink-0">제출 버튼</span>
                <span>답을 고른 뒤 "정답 확인" 버튼 클릭</span>
              </div>
            </div>

            <h4 className="font-semibold text-gray-900 mb-2">풀이 순서</h4>
            <div className="space-y-3">
              <StepItem number={1}>
                <p>문제를 읽고 <b>보기 중 하나를 선택</b>하세요. (빈칸 채우기면 답을 직접 입력)</p>
              </StepItem>
              <StepItem number={2}>
                <p><b>정답 확인</b> 버튼을 누르세요.</p>
              </StepItem>
              <StepItem number={3}>
                <p>정답/오답 결과가 바로 나타나요. 해설도 함께 표시됩니다.</p>
              </StepItem>
              <StepItem number={4}>
                <p><b>다음 문제</b> 버튼을 눌러 다음으로 넘어가세요.</p>
              </StepItem>
            </div>

            <div className="mt-4 rounded-xl bg-red-50 border border-red-200 px-4 py-3 text-sm text-red-700">
              <span className="font-semibold">주의</span> 중간에 브라우저를 닫거나 뒤로 가면 <b>진행 상황이 저장되지 않아요</b>. 끝까지 풀어주세요!
            </div>

            <Tip>
              시간이 다 되면 자동으로 제출됩니다. 서두르되 침착하게 풀어보세요.
            </Tip>
          </Section>
        </motion.div>

        {/* 4. 결과 확인 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.25 }}
        >
          <Section
            id="result"
            icon="🏆"
            title="4. 결과 확인하기"
            isOpen={openSections.has('result')}
            onToggle={() => toggleSection('result')}
          >
            <p className="mb-4">마지막 문제까지 풀면 결과 화면이 나타나요.</p>

            <h4 className="font-semibold text-gray-900 mb-2">결과 화면에서 볼 수 있는 것</h4>
            <div className="space-y-2 text-sm">
              <div className="rounded-lg bg-gray-50 px-4 py-3">
                <b>등급</b> - 정답률에 따라 A+ ~ D 등급이 매겨져요
                <div className="mt-2 flex flex-wrap gap-2">
                  <span className="rounded-full bg-purple-100 px-2 py-0.5 text-xs text-purple-700">A+ (90%+)</span>
                  <span className="rounded-full bg-primary-100 px-2 py-0.5 text-xs text-primary-700">A (80%+)</span>
                  <span className="rounded-full bg-blue-100 px-2 py-0.5 text-xs text-blue-700">B (70%+)</span>
                  <span className="rounded-full bg-yellow-100 px-2 py-0.5 text-xs text-yellow-700">C (60%+)</span>
                  <span className="rounded-full bg-gray-200 px-2 py-0.5 text-xs text-gray-700">D (60% 미만)</span>
                </div>
              </div>
              <div className="rounded-lg bg-gray-50 px-4 py-3">
                <b>정답/오답 수</b> - 몇 개를 맞추고 틀렸는지 한눈에 확인
              </div>
              <div className="rounded-lg bg-gray-50 px-4 py-3">
                <b>최대 콤보</b> - 연속 정답 최고 기록
              </div>
              <div className="rounded-lg bg-gray-50 px-4 py-3">
                <b>획득 XP</b> - 이번 테스트로 얻은 경험치
              </div>
              <div className="rounded-lg bg-gray-50 px-4 py-3">
                <b>오답 노트</b> - 틀린 문제들을 바로 확인할 수 있어요
              </div>
            </div>

            <Tip>
              정답률 80% 이상이면 폭죽 효과가 터져요! 목표로 삼아보세요.
            </Tip>
          </Section>
        </motion.div>

        {/* 5. 빠른 연습 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <Section
            id="practice"
            icon="🚀"
            title="5. 빠른 연습"
            isOpen={openSections.has('practice')}
            onToggle={() => toggleSection('practice')}
          >
            <p className="mb-4">선생님이 만든 테스트 외에, 직접 설정해서 연습할 수도 있어요.</p>
            <div className="space-y-3">
              <StepItem number={1}>
                <p><b>유형 선택</b> - 연산(빠른 계산) 또는 개념(이해도 확인) 중 선택</p>
              </StepItem>
              <StepItem number={2}>
                <p><b>문제 수</b> - 10문제, 15문제, 20문제 중 고르기</p>
              </StepItem>
              <StepItem number={3}>
                <p><b>시작 난이도</b> - Lv.1(쉬움) ~ Lv.10(어려움) 중 선택. 내 레벨에 맞게 기본 설정되어 있어요.</p>
              </StepItem>
              <StepItem number={4}>
                <p><b>연습 시작하기</b>를 누르면 적응형 테스트가 시작됩니다.</p>
              </StepItem>
            </div>
            <Tip>
              빠른 연습은 항상 적응형이에요. 맞추면 난이도가 올라가고, 틀리면 내려갑니다.
            </Tip>
            <div className="mt-4">
              <NavButton to="/practice" label="빠른 연습 바로가기" icon="🚀" />
            </div>
          </Section>
        </motion.div>

        {/* 6. 복습하기 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.35 }}
        >
          <Section
            id="review"
            icon="🔄"
            title="6. 복습하기"
            isOpen={openSections.has('review')}
            onToggle={() => toggleSection('review')}
          >
            <p className="mb-4">이전에 틀렸던 문제를 다시 풀어볼 수 있어요.</p>
            <div className="space-y-3">
              <StepItem number={1}>
                <p>복습 페이지에 들어가면 <b>틀렸던 문제 목록</b>이 나옵니다.</p>
              </StepItem>
              <StepItem number={2}>
                <p>각 문제 옆에 <b>몇 번 틀렸는지</b>와 <b>지난번 선택한 답</b>이 표시돼요.</p>
              </StepItem>
              <StepItem number={3}>
                <p>다시 풀어본 뒤 <b>정답 확인</b>을 누르면 해설과 함께 결과를 볼 수 있어요.</p>
              </StepItem>
            </div>
            <Tip>
              틀린 문제가 없으면 "완벽해요!" 화면이 나옵니다. 계속 도전해보세요!
            </Tip>
            <div className="mt-4">
              <NavButton to="/review" label="복습 바로가기" icon="🔄" />
            </div>
          </Section>
        </motion.div>

        {/* 7. 내 통계 보기 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <Section
            id="stats"
            icon="📊"
            title="7. 내 통계 보기"
            isOpen={openSections.has('stats')}
            onToggle={() => toggleSection('stats')}
          >
            <p className="mb-4">내 학습 현황을 숫자로 한눈에 확인할 수 있어요.</p>

            <h4 className="font-semibold text-gray-900 mb-2">통계 화면 구성</h4>
            <div className="space-y-2 text-sm">
              <div className="rounded-lg bg-purple-50 px-4 py-3">
                <b>레벨 카드</b> - 현재 레벨(Lv.?)과 총 XP, 다음 레벨까지 남은 XP
              </div>
              <div className="rounded-lg bg-orange-50 px-4 py-3">
                <b>스트릭 카드</b> - 연속 학습 일수와 최대 기록
              </div>
              <div className="rounded-lg bg-primary-50 px-4 py-3">
                <b>정답률</b> - 전체 정답률 + 우수/보통/도전 등급
              </div>
              <div className="rounded-lg bg-gray-50 px-4 py-3">
                <b>학습 현황</b> - 완료 테스트, 풀이 문제 수, 정답 수, 평균 풀이 시간
              </div>
              <div className="rounded-lg bg-blue-50 px-4 py-3">
                <b>트랙별 성적</b> - 연산/개념 각각의 정답률
              </div>
              <div className="rounded-lg bg-red-50 px-4 py-3">
                <b>취약 개념</b> - 정답률 60% 미만인 개념 (더 연습 필요!)
              </div>
              <div className="rounded-lg bg-green-50 px-4 py-3">
                <b>강점 개념</b> - 정답률이 높은 개념 (잘하고 있어요!)
              </div>
            </div>
            <Tip>
              테스트를 풀수록 통계가 정확해져요. 처음엔 비어있을 수 있습니다.
            </Tip>
            <div className="mt-4">
              <NavButton to="/my-stats" label="내 통계 바로가기" icon="📊" />
            </div>
          </Section>
        </motion.div>

        {/* 8. 레벨 & XP 시스템 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.45 }}
        >
          <Section
            id="level"
            icon="⭐"
            title="8. 레벨과 XP 시스템"
            isOpen={openSections.has('level')}
            onToggle={() => toggleSection('level')}
          >
            <p className="mb-4">문제를 풀면 <b>XP(경험치)</b>를 얻고, XP가 쌓이면 <b>레벨</b>이 올라갑니다.</p>

            <h4 className="font-semibold text-gray-900 mb-2">XP를 얻는 방법</h4>
            <div className="mb-4 space-y-2 text-sm">
              <div className="flex items-center gap-2 rounded-lg bg-gray-50 px-4 py-3">
                <span className="text-lg">✅</span>
                <span><b>정답</b> - 문제를 맞추면 기본 XP 획득</span>
              </div>
              <div className="flex items-center gap-2 rounded-lg bg-gray-50 px-4 py-3">
                <span className="text-lg">⚡</span>
                <span><b>빠른 풀이</b> - 시간 안에 빨리 풀면 시간 보너스 XP 추가</span>
              </div>
              <div className="flex items-center gap-2 rounded-lg bg-gray-50 px-4 py-3">
                <span className="text-lg">🔥</span>
                <span><b>콤보</b> - 연속 정답일수록 더 많은 콤보 보너스 XP</span>
              </div>
            </div>

            <h4 className="font-semibold text-gray-900 mb-2">레벨업 & 레벨다운</h4>
            <div className="space-y-2 text-sm">
              <div className="rounded-lg bg-yellow-50 border border-yellow-200 px-4 py-3">
                <b>레벨업</b> - XP가 충분히 쌓이면 레벨이 올라가요. 화면에 축하 효과가 나타납니다!
              </div>
              <div className="rounded-lg bg-red-50 border border-red-200 px-4 py-3">
                <b>레벨다운</b> - 정답률이 매우 낮으면 레벨이 내려갈 수 있어요. 하지만 걱정 마세요!
              </div>
              <div className="rounded-lg bg-emerald-50 border border-emerald-200 px-4 py-3">
                <b>방어 실드 (3회)</b> - 레벨다운 전에 실드가 먼저 소모돼요. 실드가 3개 있으면 3번까지 방어해줍니다. 좋은 성적을 내면 실드가 다시 충전됩니다.
              </div>
            </div>

            <h4 className="mt-4 font-semibold text-gray-900 mb-2">Lv.10 마스터!</h4>
            <div className="rounded-lg bg-gradient-to-r from-purple-100 to-indigo-100 px-4 py-3 text-sm">
              레벨 10에 도달하면 <b>마스터</b> 칭호를 받고, 선생님에게 <b>승급 추천</b>이 자동 전달됩니다. 최고 목표로 삼아보세요!
            </div>
          </Section>
        </motion.div>

        {/* 9. 적응형 테스트 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          <Section
            id="adaptive"
            icon="🎯"
            title="9. 적응형 테스트란?"
            isOpen={openSections.has('adaptive')}
            onToggle={() => toggleSection('adaptive')}
          >
            <p className="mb-4">적응형 테스트는 <b>내 실력에 맞게 난이도가 자동으로 조절</b>되는 특별한 테스트예요.</p>

            <h4 className="font-semibold text-gray-900 mb-2">어떻게 작동하나요?</h4>
            <div className="space-y-2 text-sm mb-4">
              <div className="flex items-center gap-2 rounded-lg bg-green-50 px-4 py-3">
                <span className="text-lg">⬆️</span>
                <span>정답을 맞추면 <b>난이도가 올라가요</b> (더 어려운 문제)</span>
              </div>
              <div className="flex items-center gap-2 rounded-lg bg-orange-50 px-4 py-3">
                <span className="text-lg">⬇️</span>
                <span>틀리면 <b>난이도가 내려가요</b> (조금 쉬운 문제)</span>
              </div>
            </div>

            <h4 className="font-semibold text-gray-900 mb-2">난이도 단계</h4>
            <div className="flex flex-wrap gap-2 mb-4">
              <span className="rounded-full bg-green-100 px-3 py-1 text-xs font-medium text-green-700">Lv.1~3 기초</span>
              <span className="rounded-full bg-blue-100 px-3 py-1 text-xs font-medium text-blue-700">Lv.4~5 보통</span>
              <span className="rounded-full bg-yellow-100 px-3 py-1 text-xs font-medium text-yellow-700">Lv.6~7 심화</span>
              <span className="rounded-full bg-orange-100 px-3 py-1 text-xs font-medium text-orange-700">Lv.8~9 고급</span>
              <span className="rounded-full bg-red-100 px-3 py-1 text-xs font-medium text-red-700">Lv.10 최고급</span>
            </div>

            <p className="text-sm text-gray-600">
              문제 풀이 중 화면 상단에 현재 난이도가 표시되고, 변경될 때 토스트 알림이 나타나요.
            </p>

            <Tip>
              적응형 테스트에서는 너무 쉬운 문제만 나오지 않아요. 내 실력 근처의 문제가 나오기 때문에 실력 향상에 가장 효과적입니다!
            </Tip>
          </Section>
        </motion.div>

        {/* 10. 꿀팁 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.55 }}
        >
          <Section
            id="tips"
            icon="💡"
            title="10. 꿀팁 모음"
            isOpen={openSections.has('tips')}
            onToggle={() => toggleSection('tips')}
          >
            <div className="space-y-3">
              <div className="rounded-xl bg-amber-50 border border-amber-100 px-4 py-3 text-sm">
                <b>매일 풀기</b> - 매일 1개씩만 풀어도 스트릭이 쌓여요. 연속 학습 기록을 만들어보세요!
              </div>
              <div className="rounded-xl bg-blue-50 border border-blue-100 px-4 py-3 text-sm">
                <b>콤보를 노려라</b> - 연속 정답이면 콤보 보너스 XP가 크게 올라가요. 신중하게 풀어보세요.
              </div>
              <div className="rounded-xl bg-green-50 border border-green-100 px-4 py-3 text-sm">
                <b>복습이 핵심</b> - 틀린 문제를 복습하면 같은 유형을 또 틀릴 확률이 줄어들어요.
              </div>
              <div className="rounded-xl bg-purple-50 border border-purple-100 px-4 py-3 text-sm">
                <b>취약 개념 확인</b> - 내 통계에서 취약 개념을 확인하고 관련 문제를 집중적으로 풀어보세요.
              </div>
              <div className="rounded-xl bg-rose-50 border border-rose-100 px-4 py-3 text-sm">
                <b>시간 보너스</b> - 남은 시간이 많을수록 시간 보너스 XP를 더 많이 받아요. 빠르고 정확하게!
              </div>
              <div className="rounded-xl bg-indigo-50 border border-indigo-100 px-4 py-3 text-sm">
                <b>Lv.10 마스터</b> - 꾸준히 풀면 누구나 도달할 수 있어요. 포기하지 마세요!
              </div>
            </div>
          </Section>
        </motion.div>

        {/* 하단 바로가기 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="rounded-2xl bg-gradient-to-r from-primary-500 to-primary-600 p-6 text-white shadow-lg"
        >
          <h3 className="text-lg font-bold mb-3">바로 시작해볼까요?</h3>
          <div className="flex flex-wrap gap-3">
            <Link
              to="/tests"
              className="inline-flex items-center gap-1.5 rounded-xl bg-white/20 px-4 py-2.5 text-sm font-medium text-white transition-colors hover:bg-white/30"
            >
              <span>📝</span> 테스트 풀기
            </Link>
            <Link
              to="/practice"
              className="inline-flex items-center gap-1.5 rounded-xl bg-white/20 px-4 py-2.5 text-sm font-medium text-white transition-colors hover:bg-white/30"
            >
              <span>🚀</span> 빠른 연습
            </Link>
            <Link
              to="/review"
              className="inline-flex items-center gap-1.5 rounded-xl bg-white/20 px-4 py-2.5 text-sm font-medium text-white transition-colors hover:bg-white/30"
            >
              <span>🔄</span> 복습하기
            </Link>
            <Link
              to="/my-stats"
              className="inline-flex items-center gap-1.5 rounded-xl bg-white/20 px-4 py-2.5 text-sm font-medium text-white transition-colors hover:bg-white/30"
            >
              <span>📊</span> 내 통계
            </Link>
          </div>
        </motion.div>
      </div>
    </div>
  )
}
