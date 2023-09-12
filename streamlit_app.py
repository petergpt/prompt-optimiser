import streamlit as st
from conversation_simulation import simulate_conversation, generate_prompts, generate_responses, evaluate_responses

# Initialize session state
if 'selected_prompt' not in st.session_state:
    st.session_state.selected_prompt = None

if 'task' not in st.session_state:
    st.session_state.task = "Create ideas for applying Generative AI in a B2B company"

if 'num_prompts' not in st.session_state:
    st.session_state.num_prompts = 4

if 'generated_prompts' not in st.session_state:
    st.session_state.generated_prompts = []

if 'generated_responses' not in st.session_state:
    st.session_state.generated_responses = []

if 'evaluation' not in st.session_state:
    st.session_state.evaluation = ""

# Streamlit UI
st.title("GPT-3 Conversation Starter")

# Widgets
st.session_state.task = st.text_area("Enter your task:", st.session_state.task)
st.session_state.num_prompts = st.slider("Number of Prompts:", min_value=2, max_value=10, value=st.session_state.num_prompts)

if st.button("Generate Prompt"):
    with st.spinner('Generating Prompts...'):
        st.session_state.generated_prompts = generate_prompts(st.session_state.task, st.session_state.num_prompts)
    with st.spinner('Generating Responses...'):
        st.session_state.generated_responses = generate_responses(st.session_state.generated_prompts, st.session_state.task)
    with st.spinner('Evaluating Responses...'):
        st.session_state.evaluation = evaluate_responses(st.session_state.generated_responses, st.session_state.task)

    st.write("Generated Prompts:")
    st.write(st.session_state.generated_prompts)

    st.write("Generated Responses:")
    st.write(st.session_state.generated_responses)

    st.write("Evaluation:")
    st.markdown(st.session_state.evaluation)

# Show radio buttons and button for another iteration only after the first iteration
if st.session_state.generated_prompts:
    st.write("Choose the prompt for the next iteration:")
    st.session_state.selected_prompt = st.radio("", st.session_state.generated_prompts, key='selected_prompt')
    
    if st.button("Run Another Iteration", key='rerun_button'):
        st.experimental_rerun()