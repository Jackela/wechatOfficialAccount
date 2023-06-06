import openai
import time
import json
from typing import List, Union, Dict, Optional

openai.api_key = ""  # intialize global api key var

def initialize_api_key():
    with open("project\config.json") as config:
        config = json.load(config)
        openai.api_key = config["openAI"]["apiKey"]

initialize_api_key()

instruct_model = ["ada", "babbage", "curie", "davinci"]
default_max_tokens=3000
default_model = "gpt-3.5-turbo"## default model
default_audio_model = "whisper-1"
# use "model" instead of "engine" !!!!!!!!!!!!!
def create_text_completion(message:str, name:Optional[str]=None, model:str=None, max_tokens:int=None, n:int=1, stream:bool = False, stop:Union[str, List[str]]=None,
        temperature:float=0.5, logit_bias:Dict[str, float]=None, user:str=None) -> str:

    prompt_text = f"Conversation with OpenAI Chatbot:\nUser: {message}\nAI:"


    response = openai.Completion.create(
        engine=model or default_model,
        prompt=prompt_text,
        max_tokens=max_tokens or default_max_tokens,
        n=n,
        stream = stream,
        stop=stop,
        temperature=temperature,
        logit_bias=logit_bias or {},
        user=user or ""
    )

    return response.choices[0].text.strip()

def create_chat_completion(content:str, name:Optional[str]=None, model:str=None, max_tokens:int=None, role:str= "user", 
        temperature:float=1, top_p:float=1, n:int=1, stream:bool=False, stop:Union[str, List[str]]=None,
        presence_penalty:float=0, frequency_penalty:float=0,
        logit_bias:Dict[str, float]=None, user:str=None):
    messages = [
        {"role": role, "content": content}
    ]
    if name is not None:
        messages[0]["name"] = name
    response = openai.ChatCompletion.create(
        model = model or default_model,
        messages = messages,
        temperature = temperature,
        max_tokens = max_tokens or default_max_tokens,
        top_p = top_p,
        n = n,
        stream = stream,
        stop = stop,
        presence_penalty = presence_penalty,
        frequency_penalty = frequency_penalty,
        logit_bias = logit_bias or {},
        user = user or ""
    )
    return response.choices[0].message.content
    
## text-davinci-edit-001 or code-davinci-edit-001
## or use list_edit_model_ids() to get list of models
def create_text_edit(model, message: str, instruction: str):
    if model in list_edit_model_ids():
        response = openai.Edit.create(
            model=model,
            input=message,
            instruction=instruction
        )
        return response.choices[0]
    return False

# image:str is file encoded in base64
def create_image(prompt: str, image_number: int = 1, size: str = "1024x1024", response_format: str = "url"):
    response = openai.Image.create(
        prompt=message,
        n=image_number,
        size=size,
        response_format=response_format
    )
    return response.data

def create_image_edit(prompt: str, image: str, mask: str = None, image_number: int = 1, size: str = "1024x1024", response_format: str = "url"):
    response = openai.Image.create_edit(
        image=image,
        mask=mask,
        prompt=prompt,
        n=image_number,
        size=size,
        response_format=response_format)
    return response.data

def create_image_variation(image: str, image_number: int = 1, size: str = "1024x1024", response_format: str = "url"):
    response = openai.Image.create_variation(
        image=image,
        n=image_number,
        size=size,
        response_format=response_format
    )
    return response.data

def create_embedding(model,message: str):
    if model in list_embedding_model_ids():
        response = openai.Embedding.create(
            model=model,
            input=message
        )
        return response.data[0].embedding
    return False

## only "whisper-1" is available for audio related work
## audio formats: mp3, mp4, mpeg, mpga, m4a, wav, or webm
def create_audio_transcription( file:str, model:str=None, prompt:str = None, response_format:str = "json", temperature:float = 0, language:str = "zh"):
    if model in list_audio_model_ids() or model == None:  
        response = openai.Audio.transcribe(
            file = file,
            model = model or default_audio_model,
            prompt = prompt,
            response_format = response_format,
            temperature = temperature,
            language = language
        )
        return response.text
    return False

## translate into English Only
## 不支持中文（普通话）翻译成英文 （ ？）
## 支持粤语翻译英文
## 支持日文翻译中文
def create_audio_translation(file:str, model:str=None, prompt:str = None, response_format:str = "json", temperature:float = 0):
    if model in list_audio_model_ids() or model == None:  
        response = openai.Audio.translate(
            file = file,
            model = model or default_audio_model,
            prompt = prompt,
            response_format = response_format,
            temperature = temperature,
            ##language = language ## only English is supported
        )
        return response.text
    return False

def create_moderation(message:str):
    return openai.Moderation.create(
        input = message
    )

def list_models():
    return openai.Model.list().data

def list_model_ids():
    model_ids = [model['id']
        for model in list_models() if model['object'] == 'model']
    return model_ids

def list_text_model_ids():
    text_model_ids = [model for model in list_model_ids() if 'text' in model 
    or 'davinci' in model or 'curie' in model or 'ada' in model]
    return text_model_ids

def list_chat_model_ids():
    chat_model_ids = [model['id'] for model in list_models() if 'gpt' in model['id']]
    return chat_model_ids

def list_edit_model_ids():
    edit_model_ids = [model['id'] for model in list_models() if 'edit' in model['id']]
    return edit_model_ids

def list_embedding_model_ids():
    embedding_model_ids = [model['id'] for model in list_models() if 'embedding' in model['id']]
    return embedding_model_ids

## only "whisper-1" is available for audio related work
## modify the code if other models released
def list_audio_model_ids():
    return ["whisper-1"]

def retritve_model(model_id: str):
    return openai.Model.retrieve(model)

def change_default_model(model: str):
    model_ids = list_model_ids()
    if model in model_ids:
        defulat_model = model
        return True
    else:
        return False

def change_default_audio_model(model: str):
    model_ids = list_audio_model_ids()
    if model in model_ids:
        defulat_audio_model = model
        return True
    else:
        return False

## only for "orgnization"
## 组织相关 暂未测试
def list_orgnization_files():
    return openai.File.list().data

def upload_orgnization_file(file:str, purpose:str):
    return openai.File.create(file=file, purpose=purpose)  

def delete_orgnization_file(file_id:str):
    return openai.File.delete(file_id)

def retrieve_orgnization_file(file_id:str):
    return openai.File.retrieve(file_id)

def receive_orgnization_file_content(file_id:str):
    content = openai.File.download(file_id)
    return content

## fine tune
## 用于微调
## 组织相关 暂未测试
def create_fine_tune(file_id, model:str,  n_epochs=4
, batch_size=None, learning_rate_multiplier=None, prompt_loss_weight=0.01
, compute_classification_metrics=False, classification_n_classes=None
, classification_positive_class=None, classification_betas=None
, suffix=None, validation_file_id=None):
    if model in instruct_model:
        return openai.FineTune.create(
            file=file_id,
            model=model,
            n_epochs=n_epochs,
            batch_size=batch_size,
            learning_rate_multiplier=learning_rate_multiplier,
            prompt_loss_weight=prompt_loss_weight,
            compute_classification_metrics=compute_classification_metrics,
            classification_n_classes=classification_n_classes,
            classification_positive_class=classification_positive_class,
            classification_betas=classification_betas,
            suffix=suffix,
            validation_file=validation_file_id
        )
    return False

def list_fine_tunes():
    fine_tunes = openai.FineTune.list().data
    return fine_tunes

def list_fine_tune_events(fine_tune_id):
    fine_tune_events = openai.FineTune.list_events(fine_tune_id).data
    return fine_tune_events

def retrieve_fine_tune(fine_tune_id):
    fine_tune = openai.FineTune.retrieve(fine_tune_id)
    return fine_tune

def cancel_fine_tune(fine_tune_id):
    return openai.FineTune.cancel(fine_tune_id)

## fine_tune_model example: curie:ft-acmeco-2021-03-03-21-44-20
def delete_fine_tune_model(model):
    return openai.Model.delete(model)



# for testing
def get_default_model():
    return default_model

def get_default_audio_model():
    return default_audio_model


if __name__ == "__main__":
    print(list_audio_model_ids())
