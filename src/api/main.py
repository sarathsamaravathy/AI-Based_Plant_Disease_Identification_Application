"""FastAPI Application - Main REST API"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import logging
import os
import uuid

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Plant Disease Identifier API",
    description="AI-powered multilingual plant disease identification",
    version="0.1.0"
)

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: str

MOCK_IMAGE_DIAGNOSIS = {
    "en": {
        "disease_name": "Leaf Blight (Demo — AI pipeline not yet connected)",
        "symptoms": [
            "Brown or yellow spots on leaves",
            "Wilting edges",
            "Discoloration spreading from leaf tip",
        ],
        "treatment_recommendations": [
            "Remove and destroy infected plant parts",
            "Apply copper-based fungicide every 7–10 days",
            "Avoid overhead irrigation to reduce leaf wetness",
            "Ensure adequate spacing for airflow between plants",
        ],
        "preventive_measures": [
            "Use disease-resistant varieties",
            "Rotate crops each season",
            "Keep field free of plant debris after harvest",
        ],
        "explanation": "Your image was received and processed. This is a placeholder result — the full AI vision model and LLM pipeline will replace this with a real diagnosis once connected.",
    },
    "hi": {
        "disease_name": "पत्ता झुलसा रोग (डेमो — AI पाइपलाइन अभी जुड़ी नहीं है)",
        "symptoms": [
            "पत्तियों पर भूरे या पीले धब्बे",
            "पत्तियों के किनारों का मुरझाना",
            "पत्ती की नोक से फैलता रंग परिवर्तन",
        ],
        "treatment_recommendations": [
            "संक्रमित पौधे के हिस्सों को हटाकर नष्ट करें",
            "हर 7–10 दिन में कॉपर आधारित फफूंदनाशक का छिड़काव करें",
            "पत्तियों की नमी कम करने के लिए ऊपर से सिंचाई से बचें",
            "हवा के प्रवाह के लिए पौधों के बीच पर्याप्त दूरी रखें",
        ],
        "preventive_measures": [
            "रोग प्रतिरोधी किस्मों का उपयोग करें",
            "हर मौसम में फसल चक्र अपनाएं",
            "फसल कटाई के बाद खेत से पौधे अवशेष हटाएं",
        ],
        "explanation": "आपकी छवि प्राप्त हो गई है। यह एक प्रदर्शन परिणाम है — पूर्ण AI दृष्टि मॉडल जुड़ने के बाद वास्तविक निदान मिलेगा।",
    },
    "ta": {
        "disease_name": "இலை கருகல் நோய் (டெமோ — AI பைப்லைன் இன்னும் இணைக்கப்படவில்லை)",
        "symptoms": [
            "இலைகளில் பழுப்பு அல்லது மஞ்சள் புள்ளிகள்",
            "இலை விளிம்புகள் வாடுதல்",
            "இலை நுனியிலிருந்து நிறமாற்றம் பரவுதல்",
        ],
        "treatment_recommendations": [
            "பாதிக்கப்பட்ட தாவர பகுதிகளை அகற்றி அழியுங்கள்",
            "7–10 நாட்களுக்கு ஒரு முறை செம்பு அடிப்படையிலான பூஞ்சாண மருந்து தெளிக்கவும்",
            "இலை ஈரப்பதத்தை குறைக்க மேல்நோக்கி நீர்ப்பாசனம் தவிர்க்கவும்",
            "காற்றோட்டத்திற்கு போதுமான இடைவெளியில் நடவு செய்யுங்கள்",
        ],
        "preventive_measures": [
            "நோய் எதிர்ப்பு திறன் கொண்ட ரகங்களை பயன்படுத்துங்கள்",
            "ஒவ்வொரு பருவமும் பயிர் சுழற்சி பின்பற்றுங்கள்",
            "அறுவடைக்கு பிறகு வயலை சுத்தமாக வைத்திருங்கள்",
        ],
        "explanation": "உங்கள் படம் பெறப்பட்டது. இது ஒரு மாதிரி முடிவு — முழு AI மாதிரி இணைக்கப்பட்டவுடன் உண்மையான நோயறிதல் கிடைக்கும்.",
    },
    "te": {
        "disease_name": "ఆకు తెగులు (డెమో — AI పైప్‌లైన్ ఇంకా అనుసంధానం కాలేదు)",
        "symptoms": [
            "ఆకులపై గోధుమ లేదా పసుపు మచ్చలు",
            "ఆకు అంచులు వాడిపోవడం",
            "ఆకు చివర నుండి రంగు మారడం వ్యాపించడం",
        ],
        "treatment_recommendations": [
            "సోకిన మొక్క భాగాలను తొలగించి నాశనం చేయండి",
            "7–10 రోజులకు ఒకసారి రాగి ఆధారిత శిలీంద్ర నాశిని పిచికారీ చేయండి",
            "ఆకు తడిని తగ్గించడానికి పైన నుండి నీటిపారుదల మానండి",
            "గాలి ప్రసరణకు మొక్కల మధ్య తగిన అంతరం పాటించండి",
        ],
        "preventive_measures": [
            "వ్యాధి-నిరోధక రకాలు ఉపయోగించండి",
            "ప్రతి సీజన్‌లో పంట మార్పిడి పాటించండి",
            "పంట కోత తర్వాత పొలాన్ని శుభ్రంగా ఉంచండి",
        ],
        "explanation": "మీ చిత్రం స్వీకరించబడింది. ఇది ఒక డెమో ఫలితం — పూర్తి AI మోడల్ అనుసంధానమైన తర్వాత నిజమైన నిర్ధారణ లభిస్తుంది.",
    },
    "ka": {
        "disease_name": "ಎಲೆ ಸುಡು ರೋಗ (ಡೆಮೋ — AI ಪೈಪ್‌ಲೈನ್ ಇನ್ನೂ ಸಂಪರ್ಕಗೊಂಡಿಲ್ಲ)",
        "symptoms": [
            "ಎಲೆಗಳ ಮೇಲೆ ಕಂದು ಅಥವಾ ಹಳದಿ ಚುಕ್ಕೆಗಳು",
            "ಎಲೆ ಅಂಚುಗಳು ಬಾಡುವುದು",
            "ಎಲೆ ತುದಿಯಿಂದ ಬಣ್ಣ ಬದಲಾವಣೆ ಹರಡುವುದು",
        ],
        "treatment_recommendations": [
            "ಸೋಂಕಿತ ಭಾಗಗಳನ್ನು ತೆಗೆದು ನಾಶ ಮಾಡಿ",
            "7–10 ದಿನಗಳಿಗೊಮ್ಮೆ ತಾಮ್ರ ಆಧಾರಿತ ಶಿಲೀಂಧ್ರನಾಶಕ ಸಿಂಪಡಿಸಿ",
            "ಎಲೆ ತೇವವನ್ನು ಕಡಿಮೆ ಮಾಡಲು ಮೇಲ್ಭಾಗದ ನೀರಾವರಿ ತಪ್ಪಿಸಿ",
            "ಗಾಳಿ ಸಂಚಾರಕ್ಕಾಗಿ ಸಸ್ಯಗಳ ನಡುವೆ ಸಾಕಷ್ಟು ಅಂತರ ಇಡಿ",
        ],
        "preventive_measures": [
            "ರೋಗ-ನಿರೋಧಕ ತಳಿಗಳನ್ನು ಬಳಸಿ",
            "ಪ್ರತಿ ಋತುವಿನಲ್ಲೂ ಬೆಳೆ ಮರಟು ಅನುಸರಿಸಿ",
            "ಕೊಯ್ಲಿನ ನಂತರ ಹೊಲವನ್ನು ಸ್ವಚ್ಛವಾಗಿ ಇಡಿ",
        ],
        "explanation": "ನಿಮ್ಮ ಚಿತ್ರ ಸ್ವೀಕರಿಸಲಾಗಿದೆ. ಇದು ಒಂದು ಡೆಮೋ ಫಲಿತಾಂಶ — ಸಂಪೂರ್ಣ AI ಮಾದರಿ ಸಂಪರ್ಕಗೊಂಡ ನಂತರ ನಿಜವಾದ ರೋಗನಿರ್ಣಯ ಸಿಗುತ್ತದೆ.",
    },
    "ml": {
        "disease_name": "ഇല കരിച്ചിൽ രോഗം (ഡെമോ — AI പൈപ്പ്‌ലൈൻ ഇനിയും ബന്ധിപ്പിച്ചിട്ടില്ല)",
        "symptoms": [
            "ഇലകളിൽ തവിട്ട് അല്ലെങ്കിൽ മഞ്ഞ പുള്ളികൾ",
            "ഇലയുടെ അരികുകൾ വാടുന്നു",
            "ഇലയുടെ അഗ്രഭാഗത്ത് നിന്ന് നിറം മാറ്റം പടരുന്നു",
        ],
        "treatment_recommendations": [
            "രോഗബാധിത ഭാഗങ്ങൾ നീക്കം ചെയ്ത് നശിപ്പിക്കുക",
            "7–10 ദിവസത്തിൽ ഒരിക്കൽ ചെമ്പ് അടിസ്ഥാനമാക്കിയ കുമിൾനാശിനി തളിക്കുക",
            "ഇലകളുടെ നനവ് കുറയ്ക്കാൻ മുകളിൽ നിന്ന് ജലസേചനം ഒഴിവാക്കുക",
            "വായുസഞ്ചാരത്തിനായി ചെടികൾക്കിടയിൽ മതിയായ അകലം പാലിക്കുക",
        ],
        "preventive_measures": [
            "രോഗ പ്രതിരോധ ശേഷിയുള്ള ഇനങ്ങൾ ഉപയോഗിക്കുക",
            "ഓരോ സീസണിലും വിള പ്രദക്ഷിണം നടത്തുക",
            "വിളവെടുപ്പിന് ശേഷം വയൽ ശുചിയായി സൂക്ഷിക്കുക",
        ],
        "explanation": "നിങ്ങളുടെ ചിത്രം ലഭിച്ചു. ഇത് ഒരു ഡെമോ ഫലമാണ് — പൂർണ AI മോഡൽ ബന്ധിപ്പിച്ചതിന് ശേഷം യഥാർത്ഥ രോഗനിർണ്ണയം ലഭിക്കും.",
    },
    "mr": {
        "disease_name": "पान करपा रोग (डेमो — AI पाइपलाइन अद्याप जोडलेली नाही)",
        "symptoms": [
            "पानांवर तपकिरी किंवा पिवळे डाग",
            "पानांचे कडे कोमेजणे",
            "पानाच्या टोकापासून रंग बदल पसरणे",
        ],
        "treatment_recommendations": [
            "बाधित पानांचे भाग काढून नष्ट करा",
            "7–10 दिवसांनी तांबे-आधारित बुरशीनाशक फवारा",
            "पाने ओली राहू नयेत म्हणून वरून पाणी देणे टाळा",
            "हवा खेळती राहण्यासाठी रोपांमध्ये पुरेसे अंतर ठेवा",
        ],
        "preventive_measures": [
            "रोगप्रतिरोधक वाणांचा वापर करा",
            "प्रत्येक हंगामात पीक बदल करा",
            "काढणीनंतर शेतातील उरलेले अवशेष काढून टाका",
        ],
        "explanation": "तुमची प्रतिमा मिळाली आहे. हा डेमो निकाल आहे — पूर्ण AI मॉडेल जोडल्यानंतर खरे निदान मिळेल.",
    },
    "gu": {
        "disease_name": "પાંદડા સૂકારો રોગ (ડેમો — AI પાઇપલાઇન હજુ જોડાઈ નથી)",
        "symptoms": [
            "પાંદડાઓ પર ભૂરા અથવા પીળા ટપકાં",
            "પાંદડાની કિનારીઓ સૂકાવી",
            "પાંદડાની ટોચ પરથી રંગ ફેરફાર ફેલાવો",
        ],
        "treatment_recommendations": [
            "સંક્રમિત ભાગો દૂર કરી નષ્ટ કરો",
            "7–10 દિવસે એકવાર કૉપર-આધારિત ફૂગનાશક છાંટો",
            "પાંદડાની ભીનાશ ઘટાડવા ઉપર થી સિંચાઈ ટાળો",
            "હવાઉજાસ માટે છોડ વચ્ચે પૂરતું અંતર રાખો",
        ],
        "preventive_measures": [
            "રોગ-પ્રતિરોધક જાતોનો ઉપયોગ કરો",
            "દર સીઝનમાં પાક ફેરબદલ કરો",
            "લણણી પછી ખેતરમાંથી પાકના અવશેષ દૂર કરો",
        ],
        "explanation": "તમારી છબી મળી ગઈ. આ ડેમો પરિણામ છે — સંપૂર્ણ AI મૉડલ જોડાય ત્યારે સાચું નિદાન મળશે.",
    },
    "bn": {
        "disease_name": "পাতা ঝলসানো রোগ (ডেমো — AI পাইপলাইন এখনো সংযুক্ত হয়নি)",
        "symptoms": [
            "পাতায় বাদামী বা হলুদ দাগ",
            "পাতার কিনারা নেতিয়ে পড়া",
            "পাতার ডগা থেকে রং পরিবর্তন ছড়িয়ে পড়া",
        ],
        "treatment_recommendations": [
            "আক্রান্ত অংশ সরিয়ে নষ্ট করুন",
            "৭–১০ দিন পরপর তামা-ভিত্তিক ছত্রাকনাশক স্প্রে করুন",
            "পাতার আর্দ্রতা কমাতে উপর থেকে সেচ এড়িয়ে চলুন",
            "বায়ু চলাচলের জন্য গাছের মাঝে পর্যাপ্ত দূরত্ব রাখুন",
        ],
        "preventive_measures": [
            "রোগ-প্রতিরোধী জাত ব্যবহার করুন",
            "প্রতি মৌসুমে ফসল পরিবর্তন করুন",
            "ফসল কাটার পর মাঠ পরিষ্কার রাখুন",
        ],
        "explanation": "আপনার ছবি পাওয়া গেছে। এটি একটি ডেমো ফলাফল — পূর্ণ AI মডেল সংযুক্ত হলে আসল রোগ নির্ণয় পাবেন।",
    },
}

MOCK_TEXT_DIAGNOSIS = {
    "en": {
        "disease_name": "Powdery Mildew (Demo — AI pipeline not yet connected)",
        "symptoms": ["White powdery coating on leaves", "Yellowing around affected areas", "Stunted new growth"],
        "treatment_recommendations": ["Apply neem oil or potassium bicarbonate spray", "Remove heavily infected leaves", "Improve air circulation around plants"],
        "preventive_measures": ["Avoid over-fertilizing with nitrogen", "Water at base of plant, not on foliage", "Plant resistant varieties"],
        "explanation": "Your symptom description was received. This is a placeholder result — the LLM text analysis pipeline will replace this once connected.",
    },
    "hi": {
        "disease_name": "चूर्णिल आसिता (डेमो — AI पाइपलाइन अभी जुड़ी नहीं है)",
        "symptoms": ["पत्तियों पर सफेद पाउडर जैसी परत", "प्रभावित क्षेत्र के आसपास पीलापन", "नई वृद्धि का रुकना"],
        "treatment_recommendations": ["नीम तेल या पोटेशियम बाइकार्बोनेट का स्प्रे करें", "भारी संक्रमित पत्तियाँ हटाएं", "पौधों के चारों ओर हवा का प्रवाह बेहतर करें"],
        "preventive_measures": ["नाइट्रोजन से अत्यधिक उर्वरकता से बचें", "पत्तियों पर नहीं, पौधे के आधार पर पानी दें", "प्रतिरोधी किस्में लगाएं"],
        "explanation": "आपके लक्षणों का विवरण प्राप्त हुआ। यह एक प्रदर्शन परिणाम है — LLM पाइपलाइन जुड़ने के बाद वास्तविक निदान मिलेगा।",
    },
    "ta": {
        "disease_name": "தூள் பூஞ்சான் நோய் (டெமோ — AI பைப்லைன் இன்னும் இணைக்கப்படவில்லை)",
        "symptoms": ["இலைகளில் வெள்ளை தூள் போன்ற பூச்சு", "பாதிக்கப்பட்ட பகுதிகளில் மஞ்சளாதல்", "புதிய வளர்ச்சி தடைபடுதல்"],
        "treatment_recommendations": ["வேப்ப எண்ணெய் அல்லது பொட்டாசியம் பைகார்பனேட் தெளிக்கவும்", "கடுமையாக சோகின இலைகளை அகற்றுங்கள்", "காற்றோட்டத்தை மேம்படுத்துங்கள்"],
        "preventive_measures": ["தழைச்சத்துடன் அதிக உரமிடுவதை தவிர்க்கவும்", "இலைகளில் அல்ல, தாவரத்தின் அடியில் நீர் பாய்ச்சவும்", "நோய் எதிர்ப்பு ரகங்களை நடவு செய்யுங்கள்"],
        "explanation": "உங்கள் அறிகுறி விவரண பெறப்பட்டது. இது ஒரு மாதிரி முடிவு — LLM பைப்லைன் இணைந்தவுடன் உண்மையான நோயறிதல் கிடைக்கும்.",
    },
    "te": {
        "disease_name": "పొడి బూజు తెగులు (డెమో — AI పైప్‌లైన్ ఇంకా అనుసంధానం కాలేదు)",
        "symptoms": ["ఆకులపై తెల్లటి పొడి పూత", "ప్రభావిత ప్రాంతాల చుట్టూ పసుపు పచ్చగా మారడం", "కొత్త వృద్ధి ఆగిపోవడం"],
        "treatment_recommendations": ["వేప నూనె లేదా పొటాషియం బైకార్బోనేట్ స్ప్రే చేయండి", "తీవ్రంగా సోకిన ఆకులు తొలగించండి", "మొక్కల చుట్టూ గాలి ప్రసరణ మెరుగుపరచండి"],
        "preventive_measures": ["నత్రజనితో అధిక ఎరువు వేయడం మానండి", "ఆకులపై కాదు, మొక్క మొదట్లో నీరు పోయండి", "నిరోధక రకాలు నాటండి"],
        "explanation": "మీ లక్షణ వివరణ స్వీకరించబడింది. ఇది ఒక డెమో ఫలితం — LLM పైప్‌లైన్ అనుసంధానమైన తర్వాత నిజమైన నిర్ధారణ లభిస్తుంది.",
    },
    "ka": {
        "disease_name": "ಬೂದು ರೋಗ (ಡೆಮೋ — AI ಪೈಪ್‌ಲೈನ್ ಇನ್ನೂ ಸಂಪರ್ಕಗೊಂಡಿಲ್ಲ)",
        "symptoms": ["ಎಲೆಗಳ ಮೇಲೆ ಬಿಳಿ ಪೌಡರ್ ರೀತಿಯ ಲೇಪ", "ಪ್ರಭಾವಿತ ಪ್ರದೇಶಗಳ ಸುತ್ತ ಹಳದಿ ಬಣ್ಣ", "ಹೊಸ ಬೆಳವಣಿಗೆ ಕುಂಠಿತ"],
        "treatment_recommendations": ["ಬೇವಿನ ಎಣ್ಣೆ ಅಥವಾ ಪೊಟ್ಯಾಸಿಯಂ ಬೈಕಾರ್ಬೋನೇಟ್ ಸಿಂಪಡಿಸಿ", "ತೀವ್ರ ಸೋಂಕಿತ ಎಲೆಗಳನ್ನು ತೆಗೆಯಿರಿ", "ಸಸ್ಯಗಳ ಸುತ್ತ ಗಾಳಿ ಸಂಚಾರ ಸುಧಾರಿಸಿ"],
        "preventive_measures": ["ಸಾರಜನಕದಿಂದ ಹೆಚ್ಚು ಗೊಬ್ಬರ ಹಾಕುವುದನ್ನು ತಪ್ಪಿಸಿ", "ಎಲೆಗಳ ಮೇಲಲ್ಲ, ಸಸ್ಯದ ತಳಭಾಗದಲ್ಲಿ ನೀರು ಕೊಡಿ", "ರೋಗ ನಿರೋಧಕ ತಳಿಗಳನ್ನು ನೆಡಿ"],
        "explanation": "ನಿಮ್ಮ ಲಕ್ಷಣ ವಿವರಣೆ ಸ್ವೀಕರಿಸಲಾಗಿದೆ. ಇದು ಡೆಮೋ ಫಲಿತಾಂಶ — LLM ಸಂಪರ್ಕಗೊಂಡ ನಂತರ ನಿಜವಾದ ರೋಗನಿರ್ಣಯ ಸಿಗುತ್ತದೆ.",
    },
    "ml": {
        "disease_name": "പൊടി പൂപ്പൽ രോഗം (ഡെമോ — AI പൈപ്പ്‌ലൈൻ ഇനിയും ബന്ധിപ്പിച്ചിട്ടില്ല)",
        "symptoms": ["ഇലകളിൽ വെളുത്ത പൊടി പോലുള്ള പൂശ്", "ബാധിത ഭാഗങ്ങൾക്ക് ചുറ്റും മഞ്ഞ നിറം", "പുതിയ വളർച്ച മുരടിക്കൽ"],
        "treatment_recommendations": ["വേപ്പ് എണ്ണ അല്ലെങ്കിൽ പൊട്ടാസ്യം ബൈകാർബണേറ്റ് സ്പ്രേ ചെയ്യുക", "കഠിനമായി ബാധിക്കപ്പെട്ട ഇലകൾ നീക്കം ചെയ്യുക", "ചെടികൾക്ക് ചുറ്റും വായുസഞ്ചാരം മെച്ചപ്പെടുത്തുക"],
        "preventive_measures": ["നൈട്രജൻ കൊണ്ട് അമിതമായ വളം ഒഴിവാക്കുക", "ഇലകളിലല്ല, ചെടിയുടെ ചുവട്ടിൽ വെള്ളം നൽകുക", "പ്രതിരോധ ശേഷിയുള്ള ഇനങ്ങൾ നടുക"],
        "explanation": "നിങ്ങളുടെ ലക്ഷണ വിവരണം ലഭിച്ചു. ഇത് ഒരു ഡെമോ ഫലമാണ് — LLM ബന്ധിപ്പിച്ചതിന് ശേഷം യഥാർത്ഥ രോഗനിർണ്ണയം ലഭിക്കും.",
    },
    "mr": {
        "disease_name": "भुरी रोग (डेमो — AI पाइपलाइन अद्याप जोडलेली नाही)",
        "symptoms": ["पानांवर पांढरी पावडरसारखी थर", "प्रभावित भागाभोवती पिवळसरपणा", "नवीन वाढ खुंटणे"],
        "treatment_recommendations": ["कडुनिंब तेल किंवा पोटेशियम बायकार्बोनेट फवारा", "जास्त बाधित पाने काढून टाका", "झाडांच्या आजूबाजूला हवा खेळती ठेवा"],
        "preventive_measures": ["नत्राने जास्त खत टाळा", "पानांवर नव्हे, झाडाच्या मुळाशी पाणी द्या", "प्रतिकारक वाण लावा"],
        "explanation": "तुमचे लक्षण वर्णन मिळाले. हा डेमो निकाल आहे — LLM जोडल्यानंतर खरे निदान मिळेल.",
    },
    "gu": {
        "disease_name": "ભૂકી છારો (ડેમો — AI પાઇપલાઇન હજુ જોડાઈ નથી)",
        "symptoms": ["પાંદડાઓ ઉપર સફેદ પાઉડર જેવો લેપ", "અસરગ્રસ્ત વિસ્તારોની આજુ-બાજુ પીળાશ", "નવી વૃદ્ધિ રૂંધાઈ"],
        "treatment_recommendations": ["લીમડાનું તેલ અથવા પોટેશિયમ બાયકાર્બોનેટ છાંટો", "ભારે સંક્રમિત પાંદડા કાઢો", "છોડ આજુ-બાજુ હવા ઉજાસ સુધારો"],
        "preventive_measures": ["નાઇટ્રોજનથી વધુ ખાતર ટાળો", "પાંદડા ઉપર નહીં, છોડના મૂળ પાસે પાણી આપો", "પ્રતિરોધક જાત વાવો"],
        "explanation": "તમારું લક્ષણ વર્ણન મળ્યું. આ ડેમો પરિણામ છે — LLM જોડાય ત્યારે સાચું નિદાન મળશે.",
    },
    "bn": {
        "disease_name": "গুঁড়ো ছত্রাক রোগ (ডেমো — AI পাইপলাইন এখনো সংযুক্ত হয়নি)",
        "symptoms": ["পাতায় সাদা পাউডারের মতো আবরণ", "আক্রান্ত জায়গার চারপাশে হলুদ হওয়া", "নতুন বৃদ্ধি থমকে যাওয়া"],
        "treatment_recommendations": ["নিম তেল বা পটাশিয়াম বাইকার্বোনেট স্প্রে করুন", "মারাত্মক আক্রান্ত পাতা সরিয়ে ফেলুন", "গাছের চারপাশে বায়ু চলাচল উন্নত করুন"],
        "preventive_measures": ["নাইট্রোজেন দিয়ে অতিরিক্ত সার এড়িয়ে চলুন", "পাতায় নয়, গাছের গোড়ায় পানি দিন", "রোগ-প্রতিরোধী জাত লাগান"],
        "explanation": "আপনার লক্ষণের বিবরণ পাওয়া গেছে। এটি একটি ডেমো ফলাফল — LLM সংযুক্ত হলে আসল রোগ নির্ণয় পাবেন।",
    },
}


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat()
    )

@app.post("/api/v1/diagnose")
async def diagnose(
    file: UploadFile = File(...),
    language: str = Form(default="en"),
    plant_type: Optional[str] = Form(default=None)
):
    """Upload image for disease diagnosis."""
    try:
        allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp", "image/gif"]
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail=f"Invalid image format: {file.content_type}. Allowed: jpeg, png, webp")

        logger.info(f"Diagnosis request - file: {file.filename}, language: {language}, plant_type: {plant_type}")

        diagnosis_id = str(uuid.uuid4())
        data = MOCK_IMAGE_DIAGNOSIS.get(language, MOCK_IMAGE_DIAGNOSIS["en"])

        return {
            "diagnosis_id": diagnosis_id,
            "disease_name": data["disease_name"],
            "confidence_score": 0.72,
            "severity_level": "medium",
            "symptoms": data["symptoms"],
            "treatment_recommendations": data["treatment_recommendations"],
            "preventive_measures": data["preventive_measures"],
            "farmer_friendly_explanation": data["explanation"],
            "audio_available": False,
            "language": language,
            "timestamp": datetime.now().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Diagnosis endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/diagnose/text")
async def diagnose_text(
    description: str,
    language: str = "en",
    plant_type: Optional[str] = None
):
    """Text-based diagnosis endpoint."""
    try:
        logger.info(f"Text diagnosis request: {description}")
        diagnosis_id = str(uuid.uuid4())
        data = MOCK_TEXT_DIAGNOSIS.get(language, MOCK_TEXT_DIAGNOSIS["en"])

        return {
            "diagnosis_id": diagnosis_id,
            "disease_name": data["disease_name"],
            "confidence_score": 0.65,
            "severity_level": "low",
            "symptoms": data["symptoms"],
            "treatment_recommendations": data["treatment_recommendations"],
            "preventive_measures": data["preventive_measures"],
            "farmer_friendly_explanation": data["explanation"],
            "audio_available": False,
            "language": language,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/diagnose/retranslate")
async def retranslate_diagnosis(diagnosis_type: str = "image", language: str = "en"):
    """Return translated mock diagnosis for the given type and language."""
    if diagnosis_type == "text":
        data = MOCK_TEXT_DIAGNOSIS.get(language, MOCK_TEXT_DIAGNOSIS["en"])
        confidence = 0.65
        severity = "low"
    else:
        data = MOCK_IMAGE_DIAGNOSIS.get(language, MOCK_IMAGE_DIAGNOSIS["en"])
        confidence = 0.72
        severity = "medium"

    return {
        "disease_name": data["disease_name"],
        "confidence_score": confidence,
        "severity_level": severity,
        "symptoms": data["symptoms"],
        "treatment_recommendations": data["treatment_recommendations"],
        "preventive_measures": data["preventive_measures"],
        "farmer_friendly_explanation": data["explanation"],
        "audio_available": False,
        "language": language,
    }


@app.get("/api/v1/languages")
async def get_supported_languages():
    """Get list of supported languages."""
    return {
        "languages": {
            "en": "English",
            "hi": "Hindi",
            "ta": "Tamil",
            "te": "Telugu",
            "ka": "Kannada",
            "ml": "Malayalam",
            "mr": "Marathi",
            "gu": "Gujarati",
            "bn": "Bengali"
        }
    }

@app.post("/api/v1/feedback")
async def submit_feedback(diagnosis_id: str, feedback: dict):
    """Submit feedback for diagnosis (RLHF)."""
    try:
        logger.info(f"Feedback received for diagnosis {diagnosis_id}")
        return {"status": "feedback_recorded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("startup")
async def startup_event():
    """Initialize models on startup."""
    logger.info("Starting Plant Disease Identifier API...")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down Plant Disease Identifier API...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
    )
