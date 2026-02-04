// 수학 텍스트 렌더링 컴포넌트
// - 지수(^) → 윗첨자  (2^a → 2ᵃ, x^{10} → x¹⁰)
// - 분수(a/b) → 세로 분수 표시
// - 단독 알파벳 → 이탤릭체(수학 변수)

interface MathTextProps {
  text: string
  className?: string
}

/** 지수 패턴: ^{그룹} 또는 ^숫자들 또는 ^알파벳 */
const SUPERSCRIPT_REGEX = /\^(?:\{([^}]+)\}|(\d+)|([a-zA-Z]))/g

/** 분수 패턴: 숫자/숫자 (예: 3/4, 12/5) */
const FRACTION_REGEX = /(\d+)\/(\d+)/g

/** 단독 라틴 알파벳(수학 변수) */
const MATH_VAR_REGEX = /(?<![a-zA-Z])([a-zA-Z])(?![a-zA-Z/^])/g

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
    <span className="inline-flex flex-col items-center mx-0.5 align-middle" style={{ verticalAlign: '-0.5em' }}>
      <span className="text-[0.75em] leading-tight px-0.5">{numerator}</span>
      <span className="w-full border-t border-current" />
      <span className="text-[0.75em] leading-tight px-0.5">{denominator}</span>
    </span>
  )
}

/** 텍스트에서 분수를 파싱하여 렌더링 */
function parseFractions(text: string): (string | JSX.Element)[] {
  const parts: (string | JSX.Element)[] = []
  let lastIndex = 0

  FRACTION_REGEX.lastIndex = 0
  let match: RegExpExecArray | null
  while ((match = FRACTION_REGEX.exec(text)) !== null) {
    if (match.index > lastIndex) {
      parts.push(text.slice(lastIndex, match.index))
    }
    parts.push(
      <InlineFraction
        key={`frac-${match.index}`}
        numerator={match[1]!}
        denominator={match[2]!}
      />
    )
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

export function MathText({ text, className }: MathTextProps) {
  // 1단계: 지수(^) 파싱 → 윗첨자
  let charOffset = 0
  const supParts = parseSuperscripts(text, 0)

  // 2단계: 문자열 부분에서 분수 파싱
  const fracParts = supParts.flatMap((part) => {
    if (typeof part === 'string') {
      const parsed = parseFractions(part)
      return parsed
    }
    return [part]
  })

  // 3단계: 문자열 부분에서 변수 파싱
  charOffset = 0
  const result = fracParts.flatMap((part) => {
    if (typeof part === 'string') {
      const varParsed = parseVars(part, charOffset)
      charOffset += part.length
      return varParsed
    }
    return [part]
  })

  return <span className={className}>{result}</span>
}
