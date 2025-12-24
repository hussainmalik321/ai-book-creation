import React from 'react';
import clsx from 'clsx';
import styles from './CodeBlock.module.css';

// Custom code block component for consistent styling
const CodeBlock = ({ children, className, language, ...props }) => {
  return (
    <pre
      className={clsx(
        styles.codeBlock,
        className
      )}
      {...props}
    >
      <code
        className={clsx(
          styles.code,
          language && styles[`language-${language}`]
        )}
      >
        {children}
      </code>
    </pre>
  );
};

export default CodeBlock;