import { randInt, randChoice, shuffle, generateParams, uuid } from '../random'

describe('randInt', () => {
  it('결과가 min과 max 범위 내에 있다', () => {
    for (let i = 0; i < 50; i++) {
      const result = randInt(1, 10)
      expect(result).toBeGreaterThanOrEqual(1)
      expect(result).toBeLessThanOrEqual(10)
    }
  })

  it('min과 max가 같으면 그 값을 반환한다', () => {
    expect(randInt(5, 5)).toBe(5)
  })

  it('음수 범위에서도 작동한다', () => {
    for (let i = 0; i < 50; i++) {
      const result = randInt(-10, -1)
      expect(result).toBeGreaterThanOrEqual(-10)
      expect(result).toBeLessThanOrEqual(-1)
    }
  })

  it('정수를 반환한다', () => {
    for (let i = 0; i < 20; i++) {
      const result = randInt(1, 100)
      expect(Number.isInteger(result)).toBe(true)
    }
  })
})

describe('randChoice', () => {
  it('배열의 요소를 반환한다', () => {
    const arr = [1, 2, 3, 4, 5]
    for (let i = 0; i < 20; i++) {
      const result = randChoice(arr)
      expect(arr).toContain(result)
    }
  })

  it('단일 요소 배열에서 그 요소를 반환한다', () => {
    const arr = ['only']
    expect(randChoice(arr)).toBe('only')
  })

  it('문자열 배열에서 작동한다', () => {
    const arr = ['a', 'b', 'c']
    const result = randChoice(arr)
    expect(arr).toContain(result)
  })

  it('객체 배열에서 작동한다', () => {
    const arr = [{ id: 1 }, { id: 2 }, { id: 3 }]
    const result = randChoice(arr)
    expect(arr).toContain(result)
  })
})

describe('shuffle', () => {
  it('원본 배열과 같은 길이를 반환한다', () => {
    const arr = [1, 2, 3, 4, 5]
    const result = shuffle(arr)
    expect(result.length).toBe(arr.length)
  })

  it('원본 배열과 같은 요소를 포함한다', () => {
    const arr = [1, 2, 3, 4, 5]
    const result = shuffle(arr)
    expect(result.sort()).toEqual(arr.sort())
  })

  it('원본 배열을 변경하지 않는다', () => {
    const arr = [1, 2, 3, 4, 5]
    const original = [...arr]
    shuffle(arr)
    expect(arr).toEqual(original)
  })

  it('빈 배열은 빈 배열을 반환한다', () => {
    const arr: number[] = []
    const result = shuffle(arr)
    expect(result).toEqual([])
  })

  it('단일 요소 배열은 그대로 반환한다', () => {
    const arr = [42]
    const result = shuffle(arr)
    expect(result).toEqual([42])
  })

  it('대부분의 경우 순서가 바뀐다 (확률적 테스트)', () => {
    const arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    let sameCount = 0
    for (let i = 0; i < 20; i++) {
      const result = shuffle(arr)
      if (JSON.stringify(result) === JSON.stringify(arr)) {
        sameCount++
      }
    }
    // 20번 중 대부분은 순서가 바뀌어야 함 (10! = 3,628,800 경우의 수)
    expect(sameCount).toBeLessThan(20)
  })
})

describe('generateParams', () => {
  it('모든 키를 가진 객체를 반환한다', () => {
    const ranges = { a: [1, 10] as [number, number], b: [5, 15] as [number, number] }
    const result = generateParams(ranges)
    expect(result).toHaveProperty('a')
    expect(result).toHaveProperty('b')
  })

  it('값이 지정된 범위 내에 있다', () => {
    const ranges = { x: [10, 20] as [number, number], y: [30, 40] as [number, number] }
    for (let i = 0; i < 20; i++) {
      const result = generateParams(ranges)
      expect(result.x).toBeGreaterThanOrEqual(10)
      expect(result.x).toBeLessThanOrEqual(20)
      expect(result.y).toBeGreaterThanOrEqual(30)
      expect(result.y).toBeLessThanOrEqual(40)
    }
  })

  it('제약 조건이 없으면 랜덤 값을 생성한다', () => {
    const ranges = { a: [1, 100] as [number, number] }
    const result = generateParams(ranges)
    expect(result.a).toBeGreaterThanOrEqual(1)
    expect(result.a).toBeLessThanOrEqual(100)
  })

  it('제약 조건을 만족하는 값을 생성한다', () => {
    const ranges = { a: [1, 10] as [number, number], b: [1, 10] as [number, number] }
    const constraints = (p: Record<string, number>) => (p.a ?? 0) < (p.b ?? 0)

    for (let i = 0; i < 10; i++) {
      const result = generateParams(ranges, constraints)
      expect(result.a).toBeLessThan(result.b)
    }
  })

  it('제약 조건을 만족할 수 없으면 중간값을 반환한다', () => {
    const ranges = { a: [5, 5] as [number, number] }
    const constraints = (p: Record<string, number>) => (p.a ?? 0) > 10 // 불가능한 조건

    const result = generateParams(ranges, constraints)
    expect(result.a).toBe(5) // (5 + 5) / 2 = 5
  })

  it('복잡한 제약 조건을 처리한다', () => {
    const ranges = {
      a: [1, 10] as [number, number],
      b: [1, 10] as [number, number],
    }
    // a < b라는 제약 조건 (만족하기 쉬움)
    const constraints = (p: Record<string, number>) =>
      (p.a ?? 0) < (p.b ?? 0)

    for (let i = 0; i < 10; i++) {
      const result = generateParams(ranges, constraints)
      expect(result.a).toBeLessThan(result.b)
    }
  })
})

describe('uuid', () => {
  it('36자 문자열을 반환한다', () => {
    const id = uuid()
    expect(id.length).toBe(36)
  })

  it('올바른 위치에 대시가 있다', () => {
    const id = uuid()
    expect(id[8]).toBe('-')
    expect(id[13]).toBe('-')
    expect(id[18]).toBe('-')
    expect(id[23]).toBe('-')
  })

  it('14번째 문자는 버전 4를 나타낸다', () => {
    const id = uuid()
    expect(id[14]).toBe('4')
  })

  it('호출할 때마다 다른 값을 생성한다', () => {
    const ids = new Set<string>()
    for (let i = 0; i < 100; i++) {
      ids.add(uuid())
    }
    expect(ids.size).toBe(100)
  })

  it('16진수 문자만 포함한다 (대시 제외)', () => {
    const id = uuid()
    const withoutDashes = id.replace(/-/g, '')
    expect(/^[0-9a-f]+$/i.test(withoutDashes)).toBe(true)
  })
})
