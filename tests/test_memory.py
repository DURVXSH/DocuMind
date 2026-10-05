from src.rag_pipeline import answer_question


print("========== CONVERSATION MEMORY TEST ==========")

conversation_history = ""

# First question
question1 = "What is the candidate's CGPA?"

answer1, sources1 = answer_question(
    question1,
    conversation_history,
    source="Durvesh_Res.pdf"
)

print("\nQuestion 1:")
print(question1)

print("\nAnswer 1:")
print(answer1)

# Add first conversation to history
conversation_history = (
    f"User: {question1}\n"
    f"Assistant: {answer1}\n"
)

# Follow-up question
question2 = "What is their highest education?"

answer2, sources2 = answer_question(
    question2,
    conversation_history,
    source="Durvesh_Res.pdf"
)

print("\nQuestion 2:")
print(question2)

print("\nAnswer 2:")
print(answer2)

print("\nSources for Question 2:")
print(sources2)

print("-----------------------------------------------")
print("Conversation memory test completed.")