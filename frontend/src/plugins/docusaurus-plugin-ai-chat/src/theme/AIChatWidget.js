import React, { useEffect } from 'react';
import ChatWidget from '@site/src/components/ChatWidget';

// This component wraps the chat widget and can be used in Docusaurus theme
const DocusaurusChatWidget = () => {
  useEffect(() => {
    // Any initialization code can go here
  }, []);

  return <ChatWidget />;
};

export default DocusaurusChatWidget;