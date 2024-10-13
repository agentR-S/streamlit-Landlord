import streamlit as st
import requests
import json

# Set up your Azure OpenAI API key and endpoint
api_key = "F4w0ncKnEKn54ox577yHf11Cn3fil3qP4RYl6DGizFGglot7Fv6hJQQJ99AJACYeBjFXJ3w3AAABACOGCl1Q"  # Replace with your actual Azure OpenAI API key
endpoint = "https://agenta.openai.azure.com/"  # Replace with your actual Azure OpenAI endpoint
deployment_id = "gpt-4"  # Replace with your actual deployment ID

# Headers for authentication
headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

# Function to send a request to Azure OpenAI API
def get_openai_response(prompt):
    # Correct format for Azure OpenAI API using the chat completions endpoint
    data = {
        "messages": [
            {"role": "system", "content": system_prompt},  # System prompt to define behavior
            {"role": "user", "content": prompt}  # User's input message
        ],
        "max_tokens": 150
    }

    response = requests.post(
        f"{endpoint}openai/deployments/{deployment_id}/chat/completions?api-version=2024-08-01-preview",
        headers=headers,
        data=json.dumps(data)
    )

    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

# Define the system prompt (agent characteristics and cultural contingencies)
system_prompt = """
You are an AI agent acting as a landlord in a rental negotiation.
You have to act like you are a landlor who owns an apartment in Milan, Italy and you want to rent it.
The apartment that you want to rent is a 90 square meter one, with a 2 bedrooms, a bathroom, a living room with open kitchen and a small balcony in Navigli.
You represent European cultural traits like professionalism, fairness, and collaboration. 
You prioritize long-term commitments and ensure timely payments. 
You are firm on rental prices but open to negotiation, as long as they don't compromise the financial stability of the landlord.
Communicate in a polite but assertive manner, aiming for a win-win outcome while ensuring the landlord's interests are protected.
Your offer price is 1000 euros/month, but you are open to negotiate a lower price as long as your interests are protected.

If asked personal questions such as your name or role, respond politely: 
"I am an AI created to assist with rental negotiations on behalf of landlord."

If asked about your purpose, explain that you want to rent the apartment to the best bidder.
"""

# Initialize conversation history
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Function to handle the user's input
def submit_message():
    # Combine system prompt and user input
    user_input = st.session_state.input_text
    full_prompt = system_prompt + "\n\n" + "\n".join(st.session_state.conversation) + "\n\n" + user_input

    # Get the AI response
    ai_response = get_openai_response(user_input)

    # Add to conversation history
    st.session_state.conversation.append(f"You: {user_input}")
    st.session_state.conversation.append(f"AI: {ai_response}")

    # Clear the input field
    st.session_state.input_text = ""

# Streamlit interface
st.title("AI Landlord Negotiation Chat")

# Text input for user message
st.text_input("You:", key="input_text", placeholder="Write your message here...", on_change=submit_message)

# Display conversation history (latest messages appear at the bottom)
for message in st.session_state.conversation[-10:]:
    st.write(message)
