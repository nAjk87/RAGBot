<h1> RAGBot README för OS X</h1>

<h2>För att köra backend</h2>
<p> Stå i projekets root mapp</p>
* brew install uv
* uv sync
* uv run uvicorn main:app

<h2>För att köra frontend</h2>

<p>Stå i chat-ui/</p>

* brew install node
* npm install
* npm run dev

<h2>För att generera nya embeddings</h2>

<p>uv run generate_embeddings.py</p>
<p>För att göra detta behöver du en json fil i mappen data samt ändra i generate_embeddings.py för att peka ut rätt fil.</p>

<p>Du behöver även ändra i vilka fält som skall läsas in och dess innebörd i generate_embeddings.py</p>

<p>I filen get_recommendations.py måste du också specificera vilken data du vill få tillbaka när boten använder sig av vår rekommendationsdatabas.</p>


<h2>För att få ett fungerande flöde</h2>

<p>Sätta miljövariabeln OPENAI_API_KEY samt filen med alla embeddings, dessa får man av Niklas.</p>