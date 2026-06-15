# =========================================================
# Multilingual Sample Reviews — Hindi, English, Hinglish
# 10-15 reviews per demo product for semantic search
# =========================================================

SAMPLE_REVIEWS = {

    # ── P001: Noise ColorFit Pro 4 Smartwatch ──────────────
    "P001": [
        {"id": 1, "user": "Rahul K.",    "rating": 5, "lang": "en",
         "text": "Amazing smartwatch for the price. The AMOLED display is super bright and battery easily lasts 5-6 days with normal use. Bluetooth calling works perfectly."},
        {"id": 2, "user": "Priya S.",    "rating": 4, "lang": "hi",
         "text": "बहुत अच्छी स्मार्टवॉच है। बैटरी लाइफ 7 दिन तक चलती है। डिस्प्ले बहुत शार्प है। बस स्ट्रैप थोड़ी सस्ती क्वालिटी की है।"},
        {"id": 3, "user": "Arjun M.",    "rating": 5, "lang": "hinglish",
         "text": "battery life kaafi achhi hai bhai, 5-6 din aaram se chalti hai. display bhi bright hai. calling feature bhi theek kaam karta hai."},
        {"id": 4, "user": "Sneha T.",    "rating": 3, "lang": "en",
         "text": "Display is good but the heart rate sensor is not accurate. It shows different readings compared to my oximeter. SpO2 is also hit or miss."},
        {"id": 5, "user": "Vikram S.",   "rating": 4, "lang": "hi",
         "text": "डिस्प्ले बहुत अच्छा है AMOLED का। 100 से ज़्यादा स्पोर्ट्स मोड हैं। हार्ट रेट सेंसर ठीक-ठाक है, बहुत accurate नहीं है।"},
        {"id": 6, "user": "Meena R.",    "rating": 5, "lang": "hinglish",
         "text": "waterproof hai kya? haan bhai IP68 rating hai, maine haath dhoye bhi toh koi issue nahi aaya. swimming mein use nahi kiya though."},
        {"id": 7, "user": "Karthik D.",  "rating": 2, "lang": "en",
         "text": "The strap broke after 2 months of daily use. Build quality is not great for daily wear. Display is good though."},
        {"id": 8, "user": "Ananya P.",   "rating": 4, "lang": "hi",
         "text": "नोटिफिकेशन अच्छे आते हैं फोन से। कॉलिंग फीचर भी काम करता है। बस स्पीकर की आवाज़ थोड़ी कम है।"},
        {"id": 9, "user": "Rohan J.",    "rating": 5, "lang": "en",
         "text": "Best smartwatch under 3500. The always-on display feature is great. Sleep tracking is fairly accurate. Charging takes about 2 hours."},
        {"id": 10, "user": "Deepika N.", "rating": 3, "lang": "hinglish",
         "text": "watch acchi hai lekin app thoda slow hai. bluetooth disconnect hota hai baar baar agar phone dur ho toh. display top class hai."},
        {"id": 11, "user": "Amit G.",    "rating": 4, "lang": "hi",
         "text": "GPS नहीं है इसमें लेकिन connected GPS से काम चल जाता है। रनिंग ट्रैकिंग के लिए ठीक है। कीमत के हिसाब से बहुत अच्छा है।"},
        {"id": 12, "user": "Neha L.",    "rating": 5, "lang": "en",
         "text": "Charging is fast, about 1.5 to 2 hours for full charge. The magnetic charger is convenient. Battery lasts me about 5 days easily."},
    ],

    # ── P002: boAt Rockerz 450 Headphones ──────────────────
    "P002": [
        {"id": 1, "user": "Arjun P.",    "rating": 4, "lang": "en",
         "text": "Great headphones for the price. Bass is punchy and the battery easily lasts 15 hours. Foldable design is a plus for travel."},
        {"id": 2, "user": "Sneha T.",    "rating": 5, "lang": "hi",
         "text": "बहुत बढ़िया हेडफोन है! आवाज़ की क्वालिटी जबरदस्त है। कीमत के हिसाब से बहुत अच्छा है। 15 घंटे बैटरी चलती है।"},
        {"id": 3, "user": "Vikram S.",   "rating": 2, "lang": "en",
         "text": "Returned it. Ear cushions are not comfortable for long use beyond 2 hours. The headband presses too tight. Sound quality is fine though."},
        {"id": 4, "user": "Meena R.",    "rating": 4, "lang": "hinglish",
         "text": "sound quality bahut acchi hai. bass bhi achha hai. lekin thoda tight feel hota hai pehle 2-3 din. uske baad theek ho jata hai."},
        {"id": 5, "user": "Rohan D.",    "rating": 5, "lang": "en",
         "text": "Best budget wireless headphones I have owned. Foldable design is a big plus. Mic quality for calls is decent too."},
        {"id": 6, "user": "Priya M.",    "rating": 3, "lang": "hi",
         "text": "साउंड अच्छा है लेकिन माइक की क्वालिटी average है। कॉल पर दूसरी तरफ आवाज़ हल्की जाती है। म्यूज़िक सुनने के लिए बढ़िया है।"},
        {"id": 7, "user": "Karthik R.",  "rating": 4, "lang": "hinglish",
         "text": "bluetooth range achhi hai, 10 meter tak aaram se kaam karta hai. latency gaming mein thodi hai but music ke liye perfect."},
        {"id": 8, "user": "Ananya S.",   "rating": 5, "lang": "en",
         "text": "I use these for gym daily. They stay on during workouts. Sweat resistant and easy to clean. Totally worth the price."},
        {"id": 9, "user": "Rahul T.",    "rating": 3, "lang": "hi",
         "text": "बिल्ड क्वालिटी ठीक है, प्लास्टिक बॉडी है। 6 महीने बाद हिंज ढीला हो गया। साउंड अभी भी अच्छा है।"},
        {"id": 10, "user": "Deepak N.",  "rating": 4, "lang": "en",
         "text": "Noise cancellation is not there but passive isolation is decent. For the price range, you cannot expect ANC. Sound is clear and bass is good."},
    ],

    # ── P003: Philips Avent Baby Monitor ───────────────────
    "P003": [
        {"id": 1, "user": "Priya S.",    "rating": 5, "lang": "en",
         "text": "Excellent baby monitor! Sound quality is crystal clear and the range is impressive. My baby is in the next room and I can hear every sound."},
        {"id": 2, "user": "Rahul K.",    "rating": 4, "lang": "hi",
         "text": "बहुत अच्छा प्रोडक्ट है। बच्चे की आवाज़ बिल्कुल साफ आती है। बैटरी भी लंबे समय तक चलती है। रेंज 200 मीटर तक ठीक है।"},
        {"id": 3, "user": "Ananya M.",   "rating": 5, "lang": "en",
         "text": "Worth every penny. The temperature sensor is a great feature. Setup was super easy, took 5 minutes. Night light is soothing."},
        {"id": 4, "user": "Karthik R.",  "rating": 3, "lang": "hinglish",
         "text": "range thodi kam lagti hai mujhe. 2 kamre dur jaane par signal weak ho jata hai. baaki sab theek hai, sound clear hai."},
        {"id": 5, "user": "Deepika N.",  "rating": 5, "lang": "en",
         "text": "Amazing product! The nightlight feature is also very useful. Battery life is about 18 hours. Highly recommend for new parents."},
        {"id": 6, "user": "Vikram P.",   "rating": 4, "lang": "hi",
         "text": "टेम्परेचर सेंसर बहुत useful है। कमरे का तापमान दिखाता है। बच्चे के लिए safe environment बनाने में मदद करता है।"},
        {"id": 7, "user": "Sneha K.",    "rating": 5, "lang": "hinglish",
         "text": "baby monitor bahut achha hai. DECT technology hai toh interference nahi aata. sound crystal clear hai dono taraf se."},
        {"id": 8, "user": "Amit S.",     "rating": 4, "lang": "en",
         "text": "Good monitor but a camera version would have been better. Audio-only is fine for newborns but once they start crawling you want video."},
        {"id": 9, "user": "Neha R.",     "rating": 5, "lang": "hi",
         "text": "नाइट लाइट बहुत अच्छी है। बच्चा आराम से सो जाता है। रात को feeding के समय भी help करती है। बैटरी 18 घंटे चलती है।"},
        {"id": 10, "user": "Rohan M.",   "rating": 3, "lang": "en",
         "text": "Decent product but feels overpriced for audio-only. The lullaby feature is nice though. Build quality is solid Philips standard."},
    ],
}


def get_reviews(product_id: str) -> list[dict]:
    """Get all reviews for a product."""
    return SAMPLE_REVIEWS.get(product_id, [])


def get_all_review_texts() -> list[tuple[str, str, dict]]:
    """Return (product_id, review_text, review_obj) for all reviews — used for embedding index."""
    results = []
    for pid, reviews in SAMPLE_REVIEWS.items():
        for r in reviews:
            results.append((pid, r["text"], r))
    return results
