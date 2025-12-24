import React, { useState } from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import { useDoc } from '@docusaurus/plugin-content-docs/client';
import styles from './TableOfContents.module.css';

// Table of Contents component for book navigation
export default function TableOfContents() {
  const { metadata, frontMatter } = useDoc();
  const [isOpen, setIsOpen] = useState(false);

  // In a real implementation, we would get the sidebar data
  // For now, we'll use a placeholder based on available docs
  const currentDocTitle = metadata.title;
  const currentDocSlug = metadata.unversionedId;

  // Placeholder navigation data - in a real implementation, this would come from the sidebar configuration
  const navItems = [
    {
      title: 'AI Book Creation Platform',
      permalink: '/ai-book-creation/',
      isActive: currentDocSlug === 'index'
    },
    {
      title: 'Chapter 1 - Introduction to AI Book Creation',
      permalink: '/ai-book-creation/docs/chapter-1',
      isActive: currentDocSlug === 'chapter-1'
    },
    {
      title: 'Chapter 2 - Building the Architecture',
      permalink: '/ai-book-creation/docs/chapter-2',
      isActive: currentDocSlug === 'chapter-2'
    }
  ];

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className={styles.tableOfContents}>
      <button
        className={styles.tocToggle}
        onClick={toggleMenu}
        aria-expanded={isOpen}
        aria-controls="table-of-contents"
      >
        <span className={styles.tocToggleText}>Table of Contents</span>
        <span className={clsx(styles.tocToggleIcon, {[styles.open]: isOpen})}>
          {isOpen ? '×' : '☰'}
        </span>
      </button>

      <nav
        id="table-of-contents"
        className={clsx(styles.tocNav, {[styles.visible]: isOpen})}
        hidden={!isOpen}
      >
        <ul className={styles.tocList}>
          {navItems.map((item, index) => (
            <li key={index} className={styles.tocItem}>
              <Link
                to={item.permalink}
                className={clsx(styles.tocLink, {[styles.active]: item.isActive})}
                onClick={() => setIsOpen(false)}
              >
                {item.title}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
}