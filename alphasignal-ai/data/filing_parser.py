import os
from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from unstructured.partition.pdf import partition_pdf

class FilingDeltaExtractor:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)

    def extract_text(self, pdf_path: str) -> str:
        """Partitions PDF into clean text elements[cite: 122]."""
        elements = partition_pdf(filename=pdf_path)
        return "\n".join([str(el) for el in elements])

    def find_management_delta(self, prev_q_text: str, curr_q_text: str) -> Dict:
        """
        Adversarial Delta Detection:
        Identifies shifts in 'Risk Factors' or 'Management Discussion'.
        """
        template = """
        Compare the following two sections of corporate filings (Previous Quarter vs Current Quarter).
        Identify specific 'Deltas' in management tone, debt guidance, or revenue outlook.
        
        PREVIOUS Q: {prev_q}
        CURRENT Q: {curr_q}
        
        Output only a JSON object with:
        1. 'tone_shift': (Positive/Negative/Neutral)
        2. 'key_changes': List of specific numeric or strategic changes.
        3. 'risk_increase': Boolean
        4. 'evidence_quote': Direct quote from Current Q.
        """
        prompt = PromptTemplate.from_template(template)
        chain = prompt | self.llm
        
       
        response = chain.invoke({"prev_q": prev_q_text[:4000], "curr_q": curr_q_text[:4000]})
        return response.content

