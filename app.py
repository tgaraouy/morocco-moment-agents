import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import random
import uvicorn

# Configure logging
log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)

# Read environment variables
DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'
CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')

# Create FastAPI app
app = FastAPI(
    title="Morocco Moment Mock Agents",
    description="Specialized agents for cultural conservation interactions",
    version="0.1.0",
    debug=DEBUG
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/tourist-agent")
async def tourist_agent(request: Request):
    try:
        body = await request.json()
        logger.info(
            f"Tourist agent received query: {body.get('query', 'No query')}")

        follow_up_possibilities = [
            {"requiresKnowledgeEnrichment": True},
            {"requiresCulturalTranslation": True},
            {"suggestsArtisanConnection": True},
            {}  # No follow-up
        ]

        follow_up = random.choice(follow_up_possibilities)

        response = {
            "message": f"Tourist agent processed query about {body.get('query', '')}",
            "location": body.get('location', ''),
            "knowledgeHighlights": [
                "Pottery techniques in Moroccan culture",
                "Traditional craftsmanship in Jamaa el Fna"
            ],
            **follow_up
        }

        logger.debug(f"Tourist agent response: {response}")
        return JSONResponse(response)

    except Exception as e:
        logger.error(f"Error in tourist agent: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": str(e)
            }
        )


@app.post("/guide-agent")
async def guide_agent(request: Request):
    try:
        body = await request.json()
        logger.info(
            f"Guide agent received query: {body.get('query', 'No query')}")

        response = {
            "message": f"Guide agent processed query about {body.get('query', '')}",
            "location": body.get('location', ''),
            "requiresCulturalTranslation": True,
            "translationHints": [
                "Local dialect nuances",
                "Cultural context for terms"
            ]
        }

        logger.debug(f"Guide agent response: {response}")
        return JSONResponse(response)

    except Exception as e:
        logger.error(f"Error in guide agent: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": str(e)
            }
        )


@app.post("/artisan-agent")
async def artisan_agent(request: Request):
    try:
        body = await request.json()
        logger.info(
            f"Artisan agent received query: {body.get('query', 'No query')}")

        response = {
            "message": f"Artisan agent processed query about {body.get('query', '')}",
            "location": body.get('location', ''),
            "craftDetails": [
                "Traditional pottery techniques",
                "Materials used in local crafts"
            ],
            "suggestsArtisanConnection": True
        }

        logger.debug(f"Artisan agent response: {response}")
        return JSONResponse(response)

    except Exception as e:
        logger.error(f"Error in artisan agent: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": str(e)
            }
        )


@app.get("/health")
async def health_check():
    """
    Simple health check endpoint
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        reload=DEBUG
    )
