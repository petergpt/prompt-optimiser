import openai

def simulate_conversation(initial_message, num_prompts=4, existing_prompt=None):
    meta_prompt = f"{initial_message}\n"
    messages = [{"role": "system", "content": meta_prompt}]

    try:
        prompts = generate_prompts(initial_message, num_prompts, existing_prompt)
        responses = generate_responses(prompts, initial_message)
        evaluation = evaluate_responses(responses, initial_message)
        
        messages.append({"role": "assistant", "content": evaluation})
        
    except openai.error.OpenAIError as e:
        print(f"Error encountered: {e}")

    return messages

def generate_prompts(task, num_prompts=4, existing_prompt=None):
    prompts = []
    for i in range(num_prompts):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": f"Generate one system prompt for the task, take a deep breath and be creative: {task}"}]
        )
        prompts.append(response['choices'][0]['message']['content'].strip())
    if existing_prompt:
        prompts.append(existing_prompt)
    return prompts

def generate_responses(prompts, task):
    responses = []
    for prompt in prompts:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": f"{prompt}: {task}"}]
        )
        responses.append(response['choices'][0]['message']['content'].strip())
    return responses

def evaluate_responses(responses, task):
    evaluation_prompt = f"Given the task '{task}', evaluate the following responses for quality giving a score of 1-5 (5 being the highest). Please create a markdown table showing the feedback and the results.:\n"
    for i, response in enumerate(responses):
        evaluation_prompt += f"Response {i+1}: {response}\n"
    
    evaluation = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": evaluation_prompt}]
    )
    return evaluation['choices'][0]['message']['content'].strip()
