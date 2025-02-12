import nest_asyncio

from service.util import add_answer, init_file
from settings import CUSTOM_QA_FILE, COCKTAIL_FILE


from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import SummaryIndex, VectorStoreIndex
from llama_index.core.tools import QueryEngineTool
from llama_index.core.query_engine.router_query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector

nest_asyncio.apply()


# LL_MODEL = "gpt-4o"
LL_MODEL = "gpt-3.5-turbo"

# EMBED_MODEL = "text-embedding-ada-002"
EMBED_MODEL = "text-embedding-3-small"


def get_router_query_engine(file_path: str, qa_file: str) -> RouterQueryEngine:
    """Get route queries."""

    llm = OpenAI(model=LL_MODEL)
    embed_model = OpenAIEmbedding(model=EMBED_MODEL)

    # load docs list
    input_files = [file_path, qa_file]
    documents = SimpleDirectoryReader(input_files=input_files).load_data()

    # split by chunk
    splitter = SentenceSplitter(chunk_size=1024)
    nodes = splitter.get_nodes_from_documents(documents)

    summary_index = SummaryIndex(nodes)

    vector_index = VectorStoreIndex(nodes, embed_model=embed_model)

    summary_query_engine = summary_index.as_query_engine(
        response_mode="tree_summarize",
        use_async=True,
        llm=llm
    )

    vector_query_engine = vector_index.as_query_engine(llm=llm)

    summary_tool = QueryEngineTool.from_defaults(query_engine=summary_query_engine)

    vector_tool = QueryEngineTool.from_defaults(query_engine=vector_query_engine)

    query_engine = RouterQueryEngine(
        selector=LLMSingleSelector.from_defaults(),
        query_engine_tools=[
            summary_tool,
            vector_tool,
        ],
        verbose=True
    )
    return query_engine


def get_answer(question):
    init_file()
    query_engine = get_router_query_engine(COCKTAIL_FILE, CUSTOM_QA_FILE)
    result = query_engine.query(question.question)
    print(f"Bot: {result}")
    add_answer(question, result)
    return result
