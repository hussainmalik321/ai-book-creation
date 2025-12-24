import React from 'react';
import clsx from 'clsx';
import styles from './Heading.module.css';

// Custom heading component for consistent styling
const Heading = ({ level = 1, children, className, ...props }) => {
  const HeadingTag = `h${level}`;

  const headingClasses = {
    1: styles.heading1,
    2: styles.heading2,
    3: styles.heading3,
    4: styles.heading4,
    5: styles.heading5,
    6: styles.heading6,
  };

  return (
    <HeadingTag
      className={clsx(
        styles.heading,
        headingClasses[level],
        className
      )}
      {...props}
    >
      {children}
    </HeadingTag>
  );
};

export default Heading;