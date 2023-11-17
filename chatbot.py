import streamlit as st
from streamlit_chat import message
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
import openai
import requests
import pycountry
from langchain.llms import OpenAI

    
generic_questions,get_news = st.tabs(["Generic Chatbot", "News Bot"]) #Tabs

#Tab1
with generic_questions:

    if "generated" not in st.session_state:
        st.session_state["generated"] = []
    if "past" not in st.session_state:
        st.session_state["past"] = []
    if "input" not in st.session_state:
        st.session_state["input"] = ""
    if "stored_session" not in st.session_state:
        st.session_state["stored_session"] = []

    def get_text():
        input_text = st.text_input("You: ", st.session_state["input"], key="input",
                                placeholder="Message GenGPT", 
                                label_visibility='hidden')
        return input_text

    #Start new chat
    def new_chat(): 
        store = []
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            store.append("User:" + st.session_state["past"][i])
            store.append("Bot:" + st.session_state["generated"][i])        
        st.session_state["stored_session"].append(store)
        st.session_state["generated"] = []
        st.session_state["past"] = []
        st.session_state["input"] = ""
        st.session_state.entity_memory.entity_store = {}
        st.session_state.entity_memory.buffer.clear()

    model = st.sidebar.selectbox(label='Model', options=['gpt-3.5-turbo','text-davinci-003','text-davinci-002'])
    K = st.sidebar.number_input(' (#)Conversation turns to be stored',min_value=3,max_value=1000)

    st.title("Ask me anything")

    apikey = st.sidebar.text_input("API-KEY", type="password")

    if apikey:
        llm = OpenAI(temperature=0,
                    openai_api_key=apikey, 
                    model_name=model, 
                    verbose=False,            
            max_tokens=256) 


        if 'entity_memory' not in st.session_state:
                st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k=K )
            
        Conversation = ConversationChain(
                llm=llm, 
                prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
                memory=st.session_state.entity_memory
            )  
    else:
        st.sidebar.warning('API key is required.')
        # st.stop()


    st.sidebar.button("New Chat", on_click = new_chat, type='primary')

    user_input = get_text()

    if user_input:
        output = Conversation.run(input=user_input)
        st.session_state.past.append(user_input)  
        st.session_state.generated.append(output)  

#Download the conversation
    download_str = []
    with st.expander("Conversation", expanded=True):
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            st.success(st.session_state["generated"][i])
            st.info(st.session_state["past"][i])     
            download_str.append(st.session_state["past"][i])
            download_str.append(st.session_state["generated"][i])
        
        download_str = '\n'.join(download_str)
        if download_str:
            st.download_button('Download',download_str)

    for i, sublist in enumerate(st.session_state.stored_session):
            with st.sidebar.expander(label= f"Conversation-Session:{i}"):
                st.write(sublist)
    if st.session_state.stored_session:   
        if st.sidebar.checkbox("Clear-all"):
            del st.session_state.stored_session
#Tab 2
            
with get_news:
    st.title('News Explorer')
    columns = st.columns([2, 1])  
    chat_history = []
    end_chat = False
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "end_chat" not in st.session_state:
        st.session_state.end_chat = False


    with columns[0]:
        with st.expander("🌐 Get News", expanded=True):
            st.subheader("Explore the latest news from around the world!")

            # User inputs
            country_name = st.text_input('Enter Country name')
            news_category = st.radio('News Category', ('Entertainment', 'General', 'Health', 'Science', 'Technology', 'Sports', 'Business'))
            user_question = st.text_input('Ask a question about the selected news category')
            button = st.button('Submit')

    if button:
        country = pycountry.countries.get(name=country_name)
        if country:
            country_code = country.alpha_2
            url = f"https://newsapi.org/v2/top-headlines?country={country_code}&category={news_category}&apiKey=b585542f69b44980a6151957646da0c9"
            r = requests.get(url)
            r = r.json()
            articles = r.get('articles', [])
            article_texts = [
                f"{article['title']}. {article['description']}. {article['content']}"  
                for article in articles
                if article.get('description') is not None and article.get('content') is not None
            ]

            with columns[1]:
                st.subheader("Articles referred:")
                st.text_area("", "\n".join([f"- {article['title']}" for article in articles]), height=500)

            articles_text = '\n'.join(article_texts)

            prompt_text = f"Refer to the articles and answer the questions appropriately. Category: {news_category}. Articles: {articles_text}\nUser question: {user_question}"

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": prompt_text}],
                temperature=0,
                max_tokens=256
            )

            st.session_state.chat_history.append({"role": "Human", "content": user_question})
            st.session_state.chat_history.append({"role": "AI", "content": response['choices'][0]['message']['content']})

            user_response = st.radio("Do you have more questions?", ("Yes", "No"))

            if user_response == "No":
                st.session_state.end_chat = True  
                st.session_state.chat_history = []
                st.experimental_rerun()
    with columns[0]:
        for chat in st.session_state.chat_history:
            st.write(f"{chat['role']}: {chat['content']}")
            
            
            
            

        