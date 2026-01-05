## 🚀 Features

✔ Generate high-quality articles on any topic
✔ Multiple writing tones (professional, persuasive, educational, etc.)
✔ Research-augmented generation (RAG) with ChromaDB
✔ **MLA-formatted academic papers** (heading, citations, Works Cited)
✔ Streamlit-based web UI
✔ Runs 100% locally via Ollama
✔ Export articles as TXT

---

## 🧩 Architecture

```
Streamlit UI
     ↓
ArticleGenerator (LangChain)
     ↓
Ollama (DeepSeek-R1 or any LLM)
     ↓
Embeddings (Ollama)
     ↓
ChromaDB (RAG memory)
```

This design allows:

* Fast local inference
* Retrieval-augmented generation
* Academic citation formatting
* Multiple content modes

---

## 🛠 Tech Stack

| Component       | Purpose                     |
| --------------- | --------------------------- |
| **Ollama**      | Local LLM runtime           |
| **DeepSeek-R1** | Main language model         |
| **LangChain**   | Prompt chaining + RAG       |
| **ChromaDB**    | Vector storage for research |
| **Streamlit**   | Web UI                      |
| **Python**      | Application logic           |

---

## 📦 Installation

### 1️⃣ Install Ollama

Download from
[https://ollama.com](https://ollama.com)

Pull the model:

```bash
ollama pull deepseek-r1
```

Start Ollama:

```bash
ollama serve
```

---

### 2️⃣ Clone the repository

```bash
git clone https://github.com/Abhishek992001/ai-article-generator.git
cd ai-article-generator
```

---

### 3️⃣ Create virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# OR
source .venv/bin/activate   # Mac/Linux
```

---

### 4️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶ Running the App

```bash
streamlit run app.py
```

Open in browser:

```
http://localhost:8501
```

---

## ✍ Writing Modes

### 1️⃣ Standard Article

Used for:

* Blogs
* SEO
* Marketing
* Educational content

Generated with tone, length, and keywords.

---

### 2️⃣ MLA Academic Paper

Used for:

* College assignments
* Research writing
* Literature reviews

Includes:

* MLA heading
* Centered title
* In-text citations
* Works Cited page

Fully formatted according to **Modern Language Association (MLA)** rules.

---

## 🧪 RAG (Research Mode)

The system can ingest:

* PDFs
* Notes
* Research material

These are:

* Chunked
* Embedded
* Stored in ChromaDB
* Retrieved during generation

This allows the model to write **fact-grounded articles** instead of hallucinating.

---

## 📁 Project Structure

```
ai-article-generator/
│
├── app.py                  # Streamlit UI
├── article_generator.py    # Core LangChain engine
├── config.py               # Model & system settings
├── requirements.txt
└── chroma/                 # Vector database (auto-created)
```

---

## 🔒 Why this matters

Most AI writing tools:

* Send your data to cloud APIs
* Charge per token
* Store your content

This system:

* Runs entirely on your machine
* Keeps your data private
* Gives you unlimited writing

It is ideal for:

* Writers
* Students
* Researchers
* Content teams
* Privacy-conscious users

---

## 🧠 Future Enhancements

Planned:

* PDF & DOCX export
* MLA + RAG hybrid citation grounding
* Plagiarism-safe paraphrasing
* Multi-language writing
* Web-based research ingestion

---

## 👤 Author

Built by **Abhishek Sudheer**

GitHub: [https://github.com/Abhishek992001](https://github.com/Abhishek992001)

---
