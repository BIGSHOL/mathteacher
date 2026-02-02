import { motion, HTMLMotionProps } from 'framer-motion'
import { clsx } from 'clsx'

interface CardProps extends HTMLMotionProps<'div'> {
  children: React.ReactNode
  hoverable?: boolean
}

export function Card({ children, className, hoverable = false, ...props }: CardProps) {
  return (
    <motion.div
      whileHover={hoverable ? { y: -4 } : undefined}
      className={clsx('card', className)}
      {...props}
    >
      {children}
    </motion.div>
  )
}

interface CardHeaderProps {
  children: React.ReactNode
  className?: string
}

export function CardHeader({ children, className }: CardHeaderProps) {
  return <div className={clsx('px-6 py-4 border-b border-gray-100', className)}>{children}</div>
}

interface CardContentProps {
  children: React.ReactNode
  className?: string
}

export function CardContent({ children, className }: CardContentProps) {
  return <div className={clsx('p-6', className)}>{children}</div>
}

interface CardFooterProps {
  children: React.ReactNode
  className?: string
}

export function CardFooter({ children, className }: CardFooterProps) {
  return <div className={clsx('px-6 py-4 border-t border-gray-100', className)}>{children}</div>
}
