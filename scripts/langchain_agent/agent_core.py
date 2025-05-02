from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# This will later receive messages + optional history
def generate_langchain_response(sender, body, history=None):
    history_text = "\n".join(history or [])
    prompt = PromptTemplate.from_template(
        "Prior messages from {sender}:\n{history}\n\nCurrent message:\n{body}\n\nReply:"
    )

    chain = LLMChain(
        llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo"),
        prompt=prompt,
    )

    return chain.run(sender=sender, body=body, history=history_text)
