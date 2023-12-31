from concurrent.futures import ThreadPoolExecutor, as_completed
import openai

openai.log='debug'

def generate_prompts(task, num_prompts=4, existing_prompt=None):
    prompts = []
    with ThreadPoolExecutor(max_workers=num_prompts) as executor:
        future_to_prompt = {executor.submit(openai.ChatCompletion.create,
                                            model="gpt-4",
                                            messages=[{"role": "system", 
                                                       "content": f"Generate one system prompt for the task, take a deep breath and be creative: {task}"}]
                                           ): i for i in range(num_prompts)}
        for future in as_completed(future_to_prompt):
            try:
                prompt = future.result()['choices'][0]['message']['content'].strip()
                prompts.append(prompt)
            except Exception as exc:
                print('%r generated an exception: %s' % (future_to_prompt[future], exc))

    if existing_prompt:
        prompts.append(existing_prompt)
    return prompts

def generate_responses(prompts, task):
    responses = []
    if not prompts:  # check if prompts is empty
        return responses
    with ThreadPoolExecutor(max_workers=len(prompts)) as executor:
        future_to_response = {executor.submit(openai.ChatCompletion.create,
                                              model="gpt-4",
                                              messages=[{"role": "system", "content": f"{prompt}: {task}. Keep it short."}],
                                              max_tokens=500,
                                              top_p=1,
                                              frequency_penalty=0,
                                              presence_penalty=0
                                             ): prompt for prompt in prompts}
        for future in as_completed(future_to_response):
            try:
                response = future.result()['choices'][0]['message']['content'].strip()
                responses.append(response)
            except Exception as exc:
                print('%r generated an exception: %s' % (future_to_response[future], exc))
            
    return responses

def evaluate_responses(responses, task):
    if not responses:  # check if responses is empty
        return ""
    evaluation_prompt = f"Evaluate the quality of the following responses for the task '{task}', giving a score between 1 and 5 (5 being the highest). Create a markdown table showing the feedback and the results.:\n"
    for i, response in enumerate(responses):
        evaluation_prompt += f"Response {i+1}: {response}\n"
    
    evaluation = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": evaluation_prompt}]
    )
    return evaluation['choices'][0]['message']['content'].strip()