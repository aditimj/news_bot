# Retrieval-Augmented News Chat Interface
This project is a chat interface designed to facilitate interactions between users and ChatGPT, allowing users to retrieve headlines and news from various categories and ask questions about the news items along with generic questions.

# Project Overview
The primary objective of this project is to develop a chat interface enabling users to communicate with ChatGPT for news-related queries.
Application consists of two components including a chatbot for generic questions and a chatbot for news related questions. The interface consists of a frontend component allowing users to input questions or prompts related to news topics, view real-time responses, and access their chat history. 

## Tech Stack
1. Frontend: Streamlit (open-source python library)
2. Backend: Python
3. APIs: ChatGPT API and News API

# Features
## Generic Chatbot:
- **Generic Questioning:** Engage in diverse conversations by asking various types of questions.
- **Model Selection:** Choose from multiple language models such as 'gpt-3.5-turbo', 'text-davinci-003', 'text-davinci-002'.
- **Context Understanding:** Capable of comprehending context and retaining conversation history for smoother interactions.
- **Conversation History:** Allow users to select the number of conversation turns to store for future reference.
- **New Chat Initialization:** Start a fresh chat session for a new conversation.
- **Conversation Download:** Enable the download of entire conversation logs for offline review.
- **Chat Clearance:** Clear the chat interface to begin a new conversation or reset the current session.

## News Bot:
- **Model:** Developed using the 'gpt-3.5-turbo' model for enhanced performance.
- **News Selection Options:** Choose news articles based on specific criteria, such as country and category ('Entertainment', 'General', 'Health', 'Science', 'Technology', 'Sports', 'Business').
- **Question-Based Responses:** Prompt users to ask questions, providing answers based on the retrieved articles from the selected categories.

  # Requirements and setup:
To utilize this chatbot application, the following prerequisites and setup instructions are necessary:  

Prerequisites:
- **OpenAI Platform Account and API Key:**
  - Create an account on the OpenAI platform and obtain an API key.
- **NewsAPI Key:**
    - Create an account on the NEWS API platform and obtain an API key.
## Setup
- Create a virtual environment named **newsbot** using the following command:
  `virtualenv newsbot`
- Activate Virtual Environment (Mac):
  `source newsbot/bin/activate`
- Install Requirements:
  `pip install -r requirements.txt`
- Setup OPENAI Key:
  `echo "export OPENAI_API_KEY='yourkey'" >> ~/.zshrc`
- Add News API Key:
  Within the chatbot.py file, locate the designated section (Tab2) to add your NewsAPI key for news retrieval functionality.
- Run the Application:
  `streamlit run chatbot.py`

# Demo 
- Check out the demo of the project in action:

## Project Demo
[![Project Demo](https://img.youtube.com/vi/luPABgDW8Do/0.jpg)](https://youtu.be/luPABgDW8Do)




