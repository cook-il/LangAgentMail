from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

def generate_langchain_response(sender, body, history=None, subject=None):
    history_text = "\n\n".join(history or [])

    prompt = PromptTemplate.from_template(
        "You are LangAgentMail, a polite and precise email assistant.\n"
        "The sender is: {sender}\n"
        "Email subject: {subject}\n\n"
        "Prior messages:\n{history}\n\n"
        "Current message:\n{body}\n\n"
        "Your reply must be helpful and clear.\n"
        "Avoid repetition or disclaimers.\n"
        "Reply below:\n"
    )

    chain = prompt | ChatOpenAI(temperature=0.3, model="gpt-3.5-turbo")

    result = chain.invoke({
        "sender": sender,
        "body": body,
        "history": history_text,
        "subject": subject or "(no subject)"
    })

    return result.content
