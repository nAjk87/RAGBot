import { useState, useEffect, useRef } from "react";
import styles from "./RAGBot.module.css";
import clsx from "classnames";
import React from "react";
function useQuestion(setThreadId, setIsLoading, threadId) {
  const [text, setText] = useState("");

  const loadQuestion = async (text: string) => {
    setIsLoading(true);
    console.log("kör vi denna två gånger?");
    setText("");
    try {
      const response = await fetch("http://localhost:8000/ask-question", {
        method: "POST",
        body: JSON.stringify({ question: text, thread_id: threadId }),
        headers: {
          "Content-Type": "application/json",
          Accept: "text/event-stream",
        },
      });

      const newThreadId = response.headers.get("x-thread-id");

      setThreadId(newThreadId);

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const a = await reader?.read();
        if (a?.done) {
          break;
        }
        setText((old) => old + decoder.decode(a?.value));
      }
    } finally {
      setIsLoading(false);
    }
  };

  return { text, loadQuestion };
}
const RAGBotQuestion = React.memo(
  ({
    setIsLoading,
    question,
    setThreadId,
    threadId,
    isActiveQuestion,
    scrollToBottom,
  }) => {
    const hasRendered = useRef<Boolean>(false);
    const { text: source, loadQuestion } = useQuestion(
      setThreadId,
      setIsLoading,
      threadId
    );

    useEffect(() => {
      if (question && !hasRendered.current) {
        loadQuestion(question);
        hasRendered.current = true;
      }
    }, [question]);

    useEffect(() => {
      scrollToBottom();
    }, [question, source]);

    return (
      <>
        <div
          className={clsx([styles.textBubbleWrapper, styles.userBubbleWrapper])}
        >
          {question}
        </div>
        <div
          className={clsx([
            styles.textBubbleWrapper,
            styles.RAGBotBubbleWrapper,
          ])}
        >
          <header className={styles.nameHeader}>
            <div
              className={clsx(styles.RAGBotNameCircle, {
                [styles.activeRAGBotNameCircle]: isActiveQuestion,
              })}
            />
            <span>RagBot</span>
          </header>
          <div className={styles.sourceContent}>
            <div style={{ marginBottom: 20 }}>
              <div
                className={styles.description}
                dangerouslySetInnerHTML={{ __html: source }}
              />
            </div>
          </div>
        </div>
      </>
    );
  },
  () => true
);
const hashCode = function (s) {
  return s.split("").reduce(function (a, b) {
    a = (a << 5) - a + b.charCodeAt(0);
    return a & a;
  }, 0);
};

export default RAGBotQuestion;
