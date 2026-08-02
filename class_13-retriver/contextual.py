from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline

from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import LLMChainExtractor

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    pipeline
)


# ============================================================
# 1. LOCAL QWEN LLM
# ============================================================

model_id = "Qwen/Qwen2.5-0.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)

model = AutoModelForCausalLM.from_pretrained(
    model_id
)

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512
)

llm = HuggingFacePipeline(
    pipeline=pipe
)


# ============================================================
# 2. LOCAL EMBEDDING MODEL
# ============================================================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ============================================================
# 3. DOCUMENTS
# ============================================================

all_docs = [

    Document(
        page_content="""
        Regular exercise is essential for maintaining physical and mental health.
        It helps improve cardiovascular health, strengthens muscles, and boosts mood.
        """,
        metadata={"source": "H1"}
    ),

    Document(
        page_content="""
        A balanced diet is crucial for overall well-being. It provides the body with
        essential nutrients, supports immune function, and helps maintain a healthy weight.
        """,
        metadata={"source": "H2"}
    ),

    Document(
        page_content="""
        Mental health is just as important as physical health. Practices such as
        mindfulness, meditation, and seeking professional help when needed can
        significantly improve mental well-being.
        """,
        metadata={"source": "H3"}
    ),

    Document(
        page_content="""
        Adequate sleep is vital for health. It allows the body to repair itself,
        supports cognitive function, and helps regulate mood.
        """,
        metadata={"source": "H4"}
    ),

    Document(
        page_content="""
        Hydration is key to maintaining health. Drinking enough water supports
        digestion, nutrient absorption, and helps regulate body temperature.
        """,
        metadata={"source": "H5"}
    ),

    Document(
        page_content="""
        Regular health check-ups are important for early detection and prevention
        of diseases. They can help identify risk factors and provide guidance on
        maintaining a healthy lifestyle.
        """,
        metadata={"source": "I1"}
    ),

    Document(
        page_content="""
        Stress management techniques, such as deep breathing exercises, yoga,
        and time management, can help reduce stress levels and improve overall
        health. Chronic stress can lead to various health issues.
        """,
        metadata={"source": "I2"}
    ),

    Document(
        page_content="""
        Vaccinations are a critical component of public health. They protect
        individuals from infectious diseases and contribute to herd immunity.
        """,
        metadata={"source": "I3"}
    ),

    Document(
        page_content="""
        Regular physical activity, such as walking, cycling, or swimming, can help
        prevent chronic diseases and improve overall health.
        """,
        metadata={"source": "I4"}
    ),

    Document(
        page_content="""
        Maintaining a healthy weight through a combination of diet and exercise
        can reduce the risk of various health conditions, including heart disease,
        diabetes, and certain cancers.
        """,
        metadata={"source": "I5"}
    )
]


# ============================================================
# 4. CREATE CHROMA VECTOR STORE
# ============================================================

vector_store = Chroma.from_documents(
    documents=all_docs,
    embedding=embedding_model,
    collection_name="health_wellness"
)


# ============================================================
# 5. BASE RETRIEVER
# ============================================================

base_retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 5
    }
)


# ============================================================
# 6. CREATE LLM COMPRESSOR
# ============================================================

compressor = LLMChainExtractor.from_llm(
    llm
)


# ============================================================
# 7. CREATE CONTEXTUAL COMPRESSION RETRIEVER
# ============================================================

compression_retriever = ContextualCompressionRetriever(
    base_retriever=base_retriever,
    base_compressor=compressor
)


# ============================================================
# 8. USER QUERY
# ============================================================

query = "What are some effective stress management techniques?"


# ============================================================
# 9. NORMAL RETRIEVAL
# ============================================================

normal_results = base_retriever.invoke(query)


# ============================================================
# 10. CONTEXTUAL COMPRESSION RETRIEVAL
# ============================================================

compressed_results = compression_retriever.invoke(query)


# ============================================================
# 11. PRINT NORMAL RESULTS
# ============================================================

print("\n")
print("=" * 70)
print("NORMAL SIMILARITY RESULTS")
print("=" * 70)

for i, doc in enumerate(normal_results, 1):

    print(f"\n--- Document {i} ---")

    print("Content:")
    print(doc.page_content.strip())

    print("\nMetadata:")
    print(doc.metadata)


