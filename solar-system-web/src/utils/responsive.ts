export const isReducedMotion = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;
export const isMobile = () => window.matchMedia('(max-width: 700px)').matches;
export const isTablet = () => window.matchMedia('(max-width: 1050px)').matches;

export function qualitySettings() {
  const mobile = isMobile();
  return {
    pixelRatio: Math.min(window.devicePixelRatio || 1, mobile ? 1.25 : isTablet() ? 1.5 : 1.75),
    starCount: mobile ? 420 : isTablet() ? 700 : 1100,
    bloom: !mobile && !isReducedMotion(),
  };
}
