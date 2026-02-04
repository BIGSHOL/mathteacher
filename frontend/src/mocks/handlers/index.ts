import { authHandlers } from './auth'
import { testHandlers } from './test'
import { statsHandlers } from './stats'
import { generateHandlers } from './generate'
import { aiHandlers } from './ai'

export const handlers = [...authHandlers, ...testHandlers, ...statsHandlers, ...generateHandlers, ...aiHandlers]
