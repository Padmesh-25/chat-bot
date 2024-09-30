import os
import google.generativeai as genai
import streamlit as st

# Set up Google API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyBYESMI0LTsnVgSWVoQ2LYQ28aJ22iXM7w"  # Replace with your actual API key
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Initialize session state for conversation history
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

max_history_length = 100

def txt_gpt(user_input):
    # Access the conversation history from session state
    conversation_history = st.session_state.conversation_history

    # Check if the user is asking for the AI's name
    if user_input.lower() in ["what is your name?", "what are you called?", "who are you?"]:
        return "I am Pandora. You can also call me Dora."

    # Update conversation history
    conversation_history.append(user_input)

    # Limit conversation history length
    if len(conversation_history) > max_history_length:
        conversation_history = conversation_history[1:]

    # Calculate weights for recent conversations
    weights = [i + 1 for i in range(len(conversation_history))]
    weighted_history = [conversation_history[i] * weights[i] for i in range(len(conversation_history))]

    # Prepare input for the API, including previous conversation context
    input_text = f"Previous conversation: {weighted_history} \nQuestion: {user_input}"

    # Call the Gemini API
    model_name = genai.GenerativeModel('gemini-1.5-flash')
    response = model_name.generate_content(input_text)
    response_content = response.text.strip()

    # Determine response length based on user input
    
    conversation_history.append(response_content)
    return response_content
    

def main():
    st.title("Pandora")

    user_input = st.text_input("Enter your message:")
    if st.button("Send"):
        if user_input.lower() == 'exit':
            st.stop()
        elif user_input.lower() == 'reset':
            st.session_state.conversation_history = []  # Reset conversation history
            st.info("Conversation history has been reset.")
        else:
            response = txt_gpt(user_input)
            st.write("Pandora:")
            st.info(response)

if __name__ == "__main__":
    main()
