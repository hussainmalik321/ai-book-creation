import React from 'react';
import Layout from '@theme-original/Layout';
import FloatingChatButton from '@site/src/components/ChatInterface/FloatingChatButton';

export default function LayoutWrapper(props) {
  return (
    <>
      <Layout {...props}>
        {props.children}
      </Layout>
      <FloatingChatButton />
    </>
  );
}