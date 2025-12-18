// This is a plugin to manage the AI chat functionality in Docusaurus
// It can be added to the docusaurus.config.js plugins array

module.exports = function(context, options) {
  return {
    name: 'docusaurus-plugin-ai-chat',

    getClientModules() {
      return [
        require.resolve('./src/theme/AIChatWidget'),
      ];
    },

    // Add scripts or styles if needed
    injectHtmlTags() {
      return {
        postBodyTags: [
          `<div id="ai-chat-root"></div>`,
        ],
      };
    },
  };
};