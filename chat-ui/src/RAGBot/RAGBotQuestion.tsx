import { useState, useEffect, useRef } from "react";
import styles from "./RAGBot.module.css";
import clsx from "classnames";

type Props = {
  setIsLoading: (isLoading: boolean) => void;
  question: string;
  setThreadId: (threadId: string | null) => void;
  threadId: string | null;
  isActiveQuestion: boolean;
  scrollToBottom: () => void;
};

function useQuestion(
  setThreadId: Props["setThreadId"],
  setIsLoading: Props["setIsLoading"],
  threadId: Props["threadId"],
) {
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

const RAGBotQuestion = ({
  setIsLoading,
  question,
  setThreadId,
  threadId,
  isActiveQuestion,
  scrollToBottom,
}: Props) => {
  const hasRendered = useRef<boolean>(false);
  const { text: source, loadQuestion } = useQuestion(
    setThreadId,
    setIsLoading,
    threadId,
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
        className={clsx([styles.textBubbleWrapper, styles.RAGBotBubbleWrapper])}
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
};

export default RAGBotQuestion;
