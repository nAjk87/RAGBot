import React, { useState } from "react";
import styles from "./RAGBot.module.css";
import RAGBotQuestion from "./RAGBotQuestion";

const RAGBot = () => {
  console.log("ragbot rendreras");
  const [questionValue, setQuestionValue] = React.useState("");
  const [questions, setQuestions] = useState<string[]>([]);
  const [threadId, setThreadId] = useState<string | null>(null);
  const scrollContainerRef = React.useRef<HTMLDivElement>(null);

  const isLoadingRef = React.useRef(false);
  const setIsLoading = (loading: boolean) => {
    isLoadingRef.current = loading;
  };
  const handleAskQuestion = () => {
    if (!questionValue) {
      return;
    }
    scrollContainerRef.current?.scrollTo({
      top: scrollContainerRef.current.scrollHeight,
      behavior: "smooth",
    });
    setQuestions((old) => [...old, questionValue]);
    setQuestionValue("");
  };

  const scrollToBottom = () => {
    scrollContainerRef.current?.scrollTo({
      top: scrollContainerRef.current.scrollHeight,
    });
  };

  return (
    <div className={styles.wrapper}>
      <div className={styles.scrollContainer} ref={scrollContainerRef}>
        <div className={styles.questionsWrapper}>
          {questions.map((question, index) => (
            <RAGBotQuestion
              key={question}
              question={question}
              setThreadId={setThreadId}
              threadId={threadId}
              isActiveQuestion={questions.length - 1 === index}
              setIsLoading={setIsLoading}
              scrollToBottom={scrollToBottom}
            />
          ))}
        </div>
      </div>
      <div className={styles.footer}>
        <div className={styles.inputWrapper}>
          <input
            className={styles.searchInput}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleAskQuestion();
              }
            }}
            placeholder="Fråga RAGBot"
            type="text"
            id="ragbot-question"
            value={questionValue}
            onChange={(e) => setQuestionValue(e.target.value)}
          />
        </div>
      </div>
    </div>
  );
};

export default RAGBot;
