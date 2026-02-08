import confetti from 'canvas-confetti'

const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 9999 }
const randomInRange = (min: number, max: number) => Math.random() * (max - min) + min

/**
 * 기본 폭죽 효과 (중앙에서 터짐)
 */
export const fireFireworks = () => {
    const duration = 5 * 1000
    const animationEnd = Date.now() + duration

    const interval: any = setInterval(function () {
        const timeLeft = animationEnd - Date.now()

        if (timeLeft <= 0) {
            return clearInterval(interval)
        }

        const particleCount = 50 * (timeLeft / duration)
        // since particles fall down, start a bit higher than random
        confetti({
            ...defaults,
            particleCount,
            origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 },
        })
        confetti({
            ...defaults,
            particleCount,
            origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 },
        })
    }, 250)
}

/**
 * 학교/학원 자랑 효과 (양옆에서 쏘아올림) - 마스터/만점 등
 */
export const fireSchoolPride = () => {
    const end = Date.now() + 2 * 1000

    // go Buckeyes!
    const colors = ['#bb0000', '#ffffff', '#3b82f6', '#fbbf24']

        ; (function frame() {
            confetti({
                particleCount: 2,
                angle: 60,
                spread: 55,
                origin: { x: 0 },
                colors: colors,
            })
            confetti({
                particleCount: 2,
                angle: 120,
                spread: 55,
                origin: { x: 1 },
                colors: colors,
            })

            if (Date.now() < end) {
                requestAnimationFrame(frame)
            }
        })()
}

/**
 * 별 모양 폭죽 (레벨업 등)
 */
export const fireStars = () => {
    const defaults = {
        spread: 360,
        ticks: 50,
        gravity: 0,
        decay: 0.94,
        startVelocity: 30,
        shapes: ['star'] as confetti.Shape[],
        colors: ['#FFE400', '#FFBD00', '#E89400', '#FFCA6C', '#FDFFB8'],
    }

    const shoot = () => {
        confetti({
            ...defaults,
            particleCount: 40,
            scalar: 1.2,
            shapes: ['star'],
        })

        confetti({
            ...defaults,
            particleCount: 10,
            scalar: 0.75,
            shapes: ['circle'],
        })
    }

    setTimeout(shoot, 0)
    setTimeout(shoot, 100)
    setTimeout(shoot, 200)
}

/**
 * 업적 달성 효과 (작고 빠른 폭죽)
 */
export const fireAchievement = () => {
    const count = 200
    const defaults = {
        origin: { y: 0.7 },
    }

    function fire(particleRatio: number, opts: confetti.Options) {
        confetti({
            ...defaults,
            ...opts,
            particleCount: Math.floor(count * particleRatio),
        })
    }

    fire(0.25, {
        spread: 26,
        startVelocity: 55,
    })
    fire(0.2, {
        spread: 60,
    })
    fire(0.35, {
        spread: 100,
        decay: 0.91,
        scalar: 0.8,
    })
    fire(0.1, {
        spread: 120,
        startVelocity: 25,
        decay: 0.92,
        scalar: 1.2,
    })
    fire(0.1, {
        spread: 120,
        startVelocity: 45,
    })
}
