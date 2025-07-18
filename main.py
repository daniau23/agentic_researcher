# main.py
from shared import ResearchState
from graph_article.graph_article import article_graph
from graph_web.graph_web import web_graph
from dotenv import load_dotenv
from graph_web.search import DEFAULT_URL
from pydantic import ValidationError
from utils.visualizer import graph_visualiser

import os
load_dotenv('.env')  # Or just '.env' if it's in the root

LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT")
LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT")

def main():
    print("=== Welcome to the LangGraph Research Assistant ===")
    
    while True:
        print("\nSelect a task to perform:")
        print("1. Generate Research Abstract")
        print("2. Summarize Webpages")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ").strip()
        
        if choice == "1":
            title = input("Enter research title: ")
            category = input("Enter category: ")
            init_state = ResearchState(input=title, category=category)
            final_state = article_graph.invoke(init_state)
            print("\n--- Final Abstract ---")
            print(final_state["final_abstract"])

        elif choice == "2":
            print("\n📄 Web Summarizer Mode (Press Enter to exit anytime)")
            while True:
                user_input = input(f"\nEnter a URL to summarize [default: {DEFAULT_URL}]: ").strip()
                if not user_input:
                    print("🔚 Returning to main menu...")
                    break

                try:
                    init_state = ResearchState(url=user_input)
                    final_state = web_graph.invoke(init_state)
                    print("\n--- Webpage Summary ---")
                    print(final_state["summary"])
                except ValidationError as e:
                    print(f"❌ Invalid URL: {e}")

        elif choice == "3":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid input. Try again.")


if __name__ == "__main__":
    graph_visualiser(web_graph, filename="visuals/web_graph.jpg")
    graph_visualiser(article_graph, filename="visuals/article_graph.jpg")
    
    main()