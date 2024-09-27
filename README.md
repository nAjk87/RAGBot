<h1> RAGBot README för OS X</h1>

<h2>För att köra backend</h2>

brew install uv

uv sync

uv run uvicorn main:app

<h2>För att köra frontend</h2>

Stå i chat-ui/

brew install node

npm install

npm run dev

<h2>För att generera nya embeddings</h2>

uv run generate_embeddings.py

<h2>För att få ett fungerand flöde</h2>

Sätta miljövariabeln OPENAI_API_KEY som man får av Niklas