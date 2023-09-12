import streamlit as st
from conversation_simulation import generate_prompts, generate_responses, evaluate_responses

# Session state initialization if not already done
if "selected_prompt" not in st.session_state:
    st.session_state.selected_prompt = None
if "task" not in st.session_state:
    st.session_state.task = "Create ideas for applying Generative AI in a B2B company"
if "num_prompts" not in st.session_state:
    st.session_state.num_prompts = 4
if 'generated_prompts' not in st.session_state:
    st.session_state.generated_prompts = []
if 'generated_responses' not in st.session_state:
    st.session_state.generated_responses = []
if 'evaluation' not in st.session_state:
    st.session_state.evaluation = ""

# Streamlit UI
st.title("GPT-4 Prompt Optimizer")

# Widgets
st.session_state.task = st.text_area("Enter your task:", st.session_state.task)
st.session_state.num_prompts = st.slider("Number of Prompts:", min_value=2, max_value=10, value=st.session_state.num_prompts)

placeholder_for_prompt = st.empty()
placeholder_for_response = st.empty()
placeholder_for_evaluation = st.empty()

# Start button
if st.button("Start the Process"):
    
    with st.spinner('Generating Prompts...'):
        st.session_state.generated_prompts = generate_prompts(st.session_state.task, st.session_state.num_prompts, st.session_state.selected_prompt)
        placeholder_for_prompt.write("Generated Prompts:")
        placeholder_for_prompt.write(st.session_state.generated_prompts)

    # Radio buttons to select prompt for next round
    if st.session_state.generated_prompts:
        st.session_state.selected_prompt = st.radio("Choose a prompt for the next round:", st.session_state.generated_prompts)

    with st.spinner('Generating Responses...'):
        st.session_state.generated_responses = generate_responses(st.session_state.generated_prompts, st.session_state.task)
        placeholder_for_response.write("Generated Responses:")
        placeholder_for_response.write(st.session_state.generated_responses)

    with st.spinner('Evaluating Responses...'):
        st.session_state.evaluation = evaluate_responses(st.session_state.generated_responses, st.session_state.task)
        placeholder_for_evaluation.markdown("Evaluation:")
        placeholder_for_evaluation.markdown(st.session_state.evaluation)