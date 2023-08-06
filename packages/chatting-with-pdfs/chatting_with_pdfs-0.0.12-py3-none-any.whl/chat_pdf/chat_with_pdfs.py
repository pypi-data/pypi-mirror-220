import sys
from langchain import OpenAI
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, LLMPredictor, PromptHelper, ServiceContext
from llama_index import StorageContext, load_index_from_storage


def handle_exit():
    print("\nGoodbye!\n")
    sys.exit(1)


def build_an_index(data_folder, openai_api_key):
    # Build an Index
    documents = SimpleDirectoryReader(data_folder).load_data()

    try:
        # rebuild storage context
        storage_context = StorageContext.from_defaults(persist_dir="./chat_pdf/storage")
        # load index
        index = load_index_from_storage(storage_context)

        return index
    except:
        # define LLM
        llm_predictor = LLMPredictor(llm=OpenAI(temperature=0,
                                                openai_api_key=openai_api_key,
                                                model_name="text-davinci-003"
                                                )
                                     )

        # define prompt helper
        # set max_input_size
        max_input_size = 4096

        # set number of output tokens
        num_output = 256

        # set max_chunk_overlap
        max_chunk_overlap = 20

        prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)

        service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)

        index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)

        index.storage_context.persist()

        return index


def ask_a_question(data_folder, openai_api_key):
    print("👀 Loading...")

    print("✅ Ready! Let's start the conversation.")
    print("ℹ️ Type exit to exit.")

    try:
        while True:
            prompt = input("\n😎 Prompt: ")
            if prompt == "exit":
                handle_exit()

            # Query an Index
            query_engine = build_an_index(data_folder=data_folder, openai_api_key=openai_api_key).as_query_engine()
            response = query_engine.query(prompt)
            print()

            # transform response to string
            response = str(response)

            # if response starts with "\n", remove it
            if response.startswith("\n"):
                response = response[1:]

            print("👻 Response: " + response)
    except KeyboardInterrupt:
        handle_exit()


if __name__ == "__main__":
    folder_name = sys.argv[1]
    api_key = sys.argv[2]
    ask_a_question(folder_name, api_key)
