import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import { useLocation } from '@docusaurus/router';
import ChatInterface from '../ChatInterface';
import styles from './BookLayout.module.css';

// Custom book layout component that provides a consistent reading experience
export default function BookLayout({children, title, description, wrapperClassName}) {
  const location = useLocation();

  // Determine if we're on a chapter page, blog page, or other content page
  const isChapter = location.pathname.includes('/docs/');
  const isBlog = location.pathname.includes('/blog/');
  const isContentPage = isChapter || isBlog; // Add other content page patterns as needed
  const isLanding = location.pathname === '/' || location.pathname === '/ai-book-creation/';

  return (
    <Layout title={title} description={description}>
      <div className={clsx('container', styles.bookContainer, wrapperClassName)}>
        <div className={clsx(styles.bookHeader, {[styles.landingHeader]: isLanding, [styles.chapterHeader]: isChapter})}>
          {isChapter && (
            <div className={styles.chapterTitle}>
              <h1>{title}</h1>
              <p className={styles.chapterDescription}>{description}</p>
            </div>
          )}
          {isLanding && (
            <div className={styles.landingTitle}>
              <h1>{title || 'AI Book Creation Platform'}</h1>
            </div>
          )}
        </div>

        <div className={clsx(styles.bookBody, {[styles.chapterBody]: isChapter, [styles.landingBody]: isLanding})}>
          <main className={styles.bookMain}>
            <div className={styles.bookContent}>
              {children}
            </div>
            {(isChapter || isBlog) && (
              <div className={styles.chatContainer}>
                <ChatInterface />
              </div>
            )}
          </main>
        </div>

        <div className={styles.bookFooter}>
          {isChapter && (
            <div className={styles.readingProgress}>
              <div className={styles.readingProgressBar} style={{width: '30%'}}></div>
            </div>
          )}
          <p className={styles.copyright}>© {new Date().getFullYear()} AI Book Creation Platform</p>
        </div>
      </div>
    </Layout>
  );
}