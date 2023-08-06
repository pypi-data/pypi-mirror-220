from typing import List, Optional, Dict, Union
from fastapi import APIRouter, HTTPException, Body, Depends
from pydantic import BaseModel, Field
from konko.utils.constants import TIMEOUT
from konko.utils.logs import BackendError, get_env_variable
import requests
import os
import json
from fastapi import Depends
from fastapi.security.api_key import APIKeyHeader

class GeneratePayload(BaseModel):
    prompt: List[str]
    models: List[str]
    prompt_file: Optional[str]
    prompt_delimiter: Optional[str]
    mode: str

generate_router = APIRouter()

api_key_header = APIKeyHeader(name="x-api-key", description="API key to authorize requests")

def get_api_key() -> str:
    if "KONKO_TOKEN" in os.environ:
        return os.environ["KONKO_TOKEN"]
    elif api_key_header:
        return api_key_header
    else:
        raise HTTPException(
            status_code=403, detail="Could not validate credentials. API key should be in the 'x-api-key' header or the 'API_KEY' environment variable."
        )

@generate_router.post("/text",
        response_model=List[Dict[str, Union[str, float, int]]],
        tags=["Generate"],
        summary="GenerateText",
        description="This endpoint generates a response for a user-specified prompt(s), set of models.")
def generate_text_api(
        prompt: List[str] = Body(default=["Summarize the Foundation by Isaac Asimov"],
                                 description="The list of prompts for which to generate responses. Each prompt should be a separate string in the list.\n" \
                                 "Suggested Example: Summarize the Foundation by Isaac Asimov",
                                 examples=["Summarize the Foundation by Isaac Asimov"]),
        models: List[str] = Body(default=["mosaicml/mpt-7b-chat"],
                                 description="A single model to be used for generating responses. We plan to support multiple models in the near future.\n" \
                                 "Suggested Example: mosaicml/mpt-7b-chat",
                                 examples=["mosaicml/mpt-7b-chat"]),
        mode: str = Body(default='batch', 
                         description="Defines the mode of operation. Current available option is 'batch'. We plan to support 'stream' in the near future.",
                         examples=["batch"]),
        prompt_file: Optional[str] =  Body(default=None, 
                                          description="Optional file path to a file containing prompts. This is used as an alternative to specifying prompts in the 'prompt' field.",
                                          examples=None),
        prompt_delimiter: Optional[str] = Body(default=None, 
                                               description="If 'prompt_file' is specified, this defines the separator string that divides separate prompts in the file."),
        api_key: str = Depends(api_key_header)
    ):
    models = [model.replace('/', '--') for model in models] 
    baseUrl = get_env_variable('KONKO_URL')
    headers = {"x-api-key": api_key}

    if prompt_file:
        with open(prompt_file, "r") as f:
            prompt = f.read().split(prompt_delimiter)
    path = '/generate/text/' 
    url = f"{baseUrl}{path}"
    payload = GeneratePayload(prompt=prompt, models=models, prompt_file=prompt_file, prompt_delimiter=prompt_delimiter, mode=mode)
    response = generate_request(url=url, headers=headers, payload=payload.dict(), stream=payload.mode == 'stream')
    return response

def generate_request(url: str, headers: Dict, payload: Dict, stream: bool) -> List[Dict[str, Union[str, float, int]]]:
    response = requests.post(url, 
                             headers=headers, 
                             json=payload,
                             timeout=TIMEOUT,
                             stream=stream)
    
    if response.status_code != 200:  
        print(f"Response code: {response.status_code}, reason: {response.reason}, response text: {response.text}")
        raise HTTPException(status_code=response.status_code, detail=response.text)
        
    result = []
    if stream:
        for chunk in response.iter_lines(chunk_size=None, decode_unicode=True):            
            chunk = chunk.strip()
            if not chunk:
                continue
            result.append(json.loads(chunk))
    else:
        data = response.json()
        if isinstance(data, list):
            result = data
        elif isinstance(data, dict):
            result = [data]
        elif isinstance(data, str):
            result = json.loads(data) 
        else:
            raise ValueError("Unexpected response format")
    return result

def generate_text(prompt: Union[List[str], str], 
                  model_ids: Union[List[str], str], 
                  mode: str = 'batch', 
                  prompt_file: Optional[str] = None, 
                  prompt_delimiter: Optional[str] = None):
    
    # If prompt is a string, convert it to a list
    if isinstance(prompt, str):
        prompt = [prompt]
    
    # If model_ids is a string, convert it to a list
    if isinstance(model_ids, str):
        model_ids = [model_ids]

    api_key = get_api_key()
    return generate_text_api(prompt, model_ids, mode, prompt_file, prompt_delimiter, api_key)

