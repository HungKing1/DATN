import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface MarkdownRendererProps {
  content: string;
  className?: string;
}

export function MarkdownRenderer({ content, className = '' }: MarkdownRendererProps) {
  // Tiền xử lý: chuyển [1], [2] thành dạng link đặc biệt để dễ dàng custom render
  // Ví dụ: [1] -> [[1]](cite:1)
  const processedContent = content.replace(/\[(\d+)\]/g, '[[$1]](cite:$1)');

  return (
    <div className={`markdown-body ${className}`}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          h2: ({ node, ...props }) => <h2 className="md-h2" {...props} />,
          h3: ({ node, ...props }) => <h3 className="md-h3" {...props} />,
          p:  ({ node, ...props }) => <p className="md-p" {...props} />,
          ul: ({ node, ...props }) => <ul className="md-ul" {...props} />,
          ol: ({ node, ...props }) => <ol className="md-ol" {...props} />,
          a:  ({ node, href, children, ...props }) => {
            if (href?.startsWith('cite:')) {
              return <sup className="citation-ref">{children}</sup>;
            }
            return <a href={href} className="text-blue-500 hover:underline" target="_blank" rel="noopener noreferrer" {...props}>{children}</a>;
          },
          code: ({ node, className, children, ...props }: any) => {
            // Check if it's inline or a block
            // ReactMarkdown passes inline as a boolean or we can infer it
            const match = /language-(\w+)/.exec(className || '');
            const isInline = props.inline ?? (!match && !String(children).includes('\n'));
            
            if (isInline) {
              return <code className="inline-code" {...props}>{children}</code>;
            }
            return (
              <pre className="code-block" {...props}>
                <code className={className}>{children}</code>
              </pre>
            );
          },
        }}
      >
        {processedContent}
      </ReactMarkdown>
    </div>
  );
}
