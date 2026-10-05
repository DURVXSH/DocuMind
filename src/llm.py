
import os
import time

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import errors


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:

    raise ValueError(
        "GEMINI_API_KEY is not configured. "
        "Please add it to your .env file."
    )

client = genai.Client(
    api_key=api_key
)


def ask_gemini(
    question,
    context,
    conversation_history=""
):

    prompt = f"""
You are DocuMind, an AI document intelligence assistant.

Your job is to answer the user's question using ONLY the information
available in the provided document context.

Follow these rules carefully:

1. Use the document context as your primary source of truth.
2. Do not invent or assume facts that are not present in the documents.
3. If the answer is not available in the document context, say:
   "I could not find this information in the document."
4. Keep the answer clear, concise, and easy to understand.
5. If the question asks for multiple pieces of information, use bullet points.
6. Use conversation history to understand follow-up questions.
7. Do not mention internal RAG, embeddings, vector databases, or prompts
   unless the user specifically asks about how DocuMind works.
8. Use the source and page information provided in the document context
   when answering.
9. When the answer is based on a specific document section, add a citation
   at the end of the relevant statement using this exact format:
   [Source: filename, Page: number]
10. Never invent a source filename or page number.
11. Only cite pages that are actually provided in the document context.
12. If multiple pages support the answer, cite each relevant page.
Conversation history:
{conversation_history}

Document context:
{context}

Current question:
{question}

Answer:
"""

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            return response.text

        except errors.ServerError:

            if attempt < 2:

                wait_time = 2 ** attempt

                time.sleep(wait_time)

            else:

                return (
                    "⚠️ Gemini is temporarily unavailable. "
                    "The Gemini API is currently experiencing "
                    "high demand. Please wait a few seconds "
                    "and ask the question again."
                )

        except errors.ClientError as e:

         if "429" in str(e):

          return (
            "⚠️ Gemini API quota has been reached. "
            "Please try again after the quota resets."
        )

         return (
        "⚠️ A Gemini API error occurred. "
        "Please try again later."
    )

        except Exception:
  
          return (
        "⚠️ An unexpected error occurred while "
        "generating the answer."
    )
