import { useState } from "react";
import RagBot from "./RAGBot/RagBot";

function App() {
  const [count, setCount] = useState(0);

  return <RagBot />;
}

export default App;
