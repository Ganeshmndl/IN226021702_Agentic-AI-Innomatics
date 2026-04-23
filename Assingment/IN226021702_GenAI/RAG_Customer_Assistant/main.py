import os
from dotenv import load_dotenv
from graph_engine import app

load_dotenv()


def run_bot():
    # thread_id is the unique key for MemorySaver to track sessions [cite: 85]
    # For your presentation, this ensures the bot 'remembers' previous turns [cite: 116]
    config = {"configurable": {"thread_id": "alphatech_presentation_001"}}

    print("\n" + "="*50)
    print("🚀 ALPHATECH SUPPORT SYSTEM (Stateful RAG)")
    print("Memory Active. Type 'exit' to quit.")
    print("="*50)

    while True:
        user_input = input("\nUser: ")

        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Ending session. Goodbye!")
            break

        # Only pass the new question; LangGraph fetches history via thread_id [cite: 75]
        inputs = {"question": user_input}

        try:
            # Using stream_mode="values" gives us the final state after nodes finish [cite: 74, 87]
            final_output = None
            for event in app.stream(inputs, config=config, stream_mode="values"):
                final_output = event

            if final_output and "answer" in final_output:
                print(f"\nBot: {final_output['answer']}")
            else:
                print("\nBot: I'm sorry, I couldn't process that request.")

        except Exception as e:
            print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    run_bot()
