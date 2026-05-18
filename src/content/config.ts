import { defineCollection, z } from 'astro:content';

const technologiesCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    publishDate: z.date(),
    updatedDate: z.date().optional(),
    category: z.enum([
      'solid-state',
      'lithium',
      'sodium-ion',
      'flow-battery',
      'compressed-air',
      'bms',
    ]),
    keyMetrics: z.object({
      energyDensity: z.string(),
      cycleLife: z.string(),
      lcoe: z.string(),
      trlLevel: z.number().min(1).max(9),
      roundTripEfficiency: z.string().optional(),
      operatingTemp: z.string().optional(),
    }),
    tags: z.array(z.string()),
    heroImage: z.string().optional(),
    diagramHtml: z.string().optional(),
  }),
});

const projectsCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    location: z.string(),
    capacity: z.string(),
    technologyType: z.string(),
    lifecycleStage: z.enum([
      'planning',
      'feasibility',
      'design',
      'construction',
      'commissioning',
      'operation',
    ]),
    scenario: z.enum(['grid-side', 'cni', 'pv-storage-charging']),
    startDate: z.date(),
    completionDate: z.date().optional(),
    investment: z.string().optional(),
    tags: z.array(z.string()),
    heroImage: z.string().optional(),
  }),
});

const reportsCollection = defineCollection({
  type: 'content',
  schema: z.object({
    date: z.date(),
    generatedBy: z.literal('automation').optional(),
    topics: z.array(z.string()),
    aiSummary: z.string(),
    dataSources: z.array(z.string()).optional(),
  }),
});

const papersCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    authors: z.array(z.string()),
    journal: z.string(),
    publishDate: z.date(),
    abstract: z.string(),
    keywords: z.array(z.string()),
    doi: z.string().optional(),
    arxivId: z.string().optional(),
    relevance: z.enum(['high', 'medium', 'low']),
  }),
});

export const collections = {
  technologies: technologiesCollection,
  projects: projectsCollection,
  reports: reportsCollection,
  papers: papersCollection,
};
