import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_postgres import PGVector
from langchain.prompts import PromptTemplate
# from langchain.chains.retrieval_qa.base import RetrievalQA

from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def search_prompt(question):
    load_dotenv()

    # 0. Validações
    for k in ("PGVECTOR_URL", "PGVECTOR_COLLECTION"):
        if not os.getenv(k):
            raise RuntimeError(f"Variável de ambiente {k} não está definida.")

    # 1. Setup
    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL", "text-embedding-3-small"))

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PGVECTOR_COLLECTION"),
        connection=os.getenv("PGVECTOR_URL"),
        use_jsonb=True,
    )

    # 2. Configura componentes
    # Chain de Recuperação
    retriever = store.as_retriever(search_kwargs={"k": 10})

    # Criar o prompt template como objeto
    prompt = PromptTemplate(
        template="""
            CONTEXTO: {context}

            REGRAS:
            - Responda somente com base no CONTEXTO.
            - Se a informação não estiver explicitamente no CONTEXTO, responda:
            "Não tenho informações necessárias para responder sua pergunta."
            - Nunca invente ou use conhecimento externo.
            - Nunca produza opiniões ou interpretações além do que está escrito.

            EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
            Pergunta: "Qual é a capital da França?"
            Resposta: "Não tenho informações necessárias para responder sua pergunta."

            Pergunta: "Quantos clientes temos em 2024?"
            Resposta: "Não tenho informações necessárias para responder sua pergunta."

            Pergunta: "Você acha isso bom ou ruim?"
            Resposta: "Não tenho informações necessárias para responder sua pergunta."

            PERGUNTA DO USUÁRIO: {question}

            RESPONDA A "PERGUNTA DO USUÁRIO"
            """,
        input_variables=["context", "question"]
    )

    # Criar o LLM
    llm = ChatOpenAI(model="gpt-4o-mini")

    # 3. Criar a chain completa
    # chain = RetrievalQA.from_chain_type(
    #     llm=llm,
    #     chain_type="stuff",
    #     retriever=retriever,
    #     chain_type_kwargs={"prompt": prompt}
    # )

    chain = (
        {
            "context": retriever | (lambda docs: "\n\n".join(doc.page_content for doc in docs)),
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    # 4. Usar a chain
    # resultado = chain.invoke({"query": question})
    resultado = chain.invoke(question)

    return resultado


    # ================================================
    #       IMPLEMENTAÇÃO MANUAL PASSO A PASSO 
    # ================================================

    # 0. Validações
    # for k in ("PGVECTOR_URL", "PGVECTOR_COLLECTION"):
    #     if not os.getenv(k):
    #         raise RuntimeError(f"Variável de ambiente {k} não está definida.")

    # 1. Setup
    # embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL", "text-embedding-3-small"))

    # store = PGVector(
    #     embeddings=embeddings,
    #     collection_name=os.getenv("PGVECTOR_COLLECTION"),
    #     connection=os.getenv("PGVECTOR_URL"),
    #     use_jsonb=True,
    # )

    # 2. Busca manual
    # results = store.similarity_search_with_score(question, k=10)

    # 3. Extrai docs manualmente
    # docs = [doc for doc, score in results]

    # 4. Monta contexto manualmente
    # context = "\n\n".join([doc.page_content for doc in docs]) 

    # 5. Formata prompt manualmente
    # PROMPT_TEMPLATE = """
    #           CONTEXTO: {context}

    #           REGRAS:
    #           - Responda somente com base no CONTEXTO.
    #           - Se a informação não estiver explicitamente no CONTEXTO, responda:
    #             "Não tenho informações necessárias para responder sua pergunta."
    #           - Nunca invente ou use conhecimento externo.
    #           - Nunca produza opiniões ou interpretações além do que está escrito.

    #           EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
    #           Pergunta: "Qual é a capital da França?"
    #           Resposta: "Não tenho informações necessárias para responder sua pergunta."

    #           Pergunta: "Quantos clientes temos em 2024?"
    #           Resposta: "Não tenho informações necessárias para responder sua pergunta."

    #           Pergunta: "Você acha isso bom ou ruim?"
    #           Resposta: "Não tenho informações necessárias para responder sua pergunta."

    #           PERGUNTA DO USUÁRIO: {question}

    #           RESPONDA A "PERGUNTA DO USUÁRIO"
    #           """

    # prompt = PROMPT_TEMPLATE.format(
            # context=context, 
            # question=question
            # )

    # 6. Chama LLM manualmente
    # llm = ChatOpenAI(model="gpt-4o-mini")
    # response = llm.invoke(prompt)

    # return response.content

if __name__ == "__main__":
    pergunta = "Quantos clientes temos em 2024?"
    chain = search_prompt(pergunta)
    print(f"\nPERGUNTA: {pergunta}\n")
    print(f"RESPOSTA: {chain}\n")