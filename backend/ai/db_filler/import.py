import os.path

import ollama, chromadb, time
from db_filler.utilities import readtext, getconfig
from mattsollamatools import chunk_text_by_sentences
from llm.summary.summury import make_summary

collectionname = "buildragwithpython"

chroma = chromadb.HttpClient(host="localhost", port=8000)
print(chroma.list_collections())
if any(collection.name == collectionname for collection in chroma.list_collections()):
    print('deleting collection')
    chroma.delete_collection("buildragwithpython")
collection = chroma.get_or_create_collection(name="buildragwithpython", metadata={"hnsw:space": "cosine"})

embedmodel = getconfig()["embedmodel"]
starttime = time.time()
with open('db_filler/sourcedocs.txt') as f:
    lines = f.readlines()
    procd_fil_cnt = 0
    for filename in lines:
        procd_fil_cnt+=1
        filename = filename.strip(" \n")
        if os.path.isfile(filename):
            print(f"processing {filename}")
            print(f"file {procd_fil_cnt}/{len(lines)}")
            text = readtext(filename)
        if os.path.isdir(filename):
            print(f"adding all files in {filename}")
            for file in os.listdir(filename):
                lines.append(os.path.join(filename, file))
            continue

        chunks = chunk_text_by_sentences(source_text=text, sentences_per_chunk=20, overlap=2)
        print(f"{len(chunks)} chunks")

        procd_embd_cnt = 0
        sum_chunks = ''
        sum_of_sum = ''
        index = 0
        for chunk in chunks:
            procd_embd_cnt += 1
            embed = ollama.embeddings(model=embedmodel, prompt=chunk)['embedding']
            print(f"\r{procd_embd_cnt}/{len(chunks)}", end="")
            collection.add([filename + str(index)], [embed], documents=[chunk], metadatas={"source": filename})
            index += 1
            sum_chunks += chunk
            if len(sum_chunks.split()) > 2048:
                text = make_summary(sum_chunks)
                collection.add([filename + str(index)], [embed], documents=[text], metadatas={"source": filename})
                index += 1
                sum_of_sum += text
                sum_chunks = ''
                if len(sum_of_sum.split()) > 2048:
                    text = make_summary(sum_of_sum)
                    collection.add([filename + str(index)], [embed], documents=[sum_of_sum],
                                   metadatas={"source": filename})
                    index += 1
                    sum_of_sum=''

        collection.add([filename + str(index)], [embed], documents=[sum_chunks], metadatas={"source": filename})
        index += 1
        sum_chunks = ''
        print()

print("--- %s seconds ---" % (time.time() - starttime))
