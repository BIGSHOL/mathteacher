import { render, screen } from '@testing-library/react'
import { MathText } from '../MathText'

describe('MathText', () => {
  it('renders plain text as-is', () => {
    render(<MathText text="hello world" />)
    expect(screen.getByText('hello world')).toBeTruthy()
  })

  it('converts ^n to superscript', () => {
    const { container } = render(<MathText text="2^3" />)
    const sup = container.querySelector('sup')
    expect(sup).toBeTruthy()
    expect(sup!.textContent).toBe('3')
  })

  it('converts ^{10} to superscript', () => {
    const { container } = render(<MathText text="x^{10}" />)
    const sup = container.querySelector('sup')
    expect(sup).toBeTruthy()
    expect(sup!.textContent).toBe('10')
  })

  it('converts ^letter to superscript', () => {
    const { container } = render(<MathText text="2^a" />)
    const sup = container.querySelector('sup')
    expect(sup).toBeTruthy()
    expect(sup!.textContent).toBe('a')
  })

  it('renders simple fraction as vertical layout', () => {
    const { container } = render(<MathText text="3/4" />)
    // InlineFraction uses inline-flex with two spans and a border
    const fractionContainer = container.querySelector('.inline-flex.flex-col')
    expect(fractionContainer).toBeTruthy()
    const spans = fractionContainer!.querySelectorAll('span.text-\\[0\\.75em\\]')
    expect(spans.length).toBe(2)
    expect(spans[0]!.textContent).toBe('3')
    expect(spans[1]!.textContent).toBe('4')
  })

  it('renders mixed number "2 3/4" with whole part + fraction', () => {
    const { container } = render(<MathText text="2 3/4" />)
    // MixedNumber wraps whole + InlineFraction
    const mixedContainer = container.querySelector('.inline-flex.items-center')
    expect(mixedContainer).toBeTruthy()
    expect(mixedContainer!.textContent).toContain('2')
    expect(mixedContainer!.textContent).toContain('3')
    expect(mixedContainer!.textContent).toContain('4')
  })

  it('renders mixed number "2(3/4)" with whole part + fraction', () => {
    const { container } = render(<MathText text="2(3/4)" />)
    const mixedContainer = container.querySelector('.inline-flex.items-center')
    expect(mixedContainer).toBeTruthy()
  })

  it('renders standalone letters as italic (math variables)', () => {
    const { container } = render(<MathText text="2x + 3" />)
    const em = container.querySelector('em')
    expect(em).toBeTruthy()
    expect(em!.textContent).toBe('x')
  })

  it('strips LaTeX $ delimiters', () => {
    const { container } = render(<MathText text="$2^3$" />)
    // $ signs should be removed
    expect(container.textContent).not.toContain('$')
    const sup = container.querySelector('sup')
    expect(sup).toBeTruthy()
    expect(sup!.textContent).toBe('3')
  })

  it('handles empty string', () => {
    const { container } = render(<MathText text="" />)
    expect(container.querySelector('span')).toBeTruthy()
  })

  it('applies className prop', () => {
    const { container } = render(<MathText text="hello" className="custom-class" />)
    expect(container.querySelector('.custom-class')).toBeTruthy()
  })
})
