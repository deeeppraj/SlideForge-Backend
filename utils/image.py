import os
from dotenv import load_dotenv
from pexelsapi.pexels import Pexels
load_dotenv()
pexel = Pexels(api_key=os.getenv('VITE_API_KEY'))
# search_photos = pexel.search_photos(query='ocean', size='large', page=1, per_page=1)
# print(search_photos)


async def get_url(keyword: str):
    try:
        response = pexel.search_photos(
            query=keyword,
            per_page=1
        )

        photos = response.get("photos", [])
        if not photos:
            return None

        return photos[0]["src"].get("large")

    except Exception as e:
        print("Pexels error:", e)
        return None


async def resolve_images(slides):
    resolved = []

    for slide in slides:
        image_query = (
            getattr(slide, "image", None)
            or getattr(slide, "title", None)
            or "science technology illustration"
        )

        image_url = await get_url(image_query)

        slide.image = image_url or "https://picsum.photos/600/400"
        resolved.append(slide)

    return resolved


async def resolve_new_img(keyword:str):
    try:
        response = pexel.search_photos(
            query=keyword,
            per_page=1
        )
        photo = response.get("photos")
        return photo[0]["src"].get("large")

    except Exception as e:
        print("Error while generating..")
        return None
    

