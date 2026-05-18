export function formatNumber(n: number, decimals = 0): string {
  if (Math.abs(n) >= 1_0000_0000) return (n / 1_0000_0000).toFixed(1) + '亿';
  if (Math.abs(n) >= 1_0000) return (n / 1_0000).toFixed(1) + '万';
  return n.toFixed(decimals);
}

export function formatCurrency(n: number): string {
  if (Math.abs(n) >= 1_0000_0000) return '¥' + (n / 1_0000_0000).toFixed(1) + '亿元';
  if (Math.abs(n) >= 1_0000) return '¥' + (n / 1_0000).toFixed(1) + '万元';
  return '¥' + n.toFixed(0);
}

export function formatPercent(n: number, decimals = 1): string {
  return (n * 100).toFixed(decimals) + '%';
}

export function formatDate(d: string | Date): string {
  const date = typeof d === 'string' ? new Date(d) : d;
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  });
}

export function formatDateFull(d: string | Date): string {
  const date = typeof d === 'string' ? new Date(d) : d;
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long',
  });
}

export function cn(...classes: (string | boolean | undefined | null)[]): string {
  return classes.filter(Boolean).join(' ');
}
