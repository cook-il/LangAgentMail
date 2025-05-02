from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# New standard uses 'Runnable' chaining with | operator
def generate_langchain_response(sender, body, history=None):
    history_text = "\n".join(history or [])
    prompt = PromptTemplate.from_template(
        "Prior messages from {sender}:\n{history}\n\nCurrent message:\n{body}\n\nReply:"
    )

    chain = prompt | ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

    result = chain.invoke({
        "sender": sender,
        "body": body,
        "history": history_text
    })

    return result.content
