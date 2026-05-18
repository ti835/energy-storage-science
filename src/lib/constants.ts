export const BASE = '/energy-storage-science';

export const SITE = {
  title: '储能科学',
  tagline: '数据驱动的储能技术洞察',
  description: '专注于储能科学与工程的个人知识库，深度聚合前沿技术、工程实践与市场数据。',
  url: 'https://ti835.github.io/energy-storage-science',
  ogImage: '/images/og-default.png',
} as const;

export const NAV_ITEMS = [
  { label: '首页', href: `${BASE}/`, icon: 'dashboard' },
  { label: '前沿技术', href: `${BASE}/technologies`, icon: 'tech' },
  { label: '储能工程', href: `${BASE}/projects`, icon: 'engineering' },
  { label: '论文追踪', href: `${BASE}/papers`, icon: 'papers' },
  { label: '日报存档', href: `${BASE}/reports`, icon: 'reports' },
] as const;

export const TECH_CATEGORIES = {
  'solid-state': { label: '固态电池', color: 'bg-blue-100 text-blue-700' },
  lithium: { label: '锂离子电池', color: 'bg-green-100 text-green-700' },
  'sodium-ion': { label: '钠离子电池', color: 'bg-amber-100 text-amber-700' },
  'flow-battery': { label: '液流电池', color: 'bg-cyan-100 text-cyan-700' },
  'compressed-air': { label: '压缩空气储能', color: 'bg-purple-100 text-purple-700' },
  bms: { label: '电池管理系统', color: 'bg-rose-100 text-rose-700' },
} as const;

export const PROJECT_STAGES = {
  planning: { label: '项目规划', color: 'bg-gray-100 text-gray-700' },
  feasibility: { label: '可行性论证', color: 'bg-blue-100 text-blue-700' },
  design: { label: '设计采购', color: 'bg-cyan-100 text-cyan-700' },
  construction: { label: '施工安装', color: 'bg-amber-100 text-amber-700' },
  commissioning: { label: '调试运行', color: 'bg-green-100 text-green-700' },
  operation: { label: '运营维护', color: 'bg-emerald-100 text-emerald-700' },
} as const;

export const PROJECT_SCENARIOS = {
  'grid-side': { label: '电网侧', icon: 'grid' },
  cni: { label: '工商业', icon: 'commercial' },
  'pv-storage-charging': { label: '光储充一体化', icon: 'solar' },
} as const;

export const ECHARTS_THEME = {
  color: ['#14919b', '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'],
  backgroundColor: 'transparent',
  textStyle: {
    fontFamily: '"Noto Sans SC", system-ui, sans-serif',
    color: '#486581',
  },
  grid: {
    borderColor: '#e2e8f0',
  },
} as const;
