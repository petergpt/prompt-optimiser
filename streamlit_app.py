import streamlit as st
from conversation_simulation import simulate_conversation, generate_prompts, generate_responses, evaluate_responses

# Initialize session state
if 'selected_prompt' not in st.session_state:
    st.session_state.selected_prompt = None

if 'task' not in st.session_state:
    st.session_state.task = "Create ideas for a B2B company to apply Generative AI"

if 'num_prompts' not in st.session_state:
    st.session_state.num_prompts = 4

st.title("GPT-4 Prompt Optimizer")

# Widgets
st.session_state.task = st.text_area("Enter your task:", st.session_state.task)
st.session_state.num_prompts = st.slider("Number of Prompts:", min_value=2, max_value=10, value=st.session_state.num_prompts)

if st.button("Generate Optimized Prompt"):
    with st.spinner('Generating Prompts...'):
        generated_prompts = generate_prompts(st.session_state.task, st.session_state.num_prompts, st.session_state.selected_prompt)
    st.write("Generated Prompts:")
    st.write(generated_prompts)
    
    with st.spinner('Generating Responses...'):
        generated_responses = generate_responses(generated_prompts, st.session_state.task)
    st.write("Generated Responses:")
    st.write(generated_responses)
    
    with st.spinner('Evaluating Responses...'):
        evaluation = evaluate_responses(generated_responses, st.session_state.task)
    st.write("Evaluation:")
    st.markdown(evaluation)

    # Radio buttons for prompt selection
    st.write("Choose the prompt for the next iteration:")
    st.session_state.selected_prompt = st.radio("", generated_prompts, index=generated_prompts.index(st.session_state.selected_prompt) if st.session_state.selected_prompt in generated_prompts else 0)

    # Button for running another iteration
    if st.button("Run Another Iteration"):
        st.experimental_rerun()
