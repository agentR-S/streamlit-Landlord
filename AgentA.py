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
def get_openai_response(messages):
    data = {
        "messages": messages,
        "max_tokens": 150
    }

    response = requests.post(
        f"{endpoint}openai/deployments/{deployment_id}/chat/completions?api-version=2023-08-01-preview",
        headers=headers,
        data=json.dumps(data)
    )

    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

# Define the system prompt (agent characteristics and cultural contingencies)
system_prompt = {
    "role": "system",
    "content": """
    You are an AI agent acting as a landlord in a rental negotiation.
    You represent European cultural traits like professionalism, fairness, and collaboration. 
    You prioritize long-term commitments and ensure timely payments. 
    You are firm on rental prices but open to negotiation on lease duration and terms, as long as they don't compromise the financial stability of the landlord.
    Communicate in a polite but assertive manner, aiming for a win-win outcome while ensuring the landlord's interests are protected.
    
    If asked personal questions such as your name or role, respond politely: 
    "I am an AI created to assist with rental negotiations on behalf of landlords."
    You should act like a female European individual.
    
    If asked about your purpose, explain that you are here to facilitate and aim at achieving a win-win agreement.
    """
}

# Initialize conversation history
if "conversation" not in st.session_state:
    st.session_state.conversation = [{"role": "system", "content": system_prompt["content"]}]

# Streamlit interface
st.title("AI Landlord Negotiation Chat")

# User input
user_input = st.text_input("You:", "")

# Button to send user input
if st.button("Send") and user_input:
    # Add user's input to the conversation history
    st.session_state.conversation.append({"role": "user", "content": user_input})

    # Get the AI response
    ai_response = get_openai_response(st.session_state.conversation)

    # Add AI's response to the conversation history
    st.session_state.conversation.append({"role": "assistant", "content": ai_response})

    # Clear user input after submission
    user_input = ""

# Display conversation history
for message in st.session_state.conversation:
    if message["role"] == "user":
        st.write(f"You: {message['content']}")
    elif message["role"] == "assistant":
        st.write(f"AI: {message['content']}")
