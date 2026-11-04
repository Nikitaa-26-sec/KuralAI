
import os
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from rag.llm import generate_answer
from rag.retrieval import retrieve_relevant_chunks
from rag.vector_store import collection


app = FastAPI(
    title="KuralAI Legal Assistance API",
    version="1.0.0",
    description="Multilingual legal information assistant using RAG.",
)

# Configure permitted frontend origins.
allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "KURALAI_CORS_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    language: Literal["English", "Tamil", "Hindi"] = "English"
    mode: Literal["legal", "fir"] = "legal"


class Source(BaseModel):
    title: str
    page: int
    chunk: int
    distance: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source] = Field(default_factory=list)
    language: str
    mode: str


FIR_GUIDANCE = {
    "English": """
FIR PROCESS ASSISTANCE

KuralAI provides information about the reporting process. It does not
register or submit an FIR.

1. Where to report:
   Visit or contact the nearest police station. For an emergency in India,
   call 112. For cybercrime, use https://cybercrime.gov.in/.

2. Information to prepare:
   - Your name and contact details.
   - Date, approximate time and location of the incident.
   - A clear description of what happened.
   - Available evidence, such as messages, photographs, documents or
     transaction details, where relevant.
   - Details of witnesses, if any.

3. What happens next:
   Explain the incident to the police and provide the available information.
   Ask for the FIR number or an acknowledgement where applicable.
   Keep copies of documents and note the details of the police station.

4. If the police do not register the information:
   Ask for the reason and seek guidance from a senior police officer or
   a qualified legal professional about the appropriate next step.
   Procedures can depend on the facts and applicable law.

5. Important:
   If anyone is in immediate danger, contact emergency services.
   Do not delay urgent reporting to use this chatbot.

Official services:
Emergency: https://112.gov.in/
National Cyber Crime Reporting Portal: https://cybercrime.gov.in/

This is general information, not legal advice. KuralAI does not file,
register or transmit complaints.
""",
    "Tamil": """
FIR பதிவு செய்வதற்கான வழிகாட்டுதல்

KuralAI FIR பதிவு செய்யாது அல்லது புகாரைச் சமர்ப்பிக்காது.
FIR நடைமுறை பற்றிய பொதுவான தகவல்களை மட்டுமே வழங்குகிறது.

1. எங்கு புகார் அளிக்கலாம்:
   அருகிலுள்ள காவல் நிலையத்தை அணுகவும். அவசரநிலைக்கு இந்தியாவில் 112
   என்ற எண்ணை அழைக்கவும். இணையக் குற்றங்களுக்கு
   https://cybercrime.gov.in/ என்ற இணையதளத்தைப் பயன்படுத்தவும்.

2. தயாராக வைத்திருக்க வேண்டிய தகவல்கள்:
   - உங்கள் பெயர் மற்றும் தொடர்பு விவரங்கள்.
   - சம்பவம் நடந்த தேதி, நேரம் மற்றும் இடம்.
   - நடந்த சம்பவத்தின் தெளிவான விளக்கம்.
   - தொடர்புடைய செய்திகள், புகைப்படங்கள், ஆவணங்கள் அல்லது பரிவர்த்தனை
     விவரங்கள் போன்ற ஆதாரங்கள்.
   - சாட்சிகள் இருந்தால் அவர்களின் விவரங்கள்.

3. புகார் அளித்த பிறகு:
   காவல்துறையிடம் சம்பவத்தை விளக்கி, கிடைக்கும் தகவல்களை வழங்கவும்.
   பொருந்தும் இடங்களில் FIR எண் அல்லது ஒப்புதல் விவரத்தைக் கேட்டு
   வைத்துக்கொள்ளவும்.

4. புகாரைப் பதிவு செய்ய மறுத்தால்:
   மறுப்பிற்கான காரணத்தைக் கேட்டு, மூத்த காவல் அதிகாரி அல்லது
   தகுதியான சட்ட நிபுணரிடம் அடுத்தகட்ட நடவடிக்கை குறித்து ஆலோசனை பெறவும்.

அவசர உதவி: https://112.gov.in/
இணையக் குற்ற புகார்: https://cybercrime.gov.in/

இது பொதுவான தகவல் மட்டுமே; சட்ட ஆலோசனை அல்ல.
KuralAI புகாரைப் பதிவு செய்யவோ சமர்ப்பிக்கவோ செய்யாது.
""",
    "Hindi": """
FIR प्रक्रिया की जानकारी

KuralAI केवल FIR प्रक्रिया के बारे में सामान्य जानकारी देता है।
यह FIR दर्ज नहीं करता और न ही शिकायत जमा करता है।

1. शिकायत कहाँ करें:
   नजदीकी पुलिस स्टेशन से संपर्क करें। भारत में आपातकाल के लिए 112 पर
   कॉल करें। साइबर अपराध के लिए https://cybercrime.gov.in/ पर जाएँ।

2. ये जानकारी तैयार रखें:
   - आपका नाम और संपर्क विवरण।
   - घटना की तारीख, अनुमानित समय और स्थान।
   - घटना का स्पष्ट विवरण।
   - उपलब्ध सबूत, जैसे संदेश, फोटो, दस्तावेज या लेन-देन का विवरण।
   - गवाहों की जानकारी, यदि उपलब्ध हो।

3. शिकायत के बाद:
   पुलिस को घटना समझाएँ और उपलब्ध जानकारी दें।
   जहाँ लागू हो, FIR नंबर या पावती माँगें और उसका रिकॉर्ड रखें।

4. यदि पुलिस शिकायत दर्ज करने से मना करे:
   कारण पूछें और वरिष्ठ पुलिस अधिकारी या योग्य कानूनी विशेषज्ञ से
   अगले उचित कदम के बारे में सलाह लें।

आपातकालीन सहायता: https://112.gov.in/
राष्ट्रीय साइबर अपराध पोर्टल: https://cybercrime.gov.in/

यह सामान्य जानकारी है, कानूनी सलाह नहीं।
KuralAI शिकायत दर्ज या जमा नहीं करता।
""",
}


@app.get("/")
def root():
    return {
        "message": "KuralAI API is running",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    try:
        return {
            "status": "ok",
            "indexed_chunks": collection.count(),
        }
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="The document database is unavailable.",
        )


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    message = request.message.strip()

    if not message:
        raise HTTPException(
            status_code=422,
            detail="Please enter a question.",
        )

    # FIR mode provides process information only.
    # It does not create, register or submit complaints.
    if request.mode == "fir":
        return ChatResponse(
            answer=FIR_GUIDANCE[request.language],
            sources=[],
            language=request.language,
            mode="fir",
        )

    # Legal Q&A uses the existing RAG pipeline.
    try:
        chunks = retrieve_relevant_chunks(message, top_k=4)

        if not chunks:
            return ChatResponse(
                answer=(
                    "I could not find a relevant passage in the legal "
                    "documents currently indexed by KuralAI. Please try "
                    "another question or consult an authoritative legal "
                    "source or qualified professional."
                ),
                sources=[],
                language=request.language,
                mode="legal",
            )

        answer = generate_answer(
            question=message,
            retrieved_chunks=chunks,
            language=request.language,
        )

        sources = [
            Source(
                title=str(chunk["source"]),
                page=int(chunk["page"]),
                chunk=int(chunk["chunk"]),
                distance=round(float(chunk["distance"]), 4),
            )
            for chunk in chunks
        ]

        return ChatResponse(
            answer=answer,
            sources=sources,
            language=request.language,
            mode="legal",
        )

    except Exception:
        # Keep internal paths, prompts and exception details out of responses.
        raise HTTPException(
            status_code=503,
            detail=(
                "KuralAI could not generate a response right now. "
                "Please check that the AI service and document database "
                "are running, then try again."
            ),
        )

