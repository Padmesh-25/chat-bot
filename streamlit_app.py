import os
import google.generativeai as genai
import streamlit as st

# Set up Google API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyBYESMI0LTsnVgSWVoQ2LYQ28aJ22iXM7w"  # Replace with your actual API key
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Initialize session state for conversation history and additional context
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'additional_context' not in st.session_state:
    st.session_state.additional_context = {
        "user_preferences": {
            "language": "english",
            "tone": "informative",
            "level_of_formality": "casual"
        },
        "recent_topics": [],
        "external_data": {}
    }

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

    # Create a container for the conversation history
    conversation_history_container = st.container()

    # Display the conversation history
    def display_conversation_history():
        for message in st.session_state.conversation_history:
            if message.startswith("Pandora:"):
                conversation_history_container.markdown(f"**Pandora:** {message[7:]}")
            else:
                conversation_history_container.markdown(f"**You:** {message}")

    display_conversation_history()

    # Create a container for the user input field
    user_input_container = st.container()

    with user_input_container:
        # Define handle_keypress function here
        def on_key_press():
            if st.session_state["key_pressed"] == "Enter":
                if user_input.lower() == 'exit':
                    st.stop()
                # ... (rest of your handle_keypress logic)
            st.session_state["key_pressed"] = None  # Reset key press state

        st.on_key_press(on_key_press)
        # Use handle_keypress function here
        user_input = st.text_input("Enter your message:", on_keypress=handle_keypress)

if __name__ == "__main__":
    main()