import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import stplPrism from './src/theme/prism-stpl';

// Brand tokens live in branding.md / preamble.tex; the CSS side is
// src/css/custom.css. Mermaid colors match images/src/config.json.
const config: Config = {
  title: 'Superteam Poland',
  tagline: 'Solana Bootcamp',
  favicon: 'img/favicon.png',

  url: 'https://matzayonc.github.io',
  baseUrl: '/stpl-slides/',
  organizationName: 'matzayonc',
  projectName: 'stpl-slides',
  trailingSlash: false,

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'pl',
    locales: ['pl'],
  },

  headTags: [
    {
      tagName: 'link',
      attributes: {rel: 'preconnect', href: 'https://fonts.googleapis.com'},
    },
    {
      tagName: 'link',
      attributes: {
        rel: 'preconnect',
        href: 'https://fonts.gstatic.com',
        crossorigin: 'anonymous',
      },
    },
    {
      tagName: 'link',
      attributes: {
        rel: 'stylesheet',
        href: 'https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;700&display=swap',
      },
    },
  ],

  stylesheets: [
    {
      href: 'https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/katex.min.css',
      type: 'text/css',
      crossorigin: 'anonymous',
    },
  ],

  markdown: {
    mermaid: true,
    hooks: {onBrokenMarkdownLinks: 'throw'},
  },
  themes: ['@docusaurus/theme-mermaid'],

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: 'docs',
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/matzayonc/stpl-slides/tree/main/site/',
          remarkPlugins: [remarkMath],
          rehypePlugins: [rehypeKatex],
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    colorMode: {
      defaultMode: 'dark',
      disableSwitch: true,
      respectPrefersColorScheme: false,
    },
    navbar: {
      title: 'Superteam Poland',
      logo: {
        alt: 'Superteam Poland',
        src: 'img/stpl-logo.png',
      },
      items: [
        {type: 'docSidebar', sidebarId: 'docs', position: 'left', label: 'Materiały'},
        {
          href: 'https://github.com/matzayonc/stpl-slides/releases/latest',
          label: 'Slajdy (PDF)',
          position: 'right',
        },
        {
          href: 'https://github.com/matzayonc/stpl-slides',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      logo: {
        alt: 'Superteam Poland',
        src: 'img/stpl-logo.png',
        height: 28,
      },
      links: [
        {
          title: 'Bootcamp',
          items: [
            {label: 'Materiały', to: '/docs'},
            {
              label: 'Slajdy (PDF)',
              href: 'https://github.com/matzayonc/stpl-slides/releases/latest',
            },
          ],
        },
        {
          title: 'Superteam',
          items: [
            {label: 'Superteam Poland', href: 'https://pl.superteam.fun'},
            {label: 'GitHub', href: 'https://github.com/matzayonc/stpl-slides'},
          ],
        },
      ],
      copyright: `Superteam Poland · ${new Date().getFullYear()}`,
    },
    prism: {
      theme: stplPrism,
      darkTheme: stplPrism,
      additionalLanguages: ['rust', 'toml', 'bash', 'json'],
    },
    mermaid: {
      theme: {light: 'base', dark: 'base'},
      options: {
        fontFamily: 'Archivo, sans-serif',
        flowchart: {htmlLabels: true, curve: 'basis'},
        themeVariables: {
          fontFamily: 'Archivo, sans-serif',
          primaryColor: '#161A1B',
          primaryTextColor: '#FFFFFF',
          primaryBorderColor: '#DC143C',
          lineColor: '#8A9BA8',
          tertiaryColor: '#161A1B',
          secondaryColor: '#161A1B',
          clusterBkg: '#0B0E0F',
          clusterBorder: '#1E2526',
          titleColor: '#FFFFFF',
          edgeLabelBackground: '#0B0E0F',
        },
      },
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
