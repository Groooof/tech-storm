import random
import sys

import chromadb
import ollama

from ai.db_filler.utilities import getconfig
from ai.llm.query_transformer.rephrase import *


class ModelOllama:
    def __init__(self, get_model_=getconfig):
        self.config = get_model_()

    def sent_query_to_model(self, query):
        model = getconfig()["mainmodel"]
        stream = ollama.generate(model=model, prompt=query, stream=True)
        return stream

    def sent_query_to_db(self, query, n_results=5):
        def collect_metadata(filenames: list[dict]):
            sources = []
            for filename in filenames:
                sources.append(filename['source'])

            unique = list(set(sources))
            return unique

        embedmodel = self.config["embedmodel"]
        chroma = chromadb.HttpClient(host="localhost", port=8000)
        collection = chroma.get_or_create_collection("buildragwithpython")
        queryembed = ollama.embeddings(model=embedmodel, prompt=query)['embedding']
        docs = collection.query(query_embeddings=[queryembed], n_results=n_results)
        relevantdocs = docs["documents"][0]
        unique_source = collect_metadata(docs['metadatas'][0])
        # len_docs = len(docs['documents'])
        # print(f'quantity of query {len_docs}')
        return relevantdocs, unique_source

    def make_search(self, query: str, additional_query: str = ''):
        relevantdocs, sources = self.sent_query_to_db(query)
        docs = "\n\n".join(relevantdocs)
        # print(relevantdocs)
        # print("--------------------")
        # print(docs)
        modelquery = (
            f"Ты очень эффективный консультант, ты умеешь блестательно отвечать на вопросы. \n"
            f"Ты должен ответить на основной вопрос ниже:"
            f"{query} - \n"
            f"Можешь использовать следующие вопросы, как контекст, который может быть интересен. \n"
            f"Но давай по ним гораздо меньше информации, чем на основной вопрос, не более двух предложений\n"
            f"Дополнительные вопросы: \n{additional_query}"
            f"Ответь на него безотценочно и лаконично "
            f"Для ответа на вопрос используй только источники которые будут ниже, от себя ты не можешь ничего придумать"
            f"Отвечай по делу, можешь привести примеры, но только маленькие, не больше одного предложения\n"
            f"В ответе используй списки, потому что они делают ответ читаемее\n"
            f"Если там нет достаточной информации, тогда откажись отвечать совсем\n"
            f"Вот контекст, с которым можно работать:\n {docs}"
        )

        stream = self.sent_query_to_model(modelquery)
        return stream, sources

    def print(self, stream):
        print('======================================================')
        for chunk in stream:
            if chunk["response"]:
                print(chunk['response'], end='', flush=True)


def main():
    query = " ".join(sys.argv[1:])
    model = ModelOllama(getconfig)
    # reph_funcs = [make_more_concrete, make_more_abstract, make_rephares]
    reph_funcs = [make_rephares]

    additional_question = rephrase_query(query, model, random.choice(reph_funcs))
    stream, sources = model.make_search(query, additional_query=additional_question)
    model.print(stream)
    print('')
    print(f'Информация взята из {sources}')


if __name__ == '__main__':
    main()
