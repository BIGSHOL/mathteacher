// 수학 텍스트 렌더링 컴포넌트
// - 지수(^) → 윗첨자  (2^a → 2ᵃ, x^{10} → x¹⁰)
// - 대분수: 2 3/5, 3(1/4) → 세로 분수 + 자연수 결합
// - 분수(a/b) → 세로 분수 표시
// - 세로 계산식: 숫자와 연산자가 여러 줄로 나열된 패턴 → 전용 박스 레이아웃
// - 단독 알파벳 → 이탤릭체(수학 변수)

interface MathTextProps {
  text: string
  className?: string
}

/** 지수 패턴: ^{그룹} 또는 ^숫자들 또는 ^알파벳 */
const SUPERSCRIPT_REGEX = /\^(?:\{([^}]+)\}|(\d+)|([a-zA-Z]))/g

/**
 * 분수/대분수 통합 패턴 (우선순위 순):
 *  1) 대분수 형태1: "2 3/4" (자연수 공백 분수)
 *  2) 대분수 형태2: "2(3/4)" (자연수 괄호 분수)
 *  3) 단순 분수: "3/4"
 */
const MIXED_AND_FRACTION_REGEX = /(\d+)\s+(\d+)\/(\d+)|(\d+)\((\d+)\/(\d+)\)|(\d+)\/(\d+)/g

/** 단독 라틴 알파벳(수학 변수) */
const MATH_VAR_REGEX = /(?<![a-zA-Z])([a-zA-Z])(?![a-zA-Z/^])/g

/** 
 * 세로 계산식 패턴 감지: 
 * - 숫자, [ ], +, -, ×, ÷, =, ( ), 공백, 줄바꿈, 대시(-)가 포함된 
 * - 최소 2줄 이상의 블록
 */
const VERTICAL_CALC_REGEX = /((?:(?:\d|[\s\+\-×÷=\[\]\(\)])+\n?){2,}(?:(?:\-{3,})+(?:\n?))+(?:(?:\d|[\s\+\-×÷=\[\]\(\)])+\n?)*)/g

/** 지수(^)를 윗첨자로 변환 */
function parseSuperscripts(text: string, keyOffset: number): (string | JSX.Element)[] {
  const parts: (string | JSX.Element)[] = []
  let lastIndex = 0

  SUPERSCRIPT_REGEX.lastIndex = 0
  let match: RegExpExecArray | null
  while ((match = SUPERSCRIPT_REGEX.exec(text)) !== null) {
    if (match.index > lastIndex) {
      parts.push(text.slice(lastIndex, match.index))
    }
    const exponent = match[1] ?? match[2] ?? match[3]!
    parts.push(
      <sup key={`sup-${keyOffset + match.index}`} className="text-[0.75em]">
        {exponent}
      </sup>
    )
    lastIndex = match.index + match[0].length
  }

  if (lastIndex < text.length) {
    parts.push(text.slice(lastIndex))
  }

  return parts
}

/** 분수를 세로로 표시하는 인라인 컴포넌트 */
function InlineFraction({ numerator, denominator }: { numerator: string; denominator: string }) {
  return (
    <span
      className="inline-flex flex-col items-center mx-[1px] relative"
      style={{
        verticalAlign: '-0.4em',
        lineHeight: 1,
      }}
    >
      <span className="text-[0.75em] leading-none px-[2px] text-center min-w-[1.1em]">{numerator}</span>
      <span className="w-full border-t border-current" style={{ margin: '1px 0' }} />
      <span className="text-[0.75em] leading-none px-[2px] text-center min-w-[1.1em]">{denominator}</span>
    </span>
  )
}

/** 대분수 표시 (자연수 + 분수) */
function MixedNumber({ whole, numerator, denominator, keyId }: { whole: string; numerator: string; denominator: string; keyId: string }) {
  return (
    <span key={keyId} className="inline-flex items-center">
      <span>{whole}</span>
      <InlineFraction numerator={numerator} denominator={denominator} />
    </span>
  )
}

/** 텍스트에서 분수(대분수 포함)를 파싱하여 렌더링 */
function parseFractions(text: string): (string | JSX.Element)[] {
  const parts: (string | JSX.Element)[] = []
  let lastIndex = 0

  MIXED_AND_FRACTION_REGEX.lastIndex = 0
  let match: RegExpExecArray | null
  while ((match = MIXED_AND_FRACTION_REGEX.exec(text)) !== null) {
    if (match.index > lastIndex) {
      parts.push(text.slice(lastIndex, match.index))
    }

    if (match[1] !== undefined) {
      // 대분수 형태1: "2 3/4"
      parts.push(
        <MixedNumber key={`mix-${match.index}`} keyId={`mix-${match.index}`}
          whole={match[1]} numerator={match[2]!} denominator={match[3]!} />
      )
    } else if (match[4] !== undefined) {
      // 대분수 형태2: "2(3/4)"
      parts.push(
        <MixedNumber key={`mix-${match.index}`} keyId={`mix-${match.index}`}
          whole={match[4]} numerator={match[5]!} denominator={match[6]!} />
      )
    } else {
      // 단순 분수: "3/4"
      parts.push(
        <InlineFraction
          key={`frac-${match.index}`}
          numerator={match[7]!}
          denominator={match[8]!}
        />
      )
    }

    lastIndex = match.index + match[0].length
  }

  if (lastIndex < text.length) {
    parts.push(text.slice(lastIndex))
  }

  return parts
}

/** 텍스트에서 수학 변수를 이탤릭체로 변환 */
function parseVars(text: string, keyOffset: number): (string | JSX.Element)[] {
  const parts: (string | JSX.Element)[] = []
  let lastIndex = 0

  MATH_VAR_REGEX.lastIndex = 0
  let match: RegExpExecArray | null
  while ((match = MATH_VAR_REGEX.exec(text)) !== null) {
    const varChar = match[1]!
    const index = match.index + (match[0].length - varChar.length)

    if (index > lastIndex) {
      parts.push(text.slice(lastIndex, index))
    }
    parts.push(
      <em key={`var-${keyOffset + index}`} className="font-math not-italic" style={{ fontStyle: 'italic' }}>
        {varChar}
      </em>
    )
    lastIndex = index + varChar.length
  }

  if (lastIndex < text.length) {
    parts.push(text.slice(lastIndex))
  }

  return parts
}

/** 세로 계산식을 깔끔하게 렌더링하는 컴포넌트 */
function VerticalCalculation({ content }: { content: string }) {
  // 줄 단위로 분리하여 각 줄을 우측 정렬된 텍스트로 표시
  const lines = content.trim().split('\n')
  return (
    <div className="my-4 block w-fit bg-gray-50 border border-gray-200 rounded-lg p-3 font-mono text-sm leading-relaxed shadow-sm">
      <div className="flex flex-col items-end">
        {lines.map((line, i) => {
          // 구분선(---)인 경우 실제 선으로 렌더링
          if (line.includes('---')) {
            return <div key={i} className="w-full border-t border-gray-400 my-1" />
          }
          return (
            <div key={i} className="whitespace-pre">
              {line}
            </div>
          )
        })}
      </div>
    </div>
  )
}

/** 텍스트에서 세로 계산식 블록을 파싱 */
function parseVerticalCalcs(text: string): (string | JSX.Element)[] {
  const parts: (string | JSX.Element)[] = []
  let lastIndex = 0

  VERTICAL_CALC_REGEX.lastIndex = 0
  let match: RegExpExecArray | null
  while ((match = VERTICAL_CALC_REGEX.exec(text)) !== null) {
    if (match.index > lastIndex) {
      parts.push(text.slice(lastIndex, match.index))
    }
    parts.push(
      <VerticalCalculation
        key={`vcalc-${match.index}`}
        content={match[1]!}
      />
    )
    lastIndex = match.index + match[0].length
  }

  if (lastIndex < text.length) {
    parts.push(text.slice(lastIndex))
  }

  return parts
}

export function MathText({ text, className }: MathTextProps) {
  // 0단계: LaTeX $...$ 구분자 제거 및 [ ]를 □로 변환
  const cleaned = text.replace(/\$/g, '').replace(/\[\s*\]/g, '□')

  // 1단계: 세로 계산식 패턴 선제적 추출 (줄바꿈이 보존되어야 하므로 가장 먼저 실행)
  const vcalcParts = parseVerticalCalcs(cleaned)

  // 1.5단계: 지수(^) 파싱 → 윗첨자
  let charOffset = 0
  const supParts = vcalcParts.flatMap((part: string | JSX.Element) => {
    if (typeof part === 'string') {
      return parseSuperscripts(part, 0)
    }
    return [part]
  })

  // 2단계: 문자열 부분에서 분수/대분수 파싱
  const fracParts = supParts.flatMap((part: string | JSX.Element) => {
    if (typeof part === 'string') {
      const parsed = parseFractions(part)
      return parsed
    }
    return [part]
  })

  // 3단계: 문자열 부분에서 변수 파싱
  charOffset = 0
  const result = fracParts.flatMap((part: string | JSX.Element) => {
    if (typeof part === 'string') {
      const varParsed = parseVars(part, charOffset)
      charOffset += part.length
      return varParsed
    }
    return [part]
  })

  // 4단계: **강조** 파싱 (Visual Decoding)
  const finalResult = result.flatMap((part: string | JSX.Element) => {
    if (typeof part === 'string') {
      const subParts: (string | JSX.Element)[] = []
      const regex = /\*\*(.*?)\*\*/g
      let last = 0
      let m

      while ((m = regex.exec(part)) !== null) {
        if (m.index > last) {
          subParts.push(part.slice(last, m.index))
        }
        subParts.push(
          <span key={`bold-${m.index}`} className="font-bold text-red-600 bg-red-50 px-1 rounded">
            {m[1]}
          </span>
        )
        last = m.index + m[0].length
      }
      if (last < part.length) {
        subParts.push(part.slice(last))
      }
      return subParts
    }
    return [part]
  })

  return <span className={className}>{finalResult}</span>
}
