"""LangChain + HuggingFace (pipeline local) para traduzir EN -> DE."""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline

MODEL_NAME = "Helsinki-NLP/opus-mt-en-de"


def build_chain():
    hf_pipe = pipeline("translation_en_to_de", model=MODEL_NAME, max_length=512)
    llm = HuggingFacePipeline(pipeline=hf_pipe)
    # O modelo de tradução é seq2seq e não segue instruções: o prompt só repassa o texto.
    prompt = PromptTemplate.from_template("{text}")
    return prompt | llm | StrOutputParser()
