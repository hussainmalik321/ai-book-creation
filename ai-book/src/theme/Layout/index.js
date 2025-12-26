import React from 'react';
import Layout from '@theme-original/Layout';
import BrowserOnly from '@docusaurus/BrowserOnly';

export default function LayoutWrapper(props) {
  return (
    <>
      <Layout {...props}>
        {props.children}
      </Layout>
      <BrowserOnly fallback={<div></div>}>
        {() => {
          const FloatingChatButton = require('@site/src/components/ChatInterface/FloatingChatButton').default;
          return <FloatingChatButton />;
        }}
      </BrowserOnly>
    </>
  );
}