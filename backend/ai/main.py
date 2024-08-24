import random
import sys

from db_filler.utilities import getconfig
from llm.llm_answer.search import ModelOllama
from llm.query_transformer.rephrase import make_rephares, rephrase_query


def main():
    query = " ".join(sys.argv[1:])
    model = ModelOllama(getconfig)
    # reph_funcs = [make_more_concrete, make_more_abstract, make_rephares]
    reph_funcs = [make_rephares]

    additional_question = rephrase_query(query, model, random.choice(reph_funcs))
    model.make_search(query, additional_query=additional_question)


if __name__ == "__main__":
    main()
