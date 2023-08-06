from typing import Any, Dict, List, Union
import requests
import os
def evaluate(prompt: List[str] = None, 
             models: List[str] = ['gpt-4', 'mpt-7b-instruct', 'llama-30b'], 
             optimize: Dict = {"cost" : 10} ) -> Dict:    
    """
    This method enables users to compare several models for a specified constraint of cost, quality and latency. 
    Note this API will not generate responses to a prompt but return Konko’s recommended models for a prompt-constraint combination. 
    Args:
        prompt: The input prompt to generate a response for 
        models: The list of models to evaluate from 
        optimize: The cost,quality, and latency constraints
    Examples: 
        >>> import konko
        >>> prompt = 'Summarize the Foundation by Isaac Asimov'
        >>> models = ['gpt-4', 'mpt-7b-instruct', 'llama-30b']
        >>> optimize = {'cost': 10, 'quality': 6}
        >>> konko.evaluate(prompt = prompt, models = models, optimize = optimize)
    """
    baseUrl = os.getenv('KONKO_URL')
    assert baseUrl is not None, "KONKO_URL must be set"

    token = os.getenv('KONKO_TOKEN')

    path = "/evaluate/batch/"  
    url = f"{baseUrl}{path}{models}"   
    headers = {"Authorization": f"Bearer {token}"} 
    params = [{"prompt": p} for p in prompt]         
    response = requests.post(url, headers=headers, json=params)
    try:
        return response.json()[model]
    except requests.JSONDecodeError as e:
        raise BackendError(
            f"Error decoding JSON from {url}. Text response: {response.text}",
            response=response) from e
    

    # response = {"model" : models[random.randrange(0,len(models)-1)],
    #             "cost" : "$" + str(round(random.random(),2)),
    #             "quality" : random.randint(0,10),
    #             "latency" : str(round(random.random(),2)) + 's'
    #             }        