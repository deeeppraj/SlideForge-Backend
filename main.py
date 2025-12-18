from components.llm_model  import mymodel,mymodel2
from components.prompt_and_parser import myprompt,myparser,img_prompt,img_parser
from langchain_core.runnables import RunnableSequence

mychain = RunnableSequence(myprompt,mymodel,myparser)

chain2 = RunnableSequence(img_prompt ,  mymodel2 ,img_parser)


def model_output(payload:dict):
    response = mychain.invoke({
        "title" : payload['title'],
        "description" : payload['description'],
        "slide" :payload['slide'],
        "tg" : payload['tg'],
        "tone":payload['tone'],
        "purpose" : payload['purpose']
    })
    return response

def new_img(payload:dict):
    response = chain2.invoke({
        "title" : payload['title']
    })

    return response

