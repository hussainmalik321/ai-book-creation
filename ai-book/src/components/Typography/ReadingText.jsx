import React from 'react';
import clsx from 'clsx';
import styles from './ReadingText.module.css';

// Custom typography component for book content
const ReadingText = ({ children, variant = 'body', className, ...props }) => {
  const getElementType = () => {
    switch (variant) {
      case 'heading1':
        return 'h1';
      case 'heading2':
        return 'h2';
      case 'heading3':
        return 'h3';
      case 'heading4':
        return 'h4';
      case 'subtitle':
        return 'h3';
      case 'caption':
        return 'p';
      case 'blockquote':
        return 'blockquote';
      default:
        return 'p';
    }
  };

  const Element = getElementType();

  const variantClasses = {
    heading1: styles.heading1,
    heading2: styles.heading2,
    heading3: styles.heading3,
    heading4: styles.heading4,
    subtitle: styles.subtitle,
    body: styles.body,
    caption: styles.caption,
    blockquote: styles.blockquote,
    code: styles.code,
  };

  return (
    <Element
      className={clsx(
        styles.readingText,
        variantClasses[variant],
        className
      )}
      {...props}
    >
      {children}
    </Element>
  );
};

export default ReadingText;