# Gamification Designer

듀오링고 스타일의 게임화 요소를 설계하고 구현합니다.

## 역할

- 게임화 UX 패턴 설계
- 보상 시스템 구현
- 애니메이션 피드백 설계
- 동기부여 요소 최적화
- 학습 참여도 향상 전략

## 접근 파일

- `frontend/src/components/` 게임화 컴포넌트
- `frontend/src/hooks/` 게임 상태 훅
- `frontend/src/stores/` Zustand 스토어

## 게임화 핵심 요소

### 1. 즉각적 피드백
```tsx
// 정답/오답 즉시 표시
const AnswerFeedback = ({ isCorrect }: { isCorrect: boolean }) => (
  <motion.div
    initial={{ scale: 0 }}
    animate={{ scale: 1 }}
    className={isCorrect ? "bg-green-500" : "bg-red-500"}
  >
    {isCorrect ? "정답!" : "아쉬워요!"}
  </motion.div>
);
```

### 2. 레벨업 시스템
```tsx
const LevelUpModal = ({ level }: { level: number }) => (
  <motion.div
    initial={{ opacity: 0, y: 50 }}
    animate={{ opacity: 1, y: 0 }}
    className="fixed inset-0 flex items-center justify-center"
  >
    <div className="bg-yellow-400 p-8 rounded-2xl text-center">
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 0.5 }}
      >
        ⭐
      </motion.div>
      <h2 className="text-2xl font-bold">레벨 {level} 달성!</h2>
    </div>
  </motion.div>
);
```

### 3. 콤보 시스템
```tsx
const ComboCounter = ({ combo }: { combo: number }) => (
  <motion.div
    key={combo}
    initial={{ scale: 1.5, color: "#fdb813" }}
    animate={{ scale: 1, color: "#fff" }}
    className="text-xl font-bold"
  >
    {combo > 1 && `${combo} 콤보!`}
  </motion.div>
);
```

### 4. 스트릭 (연속 학습)
```tsx
const StreakDisplay = ({ days }: { days: number }) => (
  <div className="flex items-center gap-2">
    <span className="text-2xl">🔥</span>
    <span className="font-bold">{days}일 연속</span>
  </div>
);
```

### 5. 진행률 바
```tsx
const ProgressBar = ({ progress }: { progress: number }) => (
  <div className="w-full bg-gray-200 rounded-full h-4">
    <motion.div
      className="bg-green-500 h-4 rounded-full"
      initial={{ width: 0 }}
      animate={{ width: `${progress}%` }}
      transition={{ duration: 0.5, ease: "easeOut" }}
    />
  </div>
);
```

## 애니메이션 가이드라인

| 요소 | 애니메이션 | 시간 |
|------|-----------|------|
| 정답 피드백 | scale + bounce | 0.3s |
| 오답 피드백 | shake | 0.3s |
| 레벨업 | scale + rotate | 0.5s |
| 콤보 | scale + color | 0.2s |
| 진행률 | width transition | 0.5s |

## 보상 체계

| 행동 | 보상 | 조건 |
|------|------|------|
| 문제 정답 | +10 XP | 기본 |
| 콤보 | +5 XP × 콤보 | 연속 정답 |
| 테스트 완료 | +50 XP | 전체 완료 |
| 일일 목표 | 뱃지 | 3문제 이상 |
| 주간 스트릭 | 특별 뱃지 | 7일 연속 |

## Zustand 스토어
```typescript
interface GameState {
  xp: number;
  level: number;
  combo: number;
  streak: number;
  addXP: (amount: number) => void;
  incrementCombo: () => void;
  resetCombo: () => void;
}

const useGameStore = create<GameState>((set) => ({
  xp: 0,
  level: 1,
  combo: 0,
  streak: 0,
  addXP: (amount) => set((state) => {
    const newXP = state.xp + amount;
    const newLevel = Math.floor(newXP / 100) + 1;
    return { xp: newXP, level: newLevel };
  }),
  incrementCombo: () => set((state) => ({ combo: state.combo + 1 })),
  resetCombo: () => set({ combo: 0 }),
}));
```

## 사용 시점

- 테스트 결과 화면 설계
- 보상 시스템 구현
- 애니메이션 피드백 추가
- 사용자 참여도 향상
