import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import { useDoc } from '@docusaurus/plugin-content-docs/client';
import styles from './ChapterNavigation.module.css';

// Navigation component for moving between chapters
export default function ChapterNavigation() {
  const { metadata } = useDoc();
  const { previous, next } = metadata;

  if (!previous && !next) {
    return null; // Don't show navigation if there's no previous/next
  }

  return (
    <nav className={styles.chapterNavigation} aria-label="Chapter navigation">
      <div className={styles.navigationContainer}>
        {previous && (
          <Link
            to={previous.permalink}
            className={clsx(styles.navLink, styles.previous)}
            aria-label={`Previous: ${previous.title}`}
          >
            <span className={styles.navArrow}>&larr;</span>
            <div className={styles.navContent}>
              <span className={styles.navLabel}>Previous</span>
              <span className={styles.navTitle}>{previous.title}</span>
            </div>
          </Link>
        )}

        {next && (
          <Link
            to={next.permalink}
            className={clsx(styles.navLink, styles.next)}
            aria-label={`Next: ${next.title}`}
          >
            <div className={styles.navContent}>
              <span className={styles.navLabel}>Next</span>
              <span className={styles.navTitle}>{next.title}</span>
            </div>
            <span className={styles.navArrow}>&rarr;</span>
          </Link>
        )}
      </div>
    </nav>
  );
}