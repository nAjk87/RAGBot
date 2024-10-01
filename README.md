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
För att göra detta behöver du en json fil i mappen data samt ändra i generate_embeddings.py för att peka ut rätt fil.

Du behöver även ändra i vilka fält som skall läsas in och dess innebörd i generate_embeddings.py

I filen get_recommendations.py måste du också specificera vilken data du vill få tillbaka när boten använder sig av vår rekommendationsdatabas.


<h2>För att få ett fungerande flöde</h2>

Sätta miljövariabeln OPENAI_API_KEY samt filen med alla embeddings, dessa får man av Niklas.