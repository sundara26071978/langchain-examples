"""
React Frontend for Generative UI Agent

This is a sample React component that demonstrates:
1. Connecting to the Generative UI Agent backend
2. Streaming UI spec generation
3. Rendering generated UI components
4. Progressive rendering as specs arrive

To use this:
1. Save as AgentGenerativeUI.tsx in your React project
2. Install dependencies: npm install @json-render/react zod
3. Import and use: <AgentGenerativeUI />

Full working example structure:
- agentGenerativeUI/
  - components/
    - AgentGenerativeUI.tsx (this file)
    - UIComponents.tsx (component implementations)
  - hooks/
    - useGenerativeUI.ts (custom hook for agent interaction)
  - styles/
    - generative-ui.css
"""

import React, { useState, useRef, useEffect } from 'react';
import { Renderer, JSONUIProvider, defineRegistry } from '@json-render/react';

// ============================================================================
// Generative UI Agent Hook
// ============================================================================

/**
 * Custom hook for streaming UI specs from the agent
 * 
 * This demonstrates:
 * - Connecting to the agent backend
 * - Streaming responses using Server-Sent Events (SSE)
 * - Progressive rendering as specs arrive
 */
const useGenerativeUI = () => {
  const [messages, setMessages] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const generateUI = async (description: string) => {
    setIsLoading(true);
    setError(null);

    try {
      // Add user message
      setMessages(prev => [
        ...prev,
        { role: 'user', content: description }
      ]);

      // Call the agent
      const response = await fetch('http://localhost:8000/agent/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: description })
      });

      if (!response.ok) throw new Error('Agent request failed');
      
      const data = await response.json();

      // Add agent response
      setMessages(prev => [
        ...prev,
        { role: 'agent', content: data.response }
      ]);

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setIsLoading(false);
    }
  };

  return { messages, isLoading, error, generateUI };
};


// ============================================================================
// Component Catalog Definition (TypeScript version)
// ============================================================================

const componentCatalog = {
  Card: {
    description: 'A card container with title and padding',
    component: ({ props, children }: any) => (
      <div className={`card card-padding-${props.padding || 'md'}`}>
        {props.title && <h2 className="card-title">{props.title}</h2>}
        <div className="card-content">{children}</div>
      </div>
    )
  },
  Stack: {
    description: 'Layout container for vertical or horizontal stacking',
    component: ({ props, children }: any) => (
      <div className={`stack stack-${props.direction} stack-gap-${props.gap || 'md'}`}>
        {children}
      </div>
    )
  },
  TextInput: {
    description: 'Text input field with label and placeholder',
    component: ({ props }: any) => (
      <div className="form-group">
        {props.label && <label className="form-label">{props.label}</label>}
        <input
          type={props.type || 'text'}
          placeholder={props.placeholder}
          className="form-input"
        />
      </div>
    )
  },
  Button: {
    description: 'Clickable button with variants',
    component: ({ props }: any) => (
      <button
        className={`btn btn-${props.variant || 'primary'} ${props.fullWidth ? 'btn-full-width' : ''}`}
      >
        {props.label}
      </button>
    )
  },
  Text: {
    description: 'Display text content',
    component: ({ props }: any) => (
      <p className={`text text-${props.size || 'md'}`}>
        {props.content}
      </p>
    )
  },
  Badge: {
    description: 'Small status indicator or label',
    component: ({ props }: any) => (
      <span className={`badge badge-${props.variant || 'primary'}`}>
        {props.label}
      </span>
    )
  }
};


// ============================================================================
// UI Component Implementations
// ============================================================================

/**
 * Core UI components that match the catalog definitions
 * These get composed by the agent to create complete interfaces
 */
const Card = ({ props, children }: any) => (
  <div className={`card card-padding-${props.padding || 'md'}`}>
    {props.title && <h2 className="card-title">{props.title}</h2>}
    <div className="card-content">{children}</div>
  </div>
);

const Stack = ({ props, children }: any) => (
  <div className={`stack stack-${props.direction} stack-gap-${props.gap || 'md'}`}>
    {children}
  </div>
);

const TextInput = ({ props }: any) => (
  <div className="form-group">
    {props.label && <label className="form-label">{props.label}</label>}
    <input
      type={props.type || 'text'}
      placeholder={props.placeholder}
      className="form-input"
    />
  </div>
);

const Button = ({ props }: any) => (
  <button
    className={`btn btn-${props.variant || 'primary'} ${props.fullWidth ? 'btn-full-width' : ''}`}
  >
    {props.label}
  </button>
);

const Text = ({ props }: any) => (
  <p className={`text text-${props.size || 'md'}`}>
    {props.content}
  </p>
);

const Badge = ({ props }: any) => (
  <span className={`badge badge-${props.variant || 'primary'}`}>
    {props.label}
  </span>
);


// ============================================================================
// Main Component
// ============================================================================

/**
 * AgentGenerativeUI Component
 * 
 * Main component that:
 * 1. Displays the chat interface for prompting the agent
 * 2. Streams and renders the generated UI specs
 * 3. Allows users to interact with generated components
 */
const AgentGenerativeUI: React.FC = () => {
  const { messages, isLoading, error, generateUI } = useGenerativeUI();
  const [inputValue, setInputValue] = useState('');
  const [generatedSpec, setGeneratedSpec] = useState<any>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim()) {
      generateUI(inputValue);
      setInputValue('');
    }
  };

  return (
    <div className="agent-ui-container">
      {/* Header */}
      <div className="agent-ui-header">
        <h1>🎨 Generative UI Agent</h1>
        <p>Describe the UI you want, and the agent will generate it for you</p>
      </div>

      {/* Main Layout */}
      <div className="agent-ui-layout">
        {/* Left Sidebar - Chat Interface */}
        <div className="agent-sidebar">
          <div className="chat-messages">
            {messages.map((msg, idx) => (
              <div key={idx} className={`message message-${msg.role}`}>
                <div className="message-avatar">
                  {msg.role === 'user' ? '👤' : '🤖'}
                </div>
                <div className="message-content">{msg.content}</div>
              </div>
            ))}
            {isLoading && (
              <div className="message message-loading">
                <div className="message-avatar">🤖</div>
                <div className="message-content">
                  <div className="loading-spinner">Generating UI...</div>
                </div>
              </div>
            )}
            {error && (
              <div className="message message-error">
                <div className="message-avatar">⚠️</div>
                <div className="message-content">Error: {error}</div>
              </div>
            )}
          </div>

          {/* Input Form */}
          <form onSubmit={handleSubmit} className="chat-input-form">
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Describe the UI you want to create..."
              disabled={isLoading}
              className="chat-input"
            />
            <button type="submit" disabled={isLoading} className="chat-submit-btn">
              {isLoading ? '⏳' : '→'}
            </button>
          </form>
        </div>

        {/* Right Sidebar - Generated UI Preview */}
        <div className="agent-preview">
          <div className="preview-header">
            <h2>Generated UI Preview</h2>
            <p className="preview-info">Components generated by AI will appear here</p>
          </div>

          <div className="preview-content">
            {generatedSpec ? (
              <JSONUIProvider registry={componentCatalog}>
                <Renderer spec={generatedSpec} loading={isLoading} />
              </JSONUIProvider>
            ) : (
              <div className="preview-placeholder">
                <div className="placeholder-icon">✨</div>
                <p>Start by describing the UI you want to create in the chat</p>
                <p className="placeholder-examples">
                  Examples:
                  <br />• "Create a login form"
                  <br />• "Build a weather search widget"
                  <br />• "Make a feedback survey"
                </p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Example Prompts */}
      <div className="agent-examples">
        <h3>Quick Examples</h3>
        <div className="examples-grid">
          <button onClick={() => generateUI('Create a login form with email and password fields')} className="example-btn">
            Login Form
          </button>
          <button onClick={() => generateUI('Build a weather search card')} className="example-btn">
            Weather Widget
          </button>
          <button onClick={() => generateUI('Create a feedback form')} className="example-btn">
            Feedback Form
          </button>
          <button onClick={() => generateUI('Build a user profile card')} className="example-btn">
            User Profile
          </button>
        </div>
      </div>
    </div>
  );
};

export default AgentGenerativeUI;


// ============================================================================
// Styling (CSS to include in your stylesheet)
// ============================================================================

const styles = `
/* Agent UI Container */
.agent-ui-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #f5f5f5;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.agent-ui-header {
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-align: center;
}

.agent-ui-layout {
  display: flex;
  flex: 1;
  gap: 20px;
  padding: 20px;
  overflow: hidden;
}

/* Sidebar Styles */
.agent-sidebar,
.agent-preview {
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.agent-sidebar {
  flex: 1;
  min-width: 300px;
}

.agent-preview {
  flex: 1;
  min-width: 300px;
}

/* Chat Messages */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message {
  display: flex;
  gap: 12px;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.message-user {
  justify-content: flex-end;
}

.message-user .message-content {
  background: #667eea;
  color: white;
}

.message-agent .message-content {
  background: #f0f0f0;
  color: #333;
}

.message-avatar {
  font-size: 24px;
}

.message-content {
  max-width: 80%;
  padding: 12px;
  border-radius: 8px;
  word-wrap: break-word;
}

/* Input Form */
.chat-input-form {
  display: flex;
  gap: 12px;
  padding: 16px;
  border-top: 1px solid #eee;
}

.chat-input {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
}

.chat-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.chat-submit-btn {
  padding: 12px 20px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.2s;
}

.chat-submit-btn:hover:not(:disabled) {
  background: #5568d3;
}

.chat-submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Preview */
.preview-header {
  padding: 16px;
  border-bottom: 1px solid #eee;
}

.preview-header h2 {
  margin: 0 0 4px 0;
  font-size: 16px;
}

.preview-info {
  margin: 0;
  font-size: 12px;
  color: #999;
}

.preview-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.preview-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
  text-align: center;
}

.placeholder-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.placeholder-examples {
  font-size: 12px;
  color: #bbb;
  line-height: 1.6;
}

/* Examples */
.agent-examples {
  padding: 20px;
  background: white;
  border-top: 1px solid #eee;
}

.agent-examples h3 {
  margin: 0 0 12px 0;
  font-size: 14px;
  font-weight: 600;
}

.examples-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px;
}

.example-btn {
  padding: 12px;
  background: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s;
}

.example-btn:hover {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

/* Component Styles */
.card {
  background: white;
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
}

.card-padding-sm { padding: 8px; }
.card-padding-md { padding: 16px; }
.card-padding-lg { padding: 24px; }

.card-title {
  margin: 0 0 12px 0;
  font-size: 16px;
  font-weight: 600;
}

.stack {
  display: flex;
}

.stack-vertical { flex-direction: column; }
.stack-horizontal { flex-direction: row; }

.stack-gap-sm { gap: 8px; }
.stack-gap-md { gap: 16px; }
.stack-gap-lg { gap: 24px; }

.form-group {
  margin-bottom: 12px;
}

.form-label {
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
  font-size: 14px;
}

.form-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.btn {
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  font-size: 14px;
  transition: all 0.2s;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-primary:hover {
  background: #5568d3;
}

.btn-secondary {
  background: #f0f0f0;
  color: #333;
}

.btn-secondary:hover {
  background: #e0e0e0;
}

.btn-full-width {
  width: 100%;
}

.text-sm { font-size: 12px; }
.text-md { font-size: 14px; }
.text-lg { font-size: 16px; }
.text-xl { font-size: 20px; }

.badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.badge-primary {
  background: #667eea;
  color: white;
}

.badge-success {
  background: #48bb78;
  color: white;
}

.badge-warning {
  background: #ed8936;
  color: white;
}

.badge-error {
  background: #f56565;
  color: white;
}
`;

console.log('Add these styles to your CSS file:', styles);
