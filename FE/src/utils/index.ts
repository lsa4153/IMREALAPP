/**
 * Format date to Korean locale
 */
export function formatDate(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

/**
 * Format confidence score to percentage
 */
export function formatConfidence(score: number): string {
  return `${Math.round(score)}%`;
}

/**
 * Check if analysis result is dangerous
 */
export function isDangerous(result: string): boolean {
  return result === 'deepfake' || result === 'suspicious';
}