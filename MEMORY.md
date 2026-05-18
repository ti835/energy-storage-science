---
name: 储能科学知识库项目
description: 个人储能科学与工程知识库网站，Astro + ECharts + Pagefind 构建，Python 自动化日报生成
type: project
---

# 储能科学个人知识库

## 项目定位
仅供个人使用的储能科学专属数据与知识库网站，无注册/账号体系，聚焦信息聚合深度、数据可视化、自动化。

## 技术栈
- **前端**：Astro 5 + TailwindCSS 3 + ECharts 5
- **搜索**：Pagefind（本地 WASM 索引，零服务器依赖）
- **自动化**：Python 脚本 + GitHub Actions 定时触发
- **内容**：Astro Content Collections（Zod 校验 + Markdown）

## 项目结构
```
D:\文件\储能\
├── src/
│   ├── pages/          # 15 个页面
│   ├── components/     # 16 个组件（图表、卡片、导航、计算器等）
│   ├── layouts/        # 4 个布局（Base, Dashboard, Content, Section）
│   ├── content/        # Markdown 内容（技术/工程/日报/论文）
│   ├── data/           # JSON 图表数据
│   ├── lib/            # 工具库（常量、格式化、图表配置、搜索）
│   └── styles/         # 全局 CSS
├── scripts/            # Python 自动化脚本（6个）
├── public/             # 静态资源
└── .github/workflows/  # CI/CD 定时任务
```

## 已完成的板块
1. **首页仪表盘**：KPI 卡片 + 3 个 ECharts 图表 + 日报卡片 + 双入口导航
2. **前沿储能技术**：固态电池、钠离子电池深度文章 + 六维雷达图对比 + 规格表 + 技术路线图
3. **最新储能工程**：山东 LNG 储能、甘肃压缩空气案例 + 峰谷套利 ROI 计算器
4. **安全合规专区**：并网标准、消防规范、事故复盘表
5. **论文追踪**：arXiv 自动抓取 + 论文卡片展示
6. **全文搜索**：Pagefind 集成（构建后可用）
7. **关于页面**：站点设计理念和技术架构说明

## 关键设计决策
- 用 Astro 而非 VitePress：需要仪表盘首页和自定义交互组件
- 用 ECharts 而非 Chart.js：原生支持雷达图、热力图、甘特图
- 用 Pagefind 而非 Algolia：零服务器、零成本
- 交互组件用原生 JS 而非框架：Calculator 和 SearchModal 是自包含简单状态
- 内容文件用 .md 而非 .mdx：Astro 5 的 glob-loader 默认只匹配 .md
- 路径别名在 tsconfig.json 和 vite.resolve.alias 两处都要配置

## 待完成
- [ ] GitHub 仓库创建和代码推送
- [ ] Cloudflare Pages 部署
- [ ] 配置 LLM_API_KEY 启用自动化日报
- [ ] 注册 GitHub 账号（自动化 CI/CD 的必要组件）
