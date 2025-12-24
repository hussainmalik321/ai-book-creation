import React from 'react';
import MDXComponents from '@theme-original/MDXComponents';
import ReadingText from '@site/src/components/Typography/ReadingText';

// Override default MDX components with custom book components
export default {
  ...MDXComponents,
  h1: (props) => <ReadingText variant="heading1" {...props} />,
  h2: (props) => <ReadingText variant="heading2" {...props} />,
  h3: (props) => <ReadingText variant="heading3" {...props} />,
  h4: (props) => <ReadingText variant="heading4" {...props} />,
  p: (props) => <ReadingText variant="body" {...props} />,
  blockquote: (props) => <ReadingText variant="blockquote" {...props} />,
  // Keep other components from the original set
};