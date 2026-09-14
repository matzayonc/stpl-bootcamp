import type {ReactNode} from 'react';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

import styles from './index.module.css';

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  const year = new Date().getFullYear();
  return (
    <Layout description="Materiały Solana Bootcamp — Superteam Poland">
      <main className={styles.hero}>
        <div className={styles.inner}>
          <img
            className={styles.logo}
            src={useBaseUrl('/img/stpl-logo.png')}
            alt="Superteam Poland"
          />
          <h1 className={styles.title}>Od Zera do Blockchain Developera</h1>
          <div className={styles.rule} />
          <p className={styles.subtitle}>{siteConfig.tagline}</p>
          <p className={styles.meta}>
            {siteConfig.title}
            {' · '}
            {year}
          </p>
          <div className={styles.actions}>
            <Link className={styles.primary} to="/docs">
              Materiały
            </Link>
            <Link
              className={styles.secondary}
              href="https://github.com/matzayonc/stpl-slides/releases/latest">
              Slajdy (PDF)
            </Link>
          </div>
        </div>
      </main>
    </Layout>
  );
}
