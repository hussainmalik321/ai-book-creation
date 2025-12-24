import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

import Heading from '@theme/Heading';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx(styles.heroBanner)}>
      <div className="container">
        <div className={styles.heroContent}>
          <Heading as="h1" className={styles.heroTitle}>
            {siteConfig.title}
          </Heading>
          <p className={styles.heroSubtitle}>
            {siteConfig.tagline}
          </p>
          <div className={styles.heroButtons}>
            <Link
              className="button button--primary button--lg"
              to="/docs/intro">
              Start Reading
            </Link>
            <Link
              className="button button--secondary button--lg"
              to="/docs/chapter-1">
              Explore Chapters
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
}

function FeatureSection() {
  return (
    <section className={styles.featuresSection}>
      <div className="container">
        <div className="row">
          {[
            {
              title: 'Premium Reading Experience',
              description: 'A distraction-free, book-like interface designed for focused learning and engagement.',
              icon: '📚'
            },
            {
              title: 'AI-Powered Content',
              description: 'Leverage artificial intelligence to create, organize, and enhance educational content.',
              icon: '🤖'
            },
            {
              title: 'Responsive Design',
              description: 'Perfect reading experience on all devices from mobile to desktop with adaptive layouts.',
              icon: '📱'
            },
            {
              title: 'Modern Architecture',
              description: 'Built with modern web technologies for optimal performance and maintainability.',
              icon: '⚡'
            },
            {
              title: 'Custom Navigation',
              description: 'Intuitive navigation systems designed specifically for book-like content consumption.',
              icon: '🧭'
            },
            {
              title: 'Scalable Platform',
              description: 'Easily extendable architecture that grows with your content and audience needs.',
              icon: '📈'
            },
          ].map((feature, idx) => (
            <div key={idx} className="col col--4">
              <div className={clsx('text--center', styles.featureCard)}>
                <div className={styles.featureIcon}>{feature.icon}</div>
                <Heading as="h3" className={styles.featureTitle}>{feature.title}</Heading>
                <p className={styles.featureDescription}>{feature.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function ChapterPreview() {
  return (
    <section className={styles.chapterPreview}>
      <div className="container">
        <Heading as="h2" className={styles.sectionTitle}>Featured Chapters</Heading>
        <div className="row">
          {[
            {
              title: 'Introduction to AI Book Creation',
              description: 'Understanding the fundamentals and principles of AI-powered book creation.',
              link: '/docs/chapter-1',
              number: '01'
            },
            {
              title: 'Building the Architecture',
              description: 'Creating the foundational components of an AI book platform.',
              link: '/docs/chapter-2',
              number: '02'
            },
            {
              title: 'Custom Navigation Systems',
              description: 'Implementing intuitive navigation for book-like reading experiences.',
              link: '/docs/chapter-3',
              number: '03'
            },
          ].map((chapter, idx) => (
            <div key={idx} className="col col--4">
              <div className={styles.chapterCard}>
                <div className={styles.chapterNumber}>{chapter.number}</div>
                <Heading as="h3" className={styles.chapterTitle}>{chapter.title}</Heading>
                <p className={styles.chapterDescription}>{chapter.description}</p>
                <Link to={chapter.link} className={styles.chapterLink}>
                  Read Chapter →
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`AI Book Platform - ${siteConfig.tagline}`}
      description="A premium, production-grade book experience authored and evolved via AI specs">
      <HomepageHeader />
      <main>
        <FeatureSection />
        <ChapterPreview />
      </main>
    </Layout>
  );
}
