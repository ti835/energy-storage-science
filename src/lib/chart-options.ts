import type { EChartsOption } from 'echarts';

export const baseChartTheme: Partial<EChartsOption> = {
  color: ['#14919b', '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'],
  textStyle: {
    fontFamily: '"Noto Sans SC", system-ui, sans-serif',
    color: '#486581',
  },
  animation: true,
  animationDuration: 800,
  animationEasing: 'cubicOut',
};

export const chartGrid: EChartsOption['grid'] = {
  top: 16,
  right: 24,
  bottom: 16,
  left: 24,
  containLabel: true,
};

export function baseLineOption(overrides: Partial<EChartsOption> = {}): EChartsOption {
  return {
    ...baseChartTheme,
    grid: chartGrid,
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255,255,255,0.95)',
      borderColor: '#d9e2ec',
      borderWidth: 1,
      textStyle: { color: '#334e68', fontSize: 13 },
      boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
    },
    xAxis: {
      type: 'category',
      axisLine: { lineStyle: { color: '#d9e2ec' } },
      axisTick: { show: false },
      axisLabel: { color: '#627d98', fontSize: 12 },
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: '#f0f4f8', type: 'dashed' } },
      axisLabel: { color: '#627d98', fontSize: 12 },
    },
    ...overrides,
  };
}
