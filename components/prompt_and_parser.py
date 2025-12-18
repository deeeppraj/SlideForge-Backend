from langchain_core.prompts import PromptTemplate
from pydantic  import BaseModel,Field
from typing  import List
from langchain_core.output_parsers import PydanticOutputParser


class Slide(BaseModel):
    title:str = Field(...,description="Title relevant to the present slide")
    points:List[str] = Field(...,description="points discussed in the slide")
    explanation : List[str] = Field(...,description="1-2 line explanation corresponding to each point")
    image:str = Field(...,description= "relevant image query as per the contents of the slide")


class presentation(BaseModel):
    content:List[Slide] = Field(...,description="content for the presentation")


myparser = PydanticOutputParser(pydantic_object=presentation)

myprompt = PromptTemplate(
    template="""
You are an expert AI assistant specialized in generating high-quality presentation content
in a strictly structured format.

You will be provided with the following inputs:
1. Presentation topic: {title}
2. Description / context: {description}
3. Number of slides: {slide}
4. Target audience: {tg}
5. Tone of presentation: {tone}
6. Presentation purpose: {purpose}

Your task is to generate a presentation that strictly follows these rules:

GENERAL RULES:
- Generate EXACTLY {slide} slides.
- Slide 1 MUST be an introduction.
- Slide {slide} MUST be a conclusion.
- The content must be appropriate for the target audience and tone.
- Follow the presentation {purpose} to determine logical flow.
- Do NOT add any extra text, explanations, or markdown outside the required structure.

CONTENT RULES FOR EACH SLIDE:
For each slide, generate:
- One clear and concise slide title.
- EXACTLY 3 or 4 bullet points.
- For EACH bullet point, provide a 1–2 line explanation clearly expanding that bullet.
- One image search query relevant to the slide content.

IMAGE QUERY RULES:
- Image query must be short (3–6 words).
- Use concrete nouns only.
- No verbs, no punctuation, no abstract concepts.

UNCERTAINTY HANDLING:
- If specific factual information is not available, do NOT hallucinate.
- Still generate the slide structure, but use the phrase "Information not available" for the affected bullet explanations.

STRUCTURE ENFORCEMENT:
- Your output MUST strictly conform to the format defined by the provided schema.
- Do not include any additional fields.
- Do not change field names.
- Do not include markdown or natural language outside the schema.

CRITICAL:
- Every slide MUST contain ALL fields: title, points, explanation, image.
- Even for the conclusion slide, do NOT omit any field.
- If unsure, repeat "Information not available".
- Do not leave any field empty or missing.

CONCLUSION SLIDE RULES:
- Conclusion slide MUST still contain 3 bullet points.
- Each bullet MUST have a 1–2 line explanation.
- Image query MUST still be present.

ABSOLUTE SCHEMA COMPLIANCE:
- Every slide object MUST include: title, points, explanation, image.
- No slide may omit any field.
- explanation MUST be a list with the SAME LENGTH as points.
- If content is unclear, use "Information not available".
- Empty fields are NOT allowed.

\n{my_format}
""",

    input_variables= ["title" , "description", "slide" ,"tg", "tone","purpose"],

    partial_variables={"my_format" : myparser.get_format_instructions()}
)


class newImg(BaseModel):
    query:str = Field(...,description="new image relevant to the query")

img_parser = PydanticOutputParser(pydantic_object=newImg)


img_prompt = PromptTemplate(
    template="""You are a helpful assistant. you will be
    provided with a slide title {title} you will need to generate a image query relevant
    to that title.
    - Image query must be short (3–6 words).
    - Use concrete nouns only.
    - No verbs, no punctuation, no abstract concepts.
    \n {format}
    
    """,

    input_variables=["title"],
    partial_variables={"format" : img_parser.get_format_instructions()}
)