import os.path
import time

import chromadb
import ollama
from mattsollamatools import chunk_text_by_sentences

from ai.db_filler.utilities import getconfig, readtext
from ai.llm.summary.summury import make_summary


class Information:
    idx: int = 0

    def __init__(self, info, level):
        self.info: str = info
        self.level: int = level


def add_summary(chunk, level, summary_list: list[Information], embedmodel, filename, collection):
    if len(summary_list) - 1 >= level:
        summary_list[level].info += chunk
    elif len(summary_list) - 1 < level:
        summary_list.append(Information(chunk, level))

    if len(summary_list[level].info.split(' ')) > 1500:
        summ = make_summary(summary_list[level].info)
        embed = ollama.embeddings(model=embedmodel, prompt=summary_list[level].info)['embedding']
        write_to_db(summary_list[level].info, embed, filename, collection)
        summary_list[level].info = ''
        print(f'added + level {level}')
        add_summary(summ, level + 1, summary_list, embedmodel, filename, collection)


def clean_db():
    collectionname = "buildragwithpython"

    chroma = chromadb.HttpClient(host="localhost", port=8000)
    print(chroma.list_collections())
    if any(collection.name == collectionname for collection in chroma.list_collections()):
        print('deleting collection')
        chroma.delete_collection("buildragwithpython")
    collection = chroma.get_or_create_collection(name="buildragwithpython", metadata={"hnsw:space": "cosine"})

    return collection


def get_files_list() -> list[str]:
    with open('db_filler/sourcedocs.txt') as f:
        lines = f.readlines()
        procd_fil_cnt = 0
        for filename in lines:
            procd_fil_cnt += 1
            filename = filename.strip(" \n")
            if os.path.isdir(filename):
                print(f"adding all files in {filename}")
                for file in os.listdir(filename):
                    lines.append(os.path.join(filename, file))
                continue

    return lines


def write_to_db(chunk, embed, filename, collection):
    collection.add([filename + str(Information.idx)], [embed], documents=[chunk], metadatas={"source": filename})
    Information.idx += 1


def fill_db():
    collection = clean_db()
    files = get_files_list()
    embedmodel = getconfig()["embedmodel"]
    starttime = time.time()
    for filename in files:
        if os.path.isfile(filename):
            print(f"processing {filename}")
            text = readtext(filename)
        else:
            continue

        chunks = chunk_text_by_sentences(source_text=text, sentences_per_chunk=30, overlap=2)
        print(f"{len(chunks)} chunks")

        procd_embd_cnt = 0
        content = {}
        summary_list = []
        for chunk in chunks:
            procd_embd_cnt += 1
            embed = ollama.embeddings(model=embedmodel, prompt=chunk)['embedding']
            print(f"\r{procd_embd_cnt}/{len(chunks)}", end="")
            write_to_db(chunk, embed, filename, collection)
            add_summary(chunk, 0, summary_list, embedmodel, filename, collection)

        for info in summary_list:
            if len(info.info.split(' ')) > 10:
                embed = ollama.embeddings(model=embedmodel, prompt=info.info)['embedding']
                write_to_db(info.info, embed, filename, collection)
        print()

    print("--- %s seconds ---" % (time.time() - starttime))


def main():
    fill_db()


if __name__ == '__main__':
    main()
