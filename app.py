from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import random
import uvicorn

app = FastAPI()


@app.post("/tourist-agent")
async def tourist_agent(request: Request):
    body = await request.json()
    follow_up_possibilities = [
        {"requiresKnowledgeEnrichment": True},
        {"requiresCulturalTranslation": True},
        {"suggestsArtisanConnection": True},
        {}  # No follow-up
    ]

    follow_up = random.choice(follow_up_possibilities)

    return JSONResponse({
        "message": f"Tourist agent processed query about {body.get('query', '')}",
        "location": body.get('location', ''),
        "knowledgeHighlights": [
            "Pottery techniques in Moroccan culture",
            "Traditional craftsmanship in Jamaa el Fna"
        ],
        **follow_up
    })


@app.post("/guide-agent")
async def guide_agent(request: Request):
    body = await request.json()
    return JSONResponse({
        "message": f"Guide agent processed query about {body.get('query', '')}",
        "location": body.get('location', ''),
        "requiresCulturalTranslation": True,
        "translationHints": [
            "Local dialect nuances",
            "Cultural context for terms"
        ]
    })


@app.post("/artisan-agent")
async def artisan_agent(request: Request):
    body = await request.json()
    return JSONResponse({
        "message": f"Artisan agent processed query about {body.get('query', '')}",
        "location": body.get('location', ''),
        "craftDetails": [
            "Traditional pottery techniques",
            "Materials used in local crafts"
        ],
        "suggestsArtisanConnection": True
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
