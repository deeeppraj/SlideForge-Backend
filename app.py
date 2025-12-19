from fastapi  import FastAPI,Body
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,Field
from main  import model_output , new_img
from utils.image import resolve_images,resolve_new_img
from utils.presentation_maker import create_elegant_slide, create_title_slide, ColorPalette
from fastapi.responses import FileResponse
from pptx import Presentation
from pptx.util import Inches, Pt




import uuid

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserResponse(BaseModel):
   title:str = Field(...,description="Title of presentation")
   description:str = Field(...,description="context needed to build")
   slide:int = Field(...,description="No. of slides in the presentation")
   tg:str = Field(...,description="Target group")
   tone:str = Field(...,description="tone of presentation")
   purpose:str = Field(...,description="purpose of the presentation")


class newImage(BaseModel):
     title:str = Field(...,description="title of the current slide")

@app.post(path='/generate/response')
async def generate_response(payload:UserResponse):
       response = model_output(payload.model_dump())
       response.content = await resolve_images(response.content)


       return  response
 
@app.post(path='/regenerate/img')
async def generate_new_img(payload:newImage):
     response = new_img(payload.model_dump())
     response.query = await resolve_new_img(response.query)
     return response

@app.post(path='/export/ppt')
def export(payload: list = Body(...)):
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)
    
    if payload and len(payload) > 0:
        first_slide = payload[0]
        if "is_title_slide" in first_slide and first_slide["is_title_slide"]:
            create_title_slide(
                prs,
                title=first_slide.get("title", "Presentation"),
                subtitle=first_slide.get("subtitle", ""),
                author=first_slide.get("author", "")
            )
            payload = payload[1:]
    
    for slide in payload:
        create_elegant_slide(prs, slide)
    
    filename = f"/tmp/{uuid.uuid4()}.pptx"
    prs.save(filename)
    
    return FileResponse(
        path=filename,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename="download_presentation.pptx"
    )
    
    

     

     
     
     

  
    