from typing import List, Dict
from langchain_ollama import OllamaLLM
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from config import config


class ArticleGenerator:
    def __init__(self):
        self.llm = None
        self.embeddings = None
        self.vector_store = None
        self._initialize_models()

    # ------------------------------------------------------

    def _initialize_models(self):
        print("Initializing models...")

        self.llm = OllamaLLM(
            model=config.LLM_MODEL,
            base_url=config.OLLAMA_BASE_URL,
            temperature=config.TEMPERATURE,
            top_p=config.TOP_P,
            model_kwargs={
                "num_predict": config.MAX_TOKENS
            }
        )

        self.embeddings = OllamaEmbeddings(
            model=config.EMBEDDING_MODEL,
            base_url=config.OLLAMA_BASE_URL
        )

        print("Models initialized successfully!")

    # ------------------------------------------------------

    def _article_prompt(self):
        return PromptTemplate.from_template("""
You are a professional article writer.

Topic: {topic}
Tone: {tone}
Target length: {length} words
Keywords: {keywords}
Style: {style}

Write a complete article with headline, intro, body and conclusion.

Article:
""")

    # ------------------------------------------------------

    def create_article_from_scratch(self, topic, tone="professional", length=800, keywords="", style="informative"):
        chain = self._article_prompt() | self.llm

        return chain.invoke({
            "topic": topic,
            "tone": tone,
            "length": length,
            "keywords": keywords,
            "style": style
        })

    # ------------------------------------------------------

    def generate_with_research(self, topic, research_materials=None, tone="professional"):
        if not research_materials:
            return self.create_article_from_scratch(topic, tone)

        docs = [
            Document(page_content=text, metadata={"source": f"doc_{i}"})
            for i, text in enumerate(research_materials)
        ]

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )

        chunks = splitter.split_documents(docs)

        self.vector_store = Chroma.from_documents(
            chunks,
            embedding=self.embeddings,
            persist_directory=config.PERSIST_DIRECTORY
        )

        retriever = self.vector_store.as_retriever()

        rag_prompt = PromptTemplate.from_template("""
Use the following context to write a detailed article about {topic}.

Context:
{context}

Write in a {tone} tone.

Article:
""")

        rag_chain = (
            {"context": retriever, "topic": RunnablePassthrough(), "tone": RunnablePassthrough()}
            | rag_prompt
            | self.llm
        )

        return rag_chain.invoke(topic)

    # ------------------------------------------------------

    def enhance_existing_article(self, article, enhancement_type="improve", target_length=None):
        prompts = {
            "expand": "Expand this article to {target_length} words:\n\n{article}",
            "improve": "Improve this article:\n\n{article}",
            "summarize": "Summarize this article in {target_length} words:\n\n{article}",
            "rewrite": "Rewrite this article:\n\n{article}"
        }

        prompt = PromptTemplate.from_template(prompts.get(enhancement_type, prompts["improve"]))

        chain = prompt | self.llm

        return chain.invoke({
            "article": article,
            "target_length": target_length or config.DEFAULT_ARTICLE_LENGTH
        })

    # ------------------------------------------------------

    def generate_multiple_variants(self, topic, num_variants=3, base_article=None):
        tones = ["professional", "conversational", "persuasive", "educational", "entertaining"]
        variants = []

        for i in range(num_variants):
            tone = tones[i % len(tones)]

            if base_article:
                prompt = PromptTemplate.from_template(f"Rewrite this article in a {tone} tone:\n\n{{article}}")
                content = (prompt | self.llm).invoke({"article": base_article})
            else:
                content = self.create_article_from_scratch(topic, tone)

            variants.append({
                "variant_id": i + 1,
                "tone": tone,
                "content": content
            })

        return variants

    # ------------------------------------------------------

    def save_article(self, article, filename=None):
        if not filename:
            from datetime import datetime
            filename = f"article_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(article)

        print(f"Saved to {filename}")

    # ------------------------------------------------------

    def estimate_tokens(self, text):
        return len(text) // 4
