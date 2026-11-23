
import base64
import io
import json
import threading

import streamlit as st
from groq import Groq
from PIL import Image
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av


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

.stApp {
    background-color: #FCE4EC;
}

[data-testid="stHeader"] {
    background-color: #FCE4EC;
}

[data-testid="stSidebar"] {
    background-color: #F8BBD0;
}

h1, h2, h3 {
    color: #AD1457 !important;
}

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

.stChatInput {
    border-radius: 15px;
}

footer {
    visibility: hidden;
}

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

    <h3 style="letter-spacing:4px; color:#AD1457;">
        BEAUTY AI
    </h3>

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

if "skin_analysis_data" not in st.session_state:
    st.session_state.skin_analysis_data = None

if "chat_recommended_names" not in st.session_state:
    st.session_state.chat_recommended_names = []

if "last_analysis_signature" not in st.session_state:
    st.session_state.last_analysis_signature = ""

if "selected_photo_bytes" not in st.session_state:
    st.session_state.selected_photo_bytes = None

if "selected_photo_source" not in st.session_state:
    st.session_state.selected_photo_source = ""

if "camera_frame_buffer" not in st.session_state:
    st.session_state.camera_frame_buffer = {
        "frame": None
    }


# =========================================================
# 6. GROQ CLIENT
# =========================================================

try:

    client = Groq(
        api_key=st.secrets["GROQ_API_KEY"]
    )

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

    st.caption(
        "Set your preferences to personalize product matches."
    )

    skin_types = [
        "Oily",
        "Dry",
        "Combination",
        "Normal",
        "Sensitive",
        "Acne-prone"
    ]

    skin_tones = [
        "Fair",
        "Light",
        "Medium",
        "Wheatish",
        "Tan",
        "Deep",
        "Dark",
        "Not sure"
    ]

    budgets = [
        "Budget-friendly",
        "Mid-range",
        "Premium",
        "Any budget"
    ]

    with st.form("skin_profile_form"):

        selected_skin_type = st.selectbox(
            "Select your skin type",
            skin_types,
            index=skin_types.index(
                st.session_state.applied_profile["skin_type"]
            )
        )

        selected_skin_tone = st.selectbox(
            "Select your skin tone",
            skin_tones,
            index=skin_tones.index(
                st.session_state.applied_profile["skin_tone"]
            )
        )

        selected_concerns = st.multiselect(
            "Your skin concerns",
            [
                "Acne",
                "Blackheads",
                "Dark spots",
                "Oiliness",
                "Dryness",
                "Sensitivity",
                "Uneven skin tone",
                "Dullness",
                "Dehydration"
            ],
            default=st.session_state.applied_profile["concerns"]
        )

        selected_budget = st.selectbox(
            "Your budget",
            budgets,
            index=budgets.index(
                st.session_state.applied_profile["budget"]
            )
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

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.session_state.chat_recommended_names = []

        st.session_state.skin_analysis = ""

        st.session_state.skin_analysis_data = None

        st.session_state.last_analysis_signature = ""

        st.session_state.selected_photo_bytes = None

        st.session_state.selected_photo_source = ""

        st.rerun()


    st.markdown("---")

    st.markdown(
        "<div style='text-align:center;'><b>Kairaé Beauty AI 💗</b></div>",
        unsafe_allow_html=True
    )


# =========================================================
# 8. PRODUCT MATCHING
# =========================================================

def recommend_products(
    skin_type,
    selected_concerns,
    selected_budget
):

    matches = [
        p for p in PRODUCTS
        if skin_type in p["skin_types"]
    ]

    def score(product):

        concern_score = sum(
            1
            for concern in selected_concerns
            if concern in product["concerns"]
        )

        if selected_budget == "Budget-friendly":

            budget_score = (
                1 if product["price"] <= 1500 else 0
            )

        elif selected_budget == "Mid-range":

            budget_score = (
                1 if 1500 < product["price"] <= 4000 else 0
            )

        elif selected_budget == "Premium":

            budget_score = (
                1 if product["price"] > 4000 else 0
            )

        else:

            budget_score = 0

        return budget_score, concern_score

    return sorted(
        matches,
        key=score,
        reverse=True
    )


# =========================================================
# 9. PRODUCT DISPLAY FUNCTIONS
# =========================================================

def get_products_by_names(names):

    ordered = []

    for name in names:

        for product in PRODUCTS:

            if (
                product["name"] == name
                and product not in ordered
            ):

                ordered.append(product)

    return ordered


def display_products(products):

    if not products:

        st.info(
            "Our current product database has no exact match "
            "for this skin type yet."
        )

        return

    columns = st.columns(3)

    for index, product in enumerate(products):

        with columns[index % 3]:

            with st.container(border=True):

                st.image(
                    product["image"],
                    use_container_width=True
                )

                st.caption(product["brand"])

                st.subheader(product["name"])

                st.markdown(
                    f"### Rs. {product['price']:,}"
                )

                st.success(product["tier"])

                st.write(product["description"])

                st.write(
                    f"**Category:** {product['category']}"
                )

                st.write(
                    f"**Suitable for:** "
                    f"{', '.join(product['skin_types'])}"
                )

                st.caption(
                    "Product details and prices should be "
                    "confirmed with the seller."
                )

                st.link_button(
                    "🛍️ Shop Now",
                    product["url"],
                    use_container_width=True
                )


# =========================================================
# 10. CAMERA FUNCTION
# =========================================================

def camera_callback(frame):

    image = frame.to_ndarray(format="rgb24")

    pil_image = Image.fromarray(image)

    buffer = io.BytesIO()

    pil_image.save(
        buffer,
        format="JPEG",
        quality=85
    )

    # Store the latest camera frame
    st.session_state.camera_frame_buffer["frame"] = (
        buffer.getvalue()
    )

    return av.VideoFrame.from_ndarray(
        image,
        format="rgb24"
    )


# =========================================================
# 11. MAIN TABS
# =========================================================

home_tab, analysis_tab, assistant_tab = st.tabs(
    [
        "🏠 Home & Matches",
        "📸 AI Skin Analysis",
        "💬 Skin Assistant"
    ]
)


# =========================================================
# 12. HOME TAB
# =========================================================

with home_tab:

    st.markdown("## 💗 Welcome to Kairaé!")

    st.write(
        "Understand your skin, explore a simple skincare routine, "
        "and discover products that match your preferences."
    )

    chat_products = get_products_by_names(
        st.session_state.chat_recommended_names
    )

    if chat_products:

        st.markdown(
            "## ✨ Products Recommended by Your AI Assistant"
        )

        st.caption(
            "These are the same database products mentioned "
            "in the latest product recommendation from your chatbot."
        )

        display_products(chat_products)

        st.divider()


    st.markdown("## 🌷 Recommended Products")

    st.caption(
        f"Matches for {skin_type} skin, your concerns and your selected budget."
    )

    profile_products = recommend_products(
        skin_type,
        concerns,
        budget
    )

    display_products(profile_products)


    if skin_type in ["Dry", "Sensitive"]:

        st.info(
            "Our current database has limited products for this skin type. "
            "At present, Simple Refreshing Facial Wash is the only listed "
            "product tagged for both Dry and Sensitive skin."
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
        "This is general skincare education, not a personalized "
        "medical prescription. Introduce new products gradually "
        "and patch test first."
    )


# =========================================================
# 13. AI SKIN ANALYSIS TAB
# =========================================================

with analysis_tab:

    st.markdown("## 📸 AI Skin Analysis")

    st.write(
        "Capture a photo using your camera or upload a picture. "
        "Kairaé will automatically review visible skin features "
        "and provide preliminary skincare insights."
    )


    st.warning(
        "Privacy notice: Your photo is sent to Groq's AI model "
        "for analysis. Do not upload a photo if you are uncomfortable "
        "sharing it with this service. This is not a medical diagnosis."
    )


    # -----------------------------------------------------
    # SELECT PHOTO METHOD
    # -----------------------------------------------------

    photo_method = st.radio(
        "Choose your photo method",
        [
            "📷 Use Camera",
            "🖼️ Upload Photo"
        ],
        horizontal=True,
        key="photo_method"
    )


    # -----------------------------------------------------
    # CAMERA MODE
    # -----------------------------------------------------

    if photo_method == "📷 Use Camera":

        st.markdown("### 📷 Your Camera")

        st.caption(
            "Press Start to turn on your camera. "
            "Press Stop to turn it off."
        )

        camera_context = webrtc_streamer(
            key="kairae_camera",
            mode=WebRtcMode.SENDRECV,
            video_frame_callback=camera_callback,
            media_stream_constraints={
                "video": True,
                "audio": False
            },
            async_processing=True
        )


        if camera_context.state.playing:

            st.success("Camera is ON 🟢")

        else:

            st.info("Camera is OFF 🔴")


        if st.button(
            "📸 Capture Photo",
            use_container_width=True
        ):

            latest_frame = (
                st.session_state.camera_frame_buffer["frame"]
            )

            if latest_frame is not None:

                st.session_state.selected_photo_bytes = (
                    latest_frame
                )

                st.session_state.selected_photo_source = (
                    "Camera"
                )

                st.success(
                    "Photo captured successfully! 💗"
                )

                st.rerun()

            else:

                st.warning(
                    "Please turn on your camera first "
                    "and wait for the video to appear."
                )


    # -----------------------------------------------------
    # UPLOAD MODE
    # -----------------------------------------------------

    elif photo_method == "🖼️ Upload Photo":

        st.markdown("### 🖼️ Upload Your Photo")

        uploaded_photo = st.file_uploader(
            "Choose a clear face photo",
            type=[
                "jpg",
                "jpeg",
                "png",
                "webp"
            ],
            key="kairae_uploaded_photo",
            help=(
                "Upload a clear, unfiltered picture "
                "with natural lighting."
            )
        )


        if uploaded_photo is not None:

            try:

                image_bytes = uploaded_photo.getvalue()

                # Verify that the file is a valid image
                image = Image.open(
                    io.BytesIO(image_bytes)
                )

                image.verify()

                st.session_state.selected_photo_bytes = (
                    image_bytes
                )

                st.session_state.selected_photo_source = (
                    "Upload"
                )

                st.success(
                    "Image uploaded successfully! 💗"
                )

            except Exception as error:

                st.error(
                    "This image could not be opened. "
                    "Please upload a valid JPG, PNG or WEBP image."
                )


    # -----------------------------------------------------
    # PHOTO PREVIEW
    # -----------------------------------------------------

    if st.session_state.selected_photo_bytes is not None:

        st.divider()

        st.markdown("## 💗 Photo Preview")

        try:

            preview_image = Image.open(
                io.BytesIO(
                    st.session_state.selected_photo_bytes
                )
            )

            st.image(
                preview_image,
                caption="Your selected photo",
                width=350
            )

        except Exception:

            st.error(
                "The selected image could not be displayed."
            )


        st.success(
            "Your photo is ready. Confirm it below to start AI analysis."
        )


        # -------------------------------------------------
        # CONFIRM PHOTO & ANALYZE
        # -------------------------------------------------

        if st.button(
            "✨ Confirm Photo & Analyze My Skin",
            use_container_width=True,
            type="primary"
        ):

            try:

                image_bytes = (
                    st.session_state.selected_photo_bytes
                )

                image = Image.open(
                    io.BytesIO(image_bytes)
                ).convert("RGB")


                # Resize image to reduce API payload
                image.thumbnail(
                    (1024, 1024)
                )


                # Convert image to JPEG
                image_buffer = io.BytesIO()

                image.save(
                    image_buffer,
                    format="JPEG",
                    quality=85
                )

                processed_image_bytes = (
                    image_buffer.getvalue()
                )


                encoded_image = base64.b64encode(
                    processed_image_bytes
                ).decode("utf-8")


                data_url = (
                    "data:image/jpeg;base64,"
                    + encoded_image
                )


                analysis_prompt = """
You are Kairaé, an AI skincare education assistant.

Analyze the provided face photo carefully.

You must NOT diagnose any medical condition.
You must NOT claim dermatologist-grade accuracy.
You must NOT infer age, ethnicity, identity, health status,
or any sensitive personal attribute.

Respond ONLY with valid JSON using this exact structure:

{
    "possible_skin_type": "Oily / Dry / Combination / Normal / Sensitive / Cannot determine",
    "confidence": "Low / Moderate",
    "visible_observations": [
        "Observation 1",
        "Observation 2"
    ],
    "possible_concerns": [
        "Concern 1",
        "Concern 2"
    ],
    "limitations": [
        "Limitation 1",
        "Limitation 2"
    ],
    "skincare_guidance": [
        "Guidance 1",
        "Guidance 2",
        "Guidance 3"
    ],
    "when_to_see_dermatologist": "Advice",
    "summary": "A short friendly summary."
}

IMPORTANT RULES:

1. Possible skin type is only a tentative estimate.
2. A photograph cannot reliably determine skin type.
3. Choose Cannot determine if the photo does not provide
   enough evidence.
4. Do not confidently classify skin type based only on
   lighting, shine, makeup or image quality.
5. Describe only features that are actually visible.
6. Visible shine does not automatically mean oily skin.
7. Visible dryness does not automatically confirm dry skin.
8. Possible concerns must be non-diagnostic observations.
9. Do not diagnose acne, rosacea, eczema, infection,
   pigmentation disorders or other medical conditions.
10. Give gentle, general skincare guidance.
11. Mention that skin type should also be confirmed through
    the user's own experience.
12. Use kind, clear and understandable language.
13. If image quality is poor, mention it.
14. Do not invent observations.
15. Do not include Markdown code fences around the JSON.
"""


                with st.spinner(
                    "Kairaé is analyzing your photo... 🌸"
                ):

                    vision_response = (
                        client.chat.completions.create(
                            model="qwen/qwen3.8-27b",
                            messages=[
                                {
                                    "role": "user",
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": analysis_prompt
                                        },
                                        {
                                            "type": "image_url",
                                            "image_url": {
                                                "url": data_url
                                            }
                                        }
                                    ]
                                }
                            ],
                            temperature=0.2,
                            max_completion_tokens=1500
                        )
                    )


                result = (
                    vision_response
                    .choices[0]
                    .message.content
                )


                # Parse AI JSON response
                try:

                    cleaned_result = result.strip()

                    if cleaned_result.startswith("```"):

                        cleaned_result = (
                            cleaned_result
                            .replace("```json", "")
                            .replace("```", "")
                            .strip()
                        )

                    analysis_data = json.loads(
                        cleaned_result
                    )

                    st.session_state.skin_analysis_data = (
                        analysis_data
                    )

                    st.session_state.skin_analysis = (
                        analysis_data
                    )

                except Exception:

                    # If AI doesn't return valid JSON
                    st.session_state.skin_analysis_data = None

                    st.session_state.skin_analysis = result


                st.session_state.last_analysis_signature = (
                    str(hash(processed_image_bytes))
                )

                st.success(
                    "Your skin analysis is ready! 💗"
                )

                st.rerun()


            except Exception as error:

                st.error(
                    "Image analysis could not be completed. "
                    "Please check your internet connection, "
                    "Groq API key and vision model availability."
                )

                st.code(
                    str(error)
                )


    # =====================================================
    # 14. DISPLAY ANALYSIS RESULTS
    # =====================================================

    if st.session_state.skin_analysis:

        st.divider()

        st.markdown("## 🌸 Your Skin Insights")


        analysis_data = (
            st.session_state.skin_analysis_data
        )


        # -------------------------------------------------
        # STRUCTURED ANALYSIS
        # -------------------------------------------------

        if isinstance(analysis_data, dict):


            possible_skin_type = (
                analysis_data.get(
                    "possible_skin_type",
                    "Cannot determine"
                )
            )

            confidence = (
                analysis_data.get(
                    "confidence",
                    "Low"
                )
            )


            st.markdown("### 💗 Possible Skin Type")


            st.info(
                f"**AI Suggestion:** {possible_skin_type}"
            )


            st.caption(
                f"Confidence level: {confidence}. "
                "This is only a tentative photo-based estimate."
            )


            st.markdown("### 🔍 Visible Observations")

            for observation in analysis_data.get(
                "visible_observations",
                []
            ):

                st.write(
                    f"• {observation}"
                )


            st.markdown("### 🌷 Possible Concerns")

            possible_concerns = (
                analysis_data.get(
                    "possible_concerns",
                    []
                )
            )

            if possible_concerns:

                for concern in possible_concerns:

                    st.write(
                        f"• {concern}"
                    )

            else:

                st.write(
                    "No clear concerns could be identified."
                )


            st.markdown("### ⚠️ Limitations")

            for limitation in analysis_data.get(
                "limitations",
                []
            ):

                st.write(
                    f"• {limitation}"
                )


            st.markdown("### 🧴 General Skincare Guidance")

            for guidance in analysis_data.get(
                "skincare_guidance",
                []
            ):

                st.write(
                    f"• {guidance}"
                )


            st.markdown(
                "### 👩‍⚕️ When to Consult a Dermatologist"
            )

            st.write(
                analysis_data.get(
                    "when_to_see_dermatologist",
                    "Consult a dermatologist for persistent or concerning skin issues."
                )
            )


            st.markdown("### 💬 Summary")

            st.write(
                analysis_data.get(
                    "summary",
                    ""
                )
            )


            # -------------------------------------------------
            # APPLY AI SUGGESTED SKIN TYPE
            # -------------------------------------------------

            st.divider()

            st.markdown(
                "## 💗 Personalize Your Skin Profile"
            )

            st.write(
                "Would you like to use the AI's tentative "
                "skin type suggestion for your product matches?"
            )


            valid_skin_types = [
                "Oily",
                "Dry",
                "Combination",
                "Normal",
                "Sensitive",
                "Acne-prone"
            ]


            if possible_skin_type in valid_skin_types:

                suggested_profile_type = (
                    possible_skin_type
                )

            else:

                suggested_profile_type = (
                    st.session_state.applied_profile["skin_type"]
                )


            selected_analysis_skin_type = st.selectbox(
                "Confirm or change your skin type",
                valid_skin_types,
                index=valid_skin_types.index(
                    suggested_profile_type
                ),
                key="analysis_confirm_skin_type"
            )


            if st.button(
                "💗 Confirm Skin Type & Update My Products",
                use_container_width=True
            ):

                st.session_state.applied_profile[
                    "skin_type"
                ] = selected_analysis_skin_type


                st.session_state.chat_recommended_names = []


                st.success(
                    f"Your profile is now updated to "
                    f"{selected_analysis_skin_type} skin! 💗"
                )


                st.info(
                    "Your product recommendations will now "
                    "match your updated skin profile."
                )


                st.rerun()


        # -------------------------------------------------
        # FALLBACK IF JSON PARSING FAILED
        # -------------------------------------------------

        else:

            st.markdown(
                st.session_state.skin_analysis
            )

            st.warning(
                "The AI response could not be formatted "
                "automatically. You can still read the analysis "
                "above, but the skin profile suggestion "
                "could not be extracted."
            )


        # -------------------------------------------------
        # SAFETY MESSAGE
        # -------------------------------------------------

        st.info(
            "This analysis is based on one photograph and is "
            "not a clinical assessment. Lighting, camera quality, "
            "makeup, filters and angle can affect the results. "
            "A photo cannot reliably confirm skin type or diagnose "
            "skin conditions. For persistent, painful, rapidly "
            "changing or concerning symptoms, consult a qualified dermatologist."
        )


# =========================================================
# 15. SKIN ASSISTANT TAB
# =========================================================

with assistant_tab:

    st.markdown(
        "## 💬 Your Personal Skin Assistant"
    )

    st.write(
        "Ask about skincare routines, ingredients, cosmetics, "
        "product comparisons and affordable options in Pakistan."
    )


    if st.session_state.skin_analysis:

        with st.expander(
            "View your latest AI skin insights"
        ):

            if isinstance(
                st.session_state.skin_analysis,
                dict
            ):

                st.json(
                    st.session_state.skin_analysis
                )

            else:

                st.markdown(
                    st.session_state.skin_analysis
                )


    # =====================================================
    # SYSTEM PROMPT
    # =====================================================

    SYSTEM_PROMPT = f"""

You are Kairaé, a friendly AI skincare, beauty and cosmetics assistant.

USER PROFILE:

Skin type: {skin_type}

Skin tone: {skin_tone}

Skin concerns: {concerns}

Budget: {budget}

Interested in makeup: {makeup_interest}


LATEST PHOTO-BASED SKIN INSIGHTS:

{st.session_state.skin_analysis or "No photo analysis has been completed."}


PRODUCT DATABASE:

{PRODUCTS}


RULES:

1. Reply in the language used by the user: English, Urdu, or Roman Urdu.

2. Be friendly, clear, practical and easy to understand.

3. Recommend products according to the user's stated profile and concerns.

4. Use only exact product names, brands, prices and links from the database.

5. Never invent a product, price, ingredient, claim, or shopping URL.

6. Prices are approximate and can change.

7. When recommending products, mention exact database product names.

8. For product recommendations, use a table with:
   Product Name | Brand | Approximate Price (PKR) | Why it may suit the user.

9. Only recommend products whose skin_types list includes
   the user's selected skin type.

10. If the database has no suitable item, say so honestly.

11. For Dry and Sensitive skin, the current database has
    limited coverage.

12. Do not say a cheap product is low quality only because of its price.

13. Do not claim products cure acne or any skin disease.

14. Do not diagnose medical conditions from a photo or text.

15. Photo insights are uncertain visible observations,
    not clinical findings.

16. Do not claim dermatologist-grade accuracy.

17. For severe, painful, persistent, rapidly changing or
    worrying symptoms, recommend a qualified dermatologist.

18. Encourage patch testing and introducing one new product
    at a time.

19. For routines, separate morning and night steps and
    include sunscreen in the morning routine.

20. Avoid recommending many active ingredients at once.

21. Skin tone may help with makeup shade suggestions,
    not skincare diagnosis.

22. If asked about a product not in the database,
    say it is not currently listed.

23. Keep the response focused on skincare, makeup and beauty.

24. If a skin analysis has been performed, use it as context
    but remember that it is only a tentative photo-based observation.

"""


    # =====================================================
    # CHAT HISTORY
    # =====================================================

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    user_input = st.chat_input(
        "Ask Kairaé about skincare, products, or makeup... 💗",
        key="beauty_chat_input"
    )


    if user_input:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )


        try:

            with st.spinner(
                "Kairaé is thinking... 🌸"
            ):

                response = client.chat.completions.create(

                    model="openai/gpt-oss-120b",

                    messages=[
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT
                        },

                        *st.session_state.messages
                    ],

                    temperature=0.5,

                    max_tokens=1200

                )


            answer = (
                response
                .choices[0]
                .message.content
                or "Sorry, I could not prepare an answer."
            )


            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )


            # Detect exact product names
            mentioned_names = [

                product["name"]

                for product in PRODUCTS

                if product["name"].casefold()
                in answer.casefold()

            ]


            if mentioned_names:

                st.session_state.chat_recommended_names = (
                    mentioned_names
                )


            st.rerun()


        except Exception as error:

            st.error(
                f"Something went wrong: {error}"
            )


# =========================================================
# 16. FOOTER
# =========================================================

st.markdown("---")

st.html("""
<div style="text-align:center; padding:15px;">

    <h3 style="color:#AD1457;">
        ✨ Kairaé Beauty AI ✨
    </h3>

    <p style="color:#AD1457;">
        Your beauty. Your confidence. Your glow. 💗
    </p>

    <p style="font-size:13px; color:#880E4F;">
        AI-powered skincare insights and cosmetics assistant
    </p>

</div>
""")
