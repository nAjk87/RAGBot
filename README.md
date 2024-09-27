<h1> RAGBot README för OS X</h1>

<h2>För att köra backend

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