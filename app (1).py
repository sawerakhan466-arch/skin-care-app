import base64
import streamlit as st
from groq import Groq

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Kairaé Beauty AI",
    page_icon="💗",
    layout="wide"
)

# =========================================================
# 2. CUSTOM CSS
# =========================================================

st.markdown("""
<style>
.stApp { background-color: #FCE4EC; }
[data-testid="stHeader"] { background-color: #FCE4EC; }
[data-testid="stSidebar"] { background-color: #F8BBD0; }
h1, h2, h3 { color: #AD1457 !important; }
div[data-testid="stChatMessage"] {
    background-color: #FFF5F8;
    border: 1px solid #F3B6CC;
    border-radius: 15px;
}
.stButton > button {
    background-color: #C2185B;
    color: white;
    border-radius: 10px;
    border: none;
}
.stButton > button:hover {
    background-color: #880E4F;
    color: white;
}
.stChatInput { border-radius: 15px; }
footer { visibility: hidden; }
div[data-testid="stMetric"] {
    background: #FFF5F8;
    border: 1px solid #F3B6CC;
    padding: 12px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. HEADER
# =========================================================

st.html("""
<div style="text-align:center; padding: 8px 0 2px;">
    <h1 style="font-family:serif; font-size:50px; color:#AD1457;">
        ✨ Kairaé ✨
    </h1>
    <h3 style="letter-spacing:4px; color:#AD1457;">BEAUTY AI</h3>
    <p style="color:#AD1457; font-size:18px;">
        Your Personal Beauty & Skincare Assistant
    </p>
    <p style="color:#880E4F;">
        Understand your skin. Discover your glow. Shop with confidence. 💗
    </p>
</div>
""")
st.divider()

# =========================================================
# 4. PRODUCT DATABASE
# NOTE: Prices and links are the values in the existing app.
# Verify them with the seller before publishing.
# =========================================================

PRODUCTS = [
    {
        "name": "Dermive Oil-Free Moisturizer",
        "brand": "Jenpharm",
        "price": 1098,
        "category": "Moisturizer",
        "tier": "Budget-friendly",
        "skin_types": ["Oily", "Combination", "Acne-prone"],
        "concerns": ["Oiliness", "Acne", "Dehydration"],
        "description": "Lightweight moisturizer for daily hydration.",
        "quality": "Good everyday skincare option",
        "image": "https://jenpharm.com/cdn/shop/files/Dermivewash_jpg.jpg?v=1778314684",
        "url": "https://jenpharm.com/products/dermive-oil-free"
    },
    {
        "name": "Acne Control Cleanser",
        "brand": "Derma London",
        "price": 1080,
        "category": "Cleanser",
        "tier": "Budget-friendly",
        "skin_types": ["Oily", "Combination", "Acne-prone"],
        "concerns": ["Acne", "Blackheads", "Oiliness"],
        "description": "Cleanser designed for acne-prone skin.",
        "quality": "Targeted skincare option",
        "image": "https://dermalondon.com.pk/cdn/shop/files/1.jpg?v=1711016939",
        "url": "https://dermalondon.com.pk/products/acne-control-cleanser-150ml"
    },
    {
        "name": "Acne Control Serum",
        "brand": "Derma London",
        "price": 1240,
        "category": "Serum",
        "tier": "Budget-friendly",
        "skin_types": ["Oily", "Combination", "Acne-prone"],
        "concerns": ["Acne", "Blackheads", "Oiliness"],
        "description": "Serum for blemish-prone skin.",
        "quality": "Active-ingredient-focused option",
        "image": "https://dermalondon.com.pk/cdn/shop/files/1_dbf13df1-bd7f-433b-aa78-f3e775b1ad60.jpg?v=1777375582",
        "url": "https://dermalondon.com.pk/collections/acne-pimples"
    },
    {
        "name": "Acne & Oil Control Moisturizer",
        "brand": "Derma London",
        "price": 1190,
        "category": "Moisturizer",
        "tier": "Budget-friendly",
        "skin_types": ["Oily", "Combination", "Acne-prone"],
        "concerns": ["Acne", "Oiliness"],
        "description": "Moisturizer designed for oily and acne-prone skin.",
        "quality": "Targeted skincare option",
        "image": "https://dermalondon.com.pk/cdn/shop/files/1_dbf13df1-bd7f-433b-aa78-f3e775b1ad60.jpg?v=1777375582",
        "url": "https://dermalondon.com.pk/collections/acne-pimples"
    },
    {
        "name": "Simple Refreshing Facial Wash",
        "brand": "Simple",
        "price": 1630,
        "category": "Cleanser",
        "tier": "Mid-range",
        "skin_types": ["Oily", "Combination", "Sensitive", "Normal", "Dry"],
        "concerns": ["Sensitivity", "Oiliness", "Dryness"],
        "description": "Gentle daily facial cleanser.",
        "quality": "Gentle everyday option",
        "image": "https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?auto=format&fit=crop&w=600&q=80",
        "url": "https://www.cozmetics.pk/concerns/oily-acne-prone-skin"
    },
    {
        "name": "Purifying Neem Face Wash",
        "brand": "Himalaya",
        "price": 680,
        "category": "Cleanser",
        "tier": "Budget-friendly",
        "skin_types": ["Oily", "Combination"],
        "concerns": ["Oiliness", "Acne"],
        "description": "Affordable neem-based facial cleanser.",
        "quality": "Basic budget cleanser",
        "image": "https://himalayausa.com/cdn/shop/files/4_714ece8d-0028-483d-9a6e-e50b7f5e1656.png?v=1770222739&width=1800",
        "url": "https://www.cozmetics.pk/concerns/oily-acne-prone-skin"
    },
    {
        "name": "Super Light Gel Moisturizer",
        "brand": "Pond's",
        "price": 1430,
        "category": "Moisturizer",
        "tier": "Budget-friendly",
        "skin_types": ["Oily", "Combination", "Normal"],
        "concerns": ["Oiliness", "Dehydration"],
        "description": "Lightweight gel moisturizer.",
        "quality": "Lightweight daily hydration",
        "image": "https://highfy.pk/cdn/shop/files/3_345886c6-d158-4bb4-bdc8-68da4a03da1f.webp?v=1784715502&width=1200",
        "url": "https://www.cozmetics.pk/concerns/oily-acne-prone-skin"
    },
    {
        "name": "Niacinamide 10% + Zinc 1%",
        "brand": "The Ordinary",
        "price": 2699,
        "category": "Serum",
        "tier": "Mid-range",
        "skin_types": ["Oily", "Combination"],
        "concerns": ["Oiliness", "Acne marks"],
        "description": "Niacinamide serum for oiliness and the appearance of blemishes.",
        "quality": "Concentrated active formula",
        "image": "https://adminbeauty.hvnet.vn/Upload/Files/the-ordinary-niacinamide-10-zinc-1-30ml.jpg",
        "url": "https://www.cozmetics.pk/concerns/oily-acne-prone-skin"
    },
    {
        "name": "Acne Control Kit",
        "brand": "Derma London",
        "price": 3370,
        "category": "Skincare Kit",
        "tier": "Mid-range",
        "skin_types": ["Oily", "Combination", "Acne-prone"],
        "concerns": ["Acne", "Blackheads", "Oiliness"],
        "description": "A skincare kit for acne-prone skin.",
        "quality": "Multi-product skincare routine",
        "image": "https://dermalondon.com.pk/cdn/shop/files/1_dbf13df1-bd7f-433b-aa78-f3e775b1ad60.jpg?v=1777375582",
        "url": "https://dermalondon.com.pk/collections/acne-pimples"
    }
]

# =========================================================
# 5. SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "applied_profile" not in st.session_state:
    st.session_state.applied_profile = {
        "skin_type": "Oily",
        "skin_tone": "Not sure",
        "concerns": [],
        "budget": "Any budget",
        "makeup_interest": False
    }

if "skin_analysis" not in st.session_state:
    st.session_state.skin_analysis = ""

if "chat_recommended_names" not in st.session_state:
    st.session_state.chat_recommended_names = []

if "last_analysis_signature" not in st.session_state:
    st.session_state.last_analysis_signature = ""

# =========================================================
# 6. GROQ CLIENT
# =========================================================

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error(
        "Groq API key is missing. Add GROQ_API_KEY to "
        ".streamlit/secrets.toml before running the app."
    )
    st.stop()

# =========================================================
# 7. SIDEBAR - USER PROFILE
# =========================================================

with st.sidebar:
    st.markdown("## 🌸 Your Skin Profile")
    st.caption("Set your preferences to personalize product matches.")

    skin_types = [
        "Oily", "Dry", "Combination", "Normal", "Sensitive", "Acne-prone"
    ]
    skin_tones = [
        "Fair", "Light", "Medium", "Wheatish",
        "Tan", "Deep", "Dark", "Not sure"
    ]
    budgets = ["Budget-friendly", "Mid-range", "Premium", "Any budget"]

    with st.form("skin_profile_form"):
        selected_skin_type = st.selectbox(
            "Select your skin type",
            skin_types,
            index=skin_types.index(st.session_state.applied_profile["skin_type"])
        )
        selected_skin_tone = st.selectbox(
            "Select your skin tone",
            skin_tones,
            index=skin_tones.index(st.session_state.applied_profile["skin_tone"])
        )
        selected_concerns = st.multiselect(
            "Your skin concerns",
            [
                "Acne", "Blackheads", "Dark spots", "Oiliness", "Dryness",
                "Sensitivity", "Uneven skin tone", "Dullness", "Dehydration"
            ],
            default=st.session_state.applied_profile["concerns"]
        )
        selected_budget = st.selectbox(
            "Your budget",
            budgets,
            index=budgets.index(st.session_state.applied_profile["budget"])
        )
        selected_makeup_interest = st.checkbox(
            "Show makeup recommendations",
            value=st.session_state.applied_profile["makeup_interest"]
        )
        apply_preferences = st.form_submit_button(
            "✅ Apply My Preferences",
            use_container_width=True
        )

    if apply_preferences:
        st.session_state.applied_profile = {
            "skin_type": selected_skin_type,
            "skin_tone": selected_skin_tone,
            "concerns": selected_concerns,
            "budget": selected_budget,
            "makeup_interest": selected_makeup_interest
        }
        st.session_state.chat_recommended_names = []
        st.success("Your preferences have been applied!")
        st.rerun()

    skin_type = st.session_state.applied_profile["skin_type"]
    skin_tone = st.session_state.applied_profile["skin_tone"]
    concerns = st.session_state.applied_profile["concerns"]
    budget = st.session_state.applied_profile["budget"]
    makeup_interest = st.session_state.applied_profile["makeup_interest"]

    st.divider()
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_recommended_names = []
        st.session_state.skin_analysis = ""
        st.session_state.last_analysis_signature = ""
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center;'><b>Kairaé Beauty AI 💗</b></div>",
        unsafe_allow_html=True
    )

# =========================================================
# 8. PRODUCT MATCHING
# =========================================================

def recommend_products(skin_type, selected_concerns, selected_budget):
    """Return skin-type matches; budget affects ranking, not exclusion."""
    matches = [
        p for p in PRODUCTS
        if skin_type in p["skin_types"]
    ]

    def score(product):
        concern_score = sum(
            1 for concern in selected_concerns
            if concern in product["concerns"]
        )

        if selected_budget == "Budget-friendly":
            budget_score = 1 if product["price"] <= 1500 else 0
        elif selected_budget == "Mid-range":
            budget_score = 1 if 1500 < product["price"] <= 4000 else 0
        elif selected_budget == "Premium":
            budget_score = 1 if product["price"] > 4000 else 0
        else:
            budget_score = 0

        return (budget_score, concern_score)

    return sorted(matches, key=score, reverse=True)


def get_products_by_names(names):
    """Keep the displayed cards synchronized with exact database names."""
    ordered = []
    for name in names:
        for product in PRODUCTS:
            if product["name"] == name and product not in ordered:
                ordered.append(product)
    return ordered


def display_products(products):
    if not products:
        st.info(
            "Our current verified product list has no exact match for this "
            "skin type yet. We are not going to suggest an unrelated product."
        )
        return

    columns = st.columns(3)
    for index, product in enumerate(products):
        with columns[index % 3]:
            with st.container(border=True):
                st.image(product["image"], use_container_width=True)
                st.caption(product["brand"])
                st.subheader(product["name"])
                st.markdown(f"### Rs. {product['price']:,}")
                st.success(product["tier"])
                st.write(product["description"])
                st.write(f"**Category:** {product['category']}")
                st.write(f"**Suitable for:** {', '.join(product['skin_types'])}")
                st.caption(
                    "Product details and prices should be confirmed with the seller."
                )
                st.link_button(
                    "🛍️ Shop Now",
                    product["url"],
                    use_container_width=True
                )

# =========================================================
# 9. MAIN TABS
# =========================================================

home_tab, analysis_tab, assistant_tab = st.tabs(
    ["🏠 Home & Matches", "📸 AI Skin Analysis", "💬 Skin Assistant"]
)

with home_tab:
    st.markdown("## 💗 Welcome to Kairaé!")
    st.write(
        "Understand your skin, explore a simple skincare routine, "
        "and discover products that match your preferences."
    )

    # If the latest chatbot answer named products from our database,
    # show those exact products here. Otherwise use profile matches.
    chat_products = get_products_by_names(
        st.session_state.chat_recommended_names
    )

    if chat_products:
        st.markdown("## ✨ Products Recommended by Your AI Assistant")
        st.caption(
            "These are the same database products mentioned in the latest "
            "product recommendation from your chatbot."
        )
        display_products(chat_products)
        st.divider()

    st.markdown("## 🌷 Recommended Products")
    st.caption(
        f"Matches for {skin_type} skin, your concerns and your selected budget. "
        "Budget is used to prioritize products, not to hide skin-type matches."
    )

    profile_products = recommend_products(skin_type, concerns, budget)
    display_products(profile_products)

    if skin_type in ["Dry", "Sensitive"]:
        st.info(
            "Our current database has limited products for this skin type. "
            "At present, Simple Refreshing Facial Wash is the only listed "
            "product tagged for both Dry and Sensitive skin. More verified "
            "products should be added before expanding these recommendations."
        )

    st.divider()
    st.markdown("## 🌞 A Simple Skincare Routine")
    morning_col, night_col = st.columns(2)
    with morning_col:
        st.markdown("### ☀️ Morning")
        st.write("1. Gentle cleanser")
        st.write("2. Moisturizer suitable for your skin")
        st.write("3. Broad-spectrum SPF 30+ sunscreen")
    with night_col:
        st.markdown("### 🌙 Night")
        st.write("1. Gentle cleanser")
        st.write("2. One suitable treatment, if needed")
        st.write("3. Moisturizer")
    st.caption(
        "This is general skincare education, not a personalized medical prescription. "
        "Introduce new products gradually and patch test first."
    )

with analysis_tab:
    st.markdown("## 📸 AI Skin Analysis")
    st.write(
        "Take a clear photo or upload a selfie in natural, even lighting. "
        "The AI will describe visible features and provide general skincare guidance."
    )

    st.warning(
        "Privacy & safety: Your photo is sent to Groq's vision model for analysis. "
        "Do not upload a photo if you are uncomfortable sharing it with this service. "
        "The analysis is not a diagnosis and cannot confirm a skin condition."
    )

    photo_method = st.radio(
        "Choose how to add your photo",
        ["Take a photo with camera", "Upload a photo"],
        horizontal=True
    )

    photo = None
    if photo_method == "Take a photo with camera":
        photo = st.camera_input(
            "Take a front-facing photo",
            help="Use natural light, remove heavy filters, and keep your face clearly visible."
        )
    else:
        photo = st.file_uploader(
            "Upload a clear face photo",
            type=["jpg", "jpeg", "png"],
            help="Use a clear, unfiltered photo with even lighting."
        )

    if photo is not None:
        st.image(photo, caption="Your selected photo", width=320)

        if st.button("✨ Analyze My Skin", use_container_width=True):
            try:
                image_bytes = photo.getvalue()
                encoded_image = base64.b64encode(image_bytes).decode("utf-8")
                mime_type = photo.type or "image/jpeg"
                data_url = f"data:{mime_type};base64,{encoded_image}"

                analysis_prompt = """
You are an AI skincare education assistant. Review this face photo only
for visible, non-diagnostic observations. Do not identify the person.
Do not infer age, ethnicity, health status, or any sensitive attribute.

Explain cautiously:
1. Visible features that may be present (for example, visible blemishes,
   shine, redness, dark spots, or texture), only if clearly visible.
2. What cannot be reliably assessed from this photo.
3. Gentle general skincare steps that may be helpful.
4. Ingredients/categories the user could discuss with a qualified
   dermatologist or pharmacist, without prescribing treatment.
5. When professional medical advice is appropriate.

Do not diagnose acne, rosacea, eczema, infection, pigmentation disorders,
or any other medical condition. Do not assign a skin type from the photo.
Do not claim dermatologist-grade accuracy. If image quality, lighting,
makeup, filters, or angle limit assessment, say so.
Use clear, kind language and headings. Avoid certainty.
"""

                with st.spinner("Kairaé is reviewing the visible features... 🌸"):
                    vision_response = client.chat.completions.create(
                        model="qwen/qwen3.8-27b",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": analysis_prompt},
                                    {
                                        "type": "image_url",
                                        "image_url": {"url": data_url}
                                    }
                                ]
                            }
                        ],
                        temperature=0.3,
                        max_completion_tokens=1200
                    )

                result = vision_response.choices[0].message.content
                st.session_state.skin_analysis = result
                st.session_state.last_analysis_signature = str(hash(image_bytes))
                st.success("Your skin insights are ready!")
                st.rerun()

            except Exception as error:
                st.error(
                    "The image analysis could not be completed. "
                    "Check that your Groq account has access to the vision model "
                    f"and try again. Technical detail: {error}"
                )

    if st.session_state.skin_analysis:
        st.divider()
        st.markdown("## 🌸 Your Skin Insights")
        st.markdown(st.session_state.skin_analysis)
        st.info(
            "This is an AI-generated observation of one photo, not a clinical "
            "assessment. Lighting, camera quality, makeup and filters can affect "
            "the result. For persistent, painful, rapidly changing or worrying "
            "skin concerns, consult a qualified dermatologist."
        )
        st.markdown("### 💗 Continue to your product matches")
        st.write(
            "Your photo analysis does not automatically determine your skin type. "
            "Use the Skin Profile in the sidebar to confirm your skin type and "
            "concerns; your product matches will update accordingly."
        )

with assistant_tab:
    st.markdown("## 💬 Your Personal Skin Assistant")
    st.write(
        "Ask about skincare routines, ingredients, cosmetics, product comparisons "
        "and affordable options in Pakistan."
    )

    if st.session_state.skin_analysis:
        with st.expander("View your latest AI skin insights"):
            st.markdown(st.session_state.skin_analysis)

    # =====================================================
    # 10. SYSTEM PROMPT
    # =====================================================

    SYSTEM_PROMPT = f"""
You are Kairaé, a friendly AI skincare, beauty and cosmetics assistant.

USER PROFILE:
Skin type: {skin_type}
Skin tone: {skin_tone}
Skin concerns: {concerns}
Budget: {budget}
Interested in makeup: {makeup_interest}

LATEST PHOTO-BASED SKIN INSIGHTS (non-diagnostic):
{st.session_state.skin_analysis or "No photo analysis has been completed."}

PRODUCT DATABASE:
{PRODUCTS}

RULES:
1. Reply in the language used by the user: English, Urdu, or Roman Urdu.
2. Be friendly, clear, practical and easy to understand.
3. Recommend products according to the user's stated profile and concerns.
4. Use only exact product names, brands, prices and links from the database.
5. Never invent a product, price, ingredient, claim, or shopping URL.
6. Prices are approximate and can change; ask users to confirm with the seller.
7. When recommending products, mention exact database product names so the
   app can display the same products in the Recommended Products section.
8. For product recommendations, use a table with:
   Product Name | Brand | Approximate Price (PKR) | Why it may suit the user.
9. Only recommend products whose skin_types list includes the user's selected
   skin type. If the database has no suitable item, say so honestly.
10. Do not recommend unrelated products merely to fill a list.
11. For Dry and Sensitive skin, the current database has limited coverage.
    Simple Refreshing Facial Wash is the only current entry tagged for both.
12. Do not say a cheap product is low quality only because of its price.
13. Do not claim products cure acne or any skin disease.
14. Do not diagnose medical conditions from a photo or text.
15. Photo insights are uncertain visible observations, not clinical findings.
16. Do not claim dermatologist-grade accuracy or that a photo proves a skin type.
17. For severe, painful, persistent, rapidly changing or worrying symptoms,
    recommend a qualified dermatologist.
18. Encourage patch testing and introducing one new product at a time.
19. For routines, separate morning and night steps and include sunscreen in
    the morning routine.
20. Avoid recommending many active ingredients at once.
21. Skin tone may help with makeup shade suggestions, not skincare diagnosis.
22. If asked about a product not in the database, say it is not currently listed.
23. Keep the response focused on skincare, makeup and beauty.
"""

    # =====================================================
    # 11. CHAT HISTORY
    # =====================================================

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input(
        "Ask Kairaé about skincare, products, or makeup... 💗",
        key="beauty_chat_input"
    )

    if user_input:
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        try:
            with st.spinner("Kairaé is thinking... 🌸"):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        *st.session_state.messages
                    ],
                    temperature=0.5,
                    max_tokens=1200
                )

            answer = response.choices[0].message.content or (
                "Sorry, I could not prepare an answer. Please try again."
            )
            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

            # Detect exact product names in the latest answer.
            mentioned_names = [
                product["name"]
                for product in PRODUCTS
                if product["name"].casefold() in answer.casefold()
            ]

            if mentioned_names:
                st.session_state.chat_recommended_names = mentioned_names

            st.rerun()

        except Exception as error:
            st.error(f"Something went wrong: {error}")

# =========================================================
# 12. FOOTER
# =========================================================

st.markdown("---")
st.html("""
<div style="text-align:center; padding:15px;">
    <h3 style="color:#AD1457;">✨ Kairaé Beauty AI ✨</h3>
    <p style="color:#AD1457;">
        Your beauty. Your confidence. Your glow. 💗
    </p>
    <p style="font-size:13px; color:#880E4F;">
        AI-powered skincare insights and cosmetics assistant
    </p>
</div>
""")
