import { useCallback } from 'react'

interface Particle {
  id: string
  x: number
  y: number
  type: 'left' | 'right' | 'center'
}

export const useParticles = () => {
  const createParticles = useCallback((element: HTMLElement | null, count: number = 8): Particle[] => {
    if (!element) return []

    const rect = element.getBoundingClientRect()
    const particles: Particle[] = []

    for (let i = 0; i < count; i++) {
      const angle = (i / count) * Math.PI * 2
      const type = i % 3 === 0 ? 'left' : i % 3 === 1 ? 'right' : 'center'

      particles.push({
        id: `particle-${Date.now()}-${i}`,
        x: rect.left + rect.width / 2,
        y: rect.top + rect.height / 2,
        type: type as 'left' | 'right' | 'center'
      })
    }

    return particles
  }, [])

  return { createParticles }
}
