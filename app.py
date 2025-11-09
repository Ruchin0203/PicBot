# """
# AI Image Generator - Complete Application in One File
# Uses LangChain, Flask, and Hugging Face API
# """

# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# from langchain_huggingface import HuggingFaceEndpoint
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# # from langchain.schema.runnable import RunnablePassthrough
# from dotenv import load_dotenv
# import os
# import requests
# import base64
# import random
# from io import BytesIO
# from PIL import Image as PILImage

# # Load environment variables
# load_dotenv()

# # Initialize Flask app
# app = Flask(__name__, static_folder='static')
# CORS(app)

# # Configuration
# HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
# IMAGE_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
# TEXT_MODEL = "microsoft/DialoGPT-medium"
# API_URL_IMAGE = f"https://api-inference.huggingface.co/models/{IMAGE_MODEL}"
# API_URL_TEXT = f"https://api-inference.huggingface.co/models/{TEXT_MODEL}"

# # Alternative: Use huggingface_hub library for better compatibility
# from huggingface_hub import InferenceClient

# # Initialize Inference Client
# inference_client = InferenceClient(token=HUGGINGFACE_API_KEY)

# # Initialize LangChain components
# try:
#     llm = HuggingFaceEndpoint(
#         repo_id=TEXT_MODEL,
#         huggingfacehub_api_token=HUGGINGFACE_API_KEY,
#         task="text-generation",
#         max_new_tokens=100,
#         temperature=0.7
#     )

#     # Prompt template for enhancing user input
#     enhance_prompt = PromptTemplate(
#         template="""Enhance this image description to be more detailed and artistic: {user_prompt}
        
# Enhanced description:""",
#         input_variables=["user_prompt"]
#     )

#     # Output parser
#     parser = StrOutputParser()

#     # Create enhancement chain
#     enhancement_chain = enhance_prompt | llm | parser
    
#     print("✓ LangChain initialized successfully")
# except Exception as e:
#     print(f"⚠ LangChain initialization warning: {e}")
#     enhancement_chain = None

# # Prompt suggestions database
# PROMPT_SUGGESTIONS = [
#     "A futuristic cyberpunk city at sunset with neon lights",
#     "Magical forest with glowing mushrooms and fireflies",
#     "Ancient temple in the mountains with mystical fog",
#     "Steampunk airship floating through cloudy skies",
#     "Underwater palace with bioluminescent sea creatures",
#     "Desert oasis with palm trees under starry night sky",
#     "Fantasy castle on floating island in the clouds",
#     "Cozy library with magical books and candles",
#     "Alien landscape with multiple moons and strange flora",
#     "Victorian street in autumn with gas lamps",
#     "Dragon perched on mountain peak breathing fire",
#     "Enchanted garden with crystal flowers at twilight",
#     "Space station orbiting a colorful nebula",
#     "Medieval marketplace bustling with fantasy creatures",
#     "Northern lights over a frozen lake with aurora",
#     "Mystical portal between dimensions in deep forest",
#     "Robot city with flying vehicles and holographic displays",
#     "Pirate ship sailing through storm clouds",
#     "Cherry blossom garden with traditional Japanese bridge",
#     "Wizard tower filled with potions and spell books"
# ]

# def generate_image_hf(prompt):
#     """Generate image using Hugging Face Inference Client"""
#     try:
#         # Use the new InferenceClient API
#         image = inference_client.text_to_image(
#             prompt=prompt,
#             model=IMAGE_MODEL
#         )
        
#         # Convert PIL Image to base64
#         buffered = BytesIO()
#         image.save(buffered, format="JPEG")
#         image_bytes = buffered.getvalue()
#         base64_image = base64.b64encode(image_bytes).decode('utf-8')
        
#         return f"data:image/jpeg;base64,{base64_image}", None, False
        
#     except Exception as e:
#         error_msg = str(e)
        
#         # Check if model is loading
#         if "loading" in error_msg.lower() or "503" in error_msg:
#             return None, "Model is loading. Please try again in 20 seconds.", True
        
#         return None, f"Error generating image: {error_msg}", False

# def enhance_prompt_langchain(prompt):
#     """Enhance prompt using LangChain"""
#     if enhancement_chain is None:
#         return prompt
    
#     try:
#         enhanced = enhancement_chain.invoke({"user_prompt": prompt})
#         return enhanced.strip() if enhanced else prompt
#     except Exception as e:
#         print(f"Enhancement error: {e}")
#         return prompt

# # API Routes
# @app.route('/')
# def index():
#     """Serve the main HTML page"""
#     return send_from_directory('static', 'index.html')

# @app.route('/api/generate-image', methods=['POST'])
# def generate_image():
#     """Generate image from prompt"""
#     data = request.get_json()
#     prompt = data.get('prompt', '')
    
#     if not prompt:
#         return jsonify({"error": "Prompt is required"}), 400
    
#     image_data, error, retry = generate_image_hf(prompt)
    
#     if error:
#         return jsonify({"error": error, "retry": retry}), 503 if retry else 500
    
#     return jsonify({
#         "image": image_data,
#         "prompt": prompt
#     })

# @app.route('/api/enhance-prompt', methods=['POST'])
# def enhance_prompt_api():
#     """Enhance prompt using LangChain"""
#     data = request.get_json()
#     prompt = data.get('prompt', '')
    
#     if not prompt:
#         return jsonify({"error": "Prompt is required"}), 400
    
#     enhanced = enhance_prompt_langchain(prompt)
#     return jsonify({"enhanced": enhanced})

# @app.route('/api/suggestions', methods=['GET'])
# def get_suggestions():
#     """Get shuffled prompt suggestions"""
#     shuffled = random.sample(PROMPT_SUGGESTIONS, min(6, len(PROMPT_SUGGESTIONS)))
#     return jsonify({"suggestions": shuffled})

# @app.route('/api/health', methods=['GET'])
# def health_check():
#     """Health check endpoint"""
#     return jsonify({
#         "status": "OK",
#         "message": "Server is running",
#         "api_key_configured": bool(HUGGINGFACE_API_KEY),
#         "langchain_available": enhancement_chain is not None
#     })

# # HTML Template
# HTML_TEMPLATE = """<!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>AI Image Generator</title>
#     <script src="https://cdn.tailwindcss.com"></script>
#     <style>
#         @keyframes pulse-slow {
#             0%, 100% { opacity: 0.1; }
#             50% { opacity: 0.2; }
#         }
#         .animate-pulse-slow {
#             animation: pulse-slow 3s ease-in-out infinite;
#         }
#         .glass {
#             background: rgba(255, 255, 255, 0.1);
#             backdrop-filter: blur(10px);
#             border: 1px solid rgba(255, 255, 255, 0.2);
#         }
#     </style>
# </head>
# <body class="bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 min-h-screen">
#     <!-- Animated Background -->
#     <div class="fixed inset-0 overflow-hidden pointer-events-none">
#         <div class="absolute w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse-slow -top-48 -left-48"></div>
#         <div class="absolute w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse-slow -bottom-48 -right-48" style="animation-delay: 1s;"></div>
#         <div class="absolute w-96 h-96 bg-pink-500/10 rounded-full blur-3xl animate-pulse-slow top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" style="animation-delay: 2s;"></div>
#     </div>

#     <div class="relative z-10 container mx-auto px-4 py-8 max-w-7xl">
#         <!-- Header -->
#         <div class="text-center mb-12">
#             <h1 class="text-5xl font-bold text-white mb-4">✨ AI Image Generator</h1>
#             <p class="text-blue-200 text-lg">Transform your imagination into stunning visuals</p>
#         </div>

#         <!-- Main Content -->
#         <div class="grid lg:grid-cols-2 gap-8 mb-8">
#             <!-- Left Panel -->
#             <div class="space-y-6">
#                 <!-- Prompt Input -->
#                 <div class="glass rounded-2xl p-6 shadow-2xl hover:shadow-purple-500/20 transition-all duration-300">
#                     <label class="block text-white text-lg font-semibold mb-3">🪄 Your Prompt</label>
#                     <textarea id="promptInput" placeholder="Describe the image you want to create..." class="w-full px-4 py-3 bg-white/20 border border-white/30 rounded-xl text-white placeholder-blue-200 focus:outline-none focus:ring-2 focus:ring-purple-500 resize-none" rows="4"></textarea>
#                     <div class="flex gap-3 mt-4">
#                         <button onclick="generateImage()" id="generateBtn" class="flex-1 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-300 transform hover:scale-105">
#                             🎨 Generate Image
#                         </button>
#                         <button onclick="refreshSuggestions()" class="bg-white/20 hover:bg-white/30 text-white p-3 rounded-xl transition-all duration-300">
#                             🔄
#                         </button>
#                     </div>
#                 </div>

#                 <!-- Error/Status Message -->
#                 <div id="statusMessage" class="hidden glass rounded-xl p-4"></div>

#                 <!-- Trending Suggestions -->
#                 <div class="glass rounded-2xl p-6 shadow-2xl">
#                     <h3 class="text-white text-lg font-semibold mb-4">✨ Trending Prompts</h3>
#                     <div id="suggestions" class="grid grid-cols-1 gap-2"></div>
#                 </div>
#             </div>

#             <!-- Right Panel -->
#             <div class="space-y-6">
#                 <div class="glass rounded-2xl p-6 shadow-2xl">
#                     <div class="flex items-center justify-between mb-4">
#                         <h3 class="text-white text-lg font-semibold">Generated Image</h3>
#                         <button onclick="downloadImage()" id="downloadBtn" class="hidden bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-all">
#                             📥 Download
#                         </button>
#                     </div>
#                     <div id="imageContainer" class="aspect-square bg-white/5 rounded-xl flex items-center justify-center border-2 border-dashed border-white/20">
#                         <div class="text-center p-8">
#                             <div class="text-6xl mb-4">🖼️</div>
#                             <p class="text-blue-200">Your generated image will appear here</p>
#                         </div>
#                     </div>
#                 </div>
#             </div>
#         </div>

#         <!-- History -->
#         <div id="historySection" class="hidden glass rounded-2xl p-6 shadow-2xl">
#             <h3 class="text-white text-lg font-semibold mb-4">📜 Recent Generations</h3>
#             <div id="historyGrid" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4"></div>
#         </div>
#     </div>

#     <script>
#         let history = [];
#         let currentImage = null;

#         async function generateImage() {
#             const prompt = document.getElementById('promptInput').value.trim();
#             if (!prompt) {
#                 showStatus('Please enter a prompt', 'error');
#                 return;
#             }

#             const btn = document.getElementById('generateBtn');
#             btn.disabled = true;
#             btn.innerHTML = '⏳ Generating...';
            
#             showStatus('Creating your masterpiece...', 'info');
#             document.getElementById('imageContainer').innerHTML = '<div class="text-center"><div class="text-6xl animate-spin">⚙️</div><p class="text-blue-200 mt-4">Generating image...</p></div>';

#             try {
#                 const response = await fetch('/api/generate-image', {
#                     method: 'POST',
#                     headers: { 'Content-Type': 'application/json' },
#                     body: JSON.stringify({ prompt })
#                 });

#                 const data = await response.json();

#                 if (data.error) {
#                     showStatus(data.error, 'error');
#                     if (data.retry) {
#                         setTimeout(() => generateImage(), 20000);
#                     }
#                     document.getElementById('imageContainer').innerHTML = '<div class="text-center p-8"><div class="text-6xl mb-4">⚠️</div><p class="text-red-200">Generation failed. Please try again.</p></div>';
#                 } else {
#                     currentImage = data.image;
#                     document.getElementById('imageContainer').innerHTML = `<img src="${data.image}" alt="Generated" class="w-full h-full object-cover rounded-xl">`;
#                     document.getElementById('downloadBtn').classList.remove('hidden');
#                     showStatus('Image generated successfully!', 'success');
                    
#                     history.unshift({ prompt, image: data.image });
#                     if (history.length > 6) history.pop();
#                     updateHistory();
#                 }
#             } catch (error) {
#                 showStatus('Failed to generate image. Please try again.', 'error');
#                 document.getElementById('imageContainer').innerHTML = '<div class="text-center p-8"><div class="text-6xl mb-4">❌</div><p class="text-red-200">Connection error</p></div>';
#             } finally {
#                 btn.disabled = false;
#                 btn.innerHTML = '🎨 Generate Image';
#             }
#         }

#         function showStatus(message, type) {
#             const status = document.getElementById('statusMessage');
#             status.classList.remove('hidden', 'bg-red-500/20', 'bg-green-500/20', 'bg-blue-500/20');
#             status.classList.add(type === 'error' ? 'bg-red-500/20' : type === 'success' ? 'bg-green-500/20' : 'bg-blue-500/20');
#             status.textContent = message;
#             status.classList.add('border', type === 'error' ? 'border-red-500/50' : type === 'success' ? 'border-green-500/50' : 'border-blue-500/50', 'text-white');
#         }

#         async function refreshSuggestions() {
#             try {
#                 const response = await fetch('/api/suggestions');
#                 const data = await response.json();
#                 const container = document.getElementById('suggestions');
#                 container.innerHTML = data.suggestions.map(s => 
#                     `<button onclick="useSuggestion('${s.replace(/'/g, "\\'")}')" class="text-left px-4 py-2 bg-white/10 hover:bg-white/20 text-blue-100 rounded-lg transition-all duration-300 text-sm border border-white/10 hover:border-purple-400/50 transform hover:scale-105">${s}</button>`
#                 ).join('');
#             } catch (error) {
#                 console.error('Failed to fetch suggestions:', error);
#             }
#         }

#         function useSuggestion(suggestion) {
#             document.getElementById('promptInput').value = suggestion;
#         }

#         function downloadImage() {
#             if (!currentImage) return;
#             const link = document.createElement('a');
#             link.href = currentImage;
#             link.download = `generated-${Date.now()}.jpg`;
#             link.click();
#         }

#         function updateHistory() {
#             if (history.length === 0) return;
#             document.getElementById('historySection').classList.remove('hidden');
#             const grid = document.getElementById('historyGrid');
#             grid.innerHTML = history.map((item, i) => 
#                 `<div class="aspect-square bg-white/5 rounded-lg overflow-hidden border border-white/20 hover:border-purple-400 transition-all duration-300 transform hover:scale-105 cursor-pointer" onclick="viewHistoryImage(${i})" title="${item.prompt}">
#                     <img src="${item.image}" alt="${item.prompt}" class="w-full h-full object-cover">
#                 </div>`
#             ).join('');
#         }

#         function viewHistoryImage(index) {
#             currentImage = history[index].image;
#             document.getElementById('imageContainer').innerHTML = `<img src="${currentImage}" alt="Generated" class="w-full h-full object-cover rounded-xl">`;
#             document.getElementById('downloadBtn').classList.remove('hidden');
#         }

#         // Initialize
#         refreshSuggestions();
#     </script>
# </body>
# </html>"""

# # Create static directory and save HTML
# os.makedirs('static', exist_ok=True)
# with open('static/index.html', 'w', encoding='utf-8') as f:
#     f.write(HTML_TEMPLATE)

# if __name__ == '__main__':
#     print("\n" + "="*60)
#     print("🚀 AI Image Generator - Starting Server")
#     print("="*60)
#     print(f"✓ Flask initialized")
#     print(f"✓ API Key configured: {bool(HUGGINGFACE_API_KEY)}")
#     print(f"✓ LangChain status: {'Active' if enhancement_chain else 'Fallback mode'}")
#     print(f"✓ Image Model: {IMAGE_MODEL}")
#     print(f"✓ Text Model: {TEXT_MODEL}")
#     print("\n📝 Access the app at: http://localhost:5000")
#     print("="*60 + "\n")
    

"""
AI Image Generator - Complete Application in One File
Uses LangChain, Flask, and Hugging Face API
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
# from langchain.schema.runnable import RunnablePassthrough
from dotenv import load_dotenv
import os
import requests
import base64
import random
import time
from io import BytesIO
from PIL import Image as PILImage


# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='static')
CORS(app)

# Configuration
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
IMAGE_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
TEXT_MODEL = "microsoft/DialoGPT-medium"
API_URL_IMAGE = f"https://api-inference.huggingface.co/models/{IMAGE_MODEL}"
API_URL_TEXT = f"https://api-inference.huggingface.co/models/{TEXT_MODEL}"

# Alternative: Use huggingface_hub library for better compatibility
from huggingface_hub import InferenceClient

# Initialize Inference Client
inference_client = InferenceClient(token=HUGGINGFACE_API_KEY)

# Initialize LangChain components
try:
    llm = HuggingFaceEndpoint(
        repo_id=TEXT_MODEL,
        huggingfacehub_api_token=HUGGINGFACE_API_KEY,
        task="text-generation",
        max_new_tokens=100,
        temperature=0.7
    )

    # Prompt template for enhancing user input
    enhance_prompt = PromptTemplate(
        template="""Enhance this image description to be more detailed and artistic: {user_prompt}
        
Enhanced description:""",
        input_variables=["user_prompt"]
    )

    # Output parser
    parser = StrOutputParser()

    # Create enhancement chain
    enhancement_chain = enhance_prompt | llm | parser
    
    print("✓ LangChain initialized successfully")
except Exception as e:
    print(f"⚠ LangChain initialization warning: {e}")
    enhancement_chain = None

# Prompt suggestions database
PROMPT_SUGGESTIONS = [
    "A futuristic cyberpunk city at sunset with neon lights",
    "Magical forest with glowing mushrooms and fireflies",
    "Ancient temple in the mountains with mystical fog",
    "Steampunk airship floating through cloudy skies",
    "Underwater palace with bioluminescent sea creatures",
    "Desert oasis with palm trees under starry night sky",
    "Fantasy castle on floating island in the clouds",
    "Cozy library with magical books and candles",
    "Alien landscape with multiple moons and strange flora",
    "Victorian street in autumn with gas lamps",
    "Dragon perched on mountain peak breathing fire",
    "Enchanted garden with crystal flowers at twilight",
    "Space station orbiting a colorful nebula",
    "Medieval marketplace bustling with fantasy creatures",
    "Northern lights over a frozen lake with aurora",
    "Mystical portal between dimensions in deep forest",
    "Robot city with flying vehicles and holographic displays",
    "Pirate ship sailing through storm clouds",
    "Cherry blossom garden with traditional Japanese bridge",
    "Wizard tower filled with potions and spell books"
]

def generate_image_hf(prompt):
    """Generate image using Pollinations AI - completely free, no API key needed"""
    try:
        # Using Pollinations.ai - Free API without rate limits
        # No authentication needed!
        import urllib.parse
        
        # URL encode the prompt
        encoded_prompt = urllib.parse.quote(prompt)
        
        # Pollinations API endpoint - completely free
        api_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        
        # Add parameters for better quality
        params = {
            "width": 1024,
            "height": 1024,
            "nologo": "true",
            "model": "flux"  # Using FLUX model via Pollinations
        }
        
        param_string = "&".join([f"{k}={v}" for k, v in params.items()])
        full_url = f"{api_url}?{param_string}"
        
        print(f"Generating image from: {full_url}")
        
        # Make request
        response = requests.get(full_url, timeout=120)
        
        if response.status_code == 200:
            # Convert to base64
            image_bytes = response.content
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            print(f"✓ Successfully generated image")
            return f"data:image/png;base64,{base64_image}", None, False
        else:
            raise Exception(f"API returned status code {response.status_code}")
            
    except Exception as e:
        error_msg = str(e)
        print(f"Pollinations error: {error_msg}")
        
        # Try alternative free API - DeepAI
        try:
            print("Trying alternative API...")
            deepai_url = "https://api.deepai.org/api/text2img"
            
            response = requests.post(
                deepai_url,
                data={'text': prompt},
                headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'},  # Free quickstart key
                timeout=120
            )
            
            if response.status_code == 200:
                data = response.json()
                image_url = data.get('output_url')
                
                # Download the image
                img_response = requests.get(image_url, timeout=60)
                image_bytes = img_response.content
                base64_image = base64.b64encode(image_bytes).decode('utf-8')
                print(f"✓ Successfully generated with DeepAI")
                return f"data:image/png;base64,{base64_image}", None, False
                
        except Exception as deepai_error:
            print(f"DeepAI error: {deepai_error}")
        
        return None, "Unable to generate image. Please try again in a moment.", False

def enhance_prompt_langchain(prompt):
    """Enhance prompt using LangChain"""
    if enhancement_chain is None:
        return prompt
    
    try:
        enhanced = enhancement_chain.invoke({"user_prompt": prompt})
        return enhanced.strip() if enhanced else prompt
    except Exception as e:
        print(f"Enhancement error: {e}")
        return prompt

# API Routes
@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('static', 'index.html')

@app.route('/api/generate-image', methods=['POST'])
def generate_image():
    """Generate image from prompt"""
    data = request.get_json()
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    image_data, error, retry = generate_image_hf(prompt)
    
    if error:
        return jsonify({"error": error, "retry": retry}), 503 if retry else 500
    
    return jsonify({
        "image": image_data,
        "prompt": prompt
    })

@app.route('/api/enhance-prompt', methods=['POST'])
def enhance_prompt_api():
    """Enhance prompt using LangChain"""
    data = request.get_json()
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    enhanced = enhance_prompt_langchain(prompt)
    return jsonify({"enhanced": enhanced})

@app.route('/api/suggestions', methods=['GET'])
def get_suggestions():
    """Get shuffled prompt suggestions"""
    shuffled = random.sample(PROMPT_SUGGESTIONS, min(6, len(PROMPT_SUGGESTIONS)))
    return jsonify({"suggestions": shuffled})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "OK",
        "message": "Server is running",
        "api_key_configured": bool(HUGGINGFACE_API_KEY),
        "langchain_available": enhancement_chain is not None
    })

# HTML Template
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PicBot - Dream It. Create It. Own It.</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @keyframes pulse-slow {
            0%, 100% { opacity: 0.15; transform: scale(1) rotate(0deg); }
            50% { opacity: 0.25; transform: scale(1.1) rotate(5deg); }
        }
        @keyframes float {
            0%, 100% { transform: translateY(0px) translateX(0px); }
            25% { transform: translateY(-30px) translateX(10px); }
            50% { transform: translateY(-20px) translateX(-10px); }
            75% { transform: translateY(-40px) translateX(5px); }
        }
        @keyframes shimmer {
            0% { background-position: -1000px 0; }
            100% { background-position: 1000px 0; }
        }
        @keyframes glow {
            0%, 100% { box-shadow: 0 0 20px rgba(147, 51, 234, 0.3), 0 0 40px rgba(59, 130, 246, 0.2); }
            50% { box-shadow: 0 0 40px rgba(147, 51, 234, 0.6), 0 0 80px rgba(59, 130, 246, 0.4), 0 0 100px rgba(236, 72, 153, 0.3); }
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes bounce-slow {
            0%, 100% { transform: translateY(0) scale(1); }
            50% { transform: translateY(-10px) scale(1.05); }
        }
        @keyframes rotate-slow {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        @keyframes gradient-shift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes sparkle {
            0%, 100% { opacity: 0; transform: scale(0); }
            50% { opacity: 1; transform: scale(1); }
        }
        .animate-pulse-slow {
            animation: pulse-slow 6s ease-in-out infinite;
        }
        .animate-float {
            animation: float 8s ease-in-out infinite;
        }
        .animate-glow {
            animation: glow 3s ease-in-out infinite;
        }
        .animate-bounce-slow {
            animation: bounce-slow 2s ease-in-out infinite;
        }
        .animate-rotate-slow {
            animation: rotate-slow 20s linear infinite;
        }
        .animate-gradient {
            background-size: 200% 200%;
            animation: gradient-shift 5s ease infinite;
        }
        .glass {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }
        .glass-strong {
            background: rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(25px);
            border: 1px solid rgba(255, 255, 255, 0.25);
        }
        .shimmer {
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
            background-size: 200% 100%;
            animation: shimmer 3s infinite;
        }
        .gradient-text {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .slide-in {
            animation: slideIn 0.5s ease-out forwards;
        }
        .fade-in-up {
            animation: fadeInUp 0.6s ease-out forwards;
        }
        .hover-lift {
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .hover-lift:hover {
            transform: translateY(-12px) scale(1.02);
            box-shadow: 0 25px 50px rgba(147, 51, 234, 0.3), 0 15px 30px rgba(59, 130, 246, 0.2);
        }
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        .btn-primary::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.6s;
        }
        .btn-primary:hover::before {
            left: 100%;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(147, 51, 234, 0.5);
        }
        .card-hover {
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .card-hover:hover {
            transform: translateY(-4px) scale(1.02);
            border-color: rgba(147, 51, 234, 0.6);
            box-shadow: 0 15px 40px rgba(147, 51, 234, 0.3), 0 5px 15px rgba(59, 130, 246, 0.2);
        }
        .sparkle {
            animation: sparkle 1.5s ease-in-out infinite;
        }
        .bg-animated {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 25%, #0f3460 50%, #533483 75%, #4a148c 100%);
            background-size: 400% 400%;
            animation: gradient-shift 15s ease infinite;
        }
        .text-glow {
            text-shadow: 0 0 10px rgba(147, 51, 234, 0.5), 0 0 20px rgba(59, 130, 246, 0.3);
        }
        .input-glow:focus {
            box-shadow: 0 0 0 3px rgba(147, 51, 234, 0.3), 0 0 20px rgba(147, 51, 234, 0.2);
        }
        .history-card {
            position: relative;
            overflow: hidden;
        }
        .history-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }
        .history-card:hover::before {
            left: 100%;
        }
    </style>
</head>
<body class="bg-animated min-h-screen">
    <!-- Animated Background -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
        <!-- Main gradient orbs -->
        <div class="absolute w-[500px] h-[500px] bg-purple-600/20 rounded-full blur-3xl animate-pulse-slow -top-48 -left-48"></div>
        <div class="absolute w-[500px] h-[500px] bg-blue-600/20 rounded-full blur-3xl animate-pulse-slow -bottom-48 -right-48" style="animation-delay: 2s;"></div>
        <div class="absolute w-[400px] h-[400px] bg-pink-600/20 rounded-full blur-3xl animate-pulse-slow top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" style="animation-delay: 4s;"></div>
        
        <!-- Floating orbs -->
        <div class="absolute w-64 h-64 bg-indigo-600/15 rounded-full blur-2xl animate-float top-20 right-20" style="animation-delay: 1s;"></div>
        <div class="absolute w-80 h-80 bg-violet-600/15 rounded-full blur-2xl animate-float bottom-40 left-40" style="animation-delay: 3s;"></div>
        <div class="absolute w-48 h-48 bg-fuchsia-600/15 rounded-full blur-2xl animate-float top-1/3 right-1/3" style="animation-delay: 5s;"></div>
        
        <!-- Sparkles -->
        <div class="absolute w-2 h-2 bg-white rounded-full top-1/4 left-1/4 sparkle" style="animation-delay: 0.5s;"></div>
        <div class="absolute w-2 h-2 bg-white rounded-full top-3/4 right-1/4 sparkle" style="animation-delay: 1.5s;"></div>
        <div class="absolute w-2 h-2 bg-white rounded-full bottom-1/4 left-3/4 sparkle" style="animation-delay: 2.5s;"></div>
    </div>

    <div class="relative z-10 container mx-auto px-4 py-8 max-w-7xl">
        <!-- Header -->
        <div class="text-center mb-12 fade-in-up">
            <div class="flex items-center justify-center mb-6 animate-bounce-slow">
                <div class="relative">
                    <div class="absolute inset-0 bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 rounded-full blur-2xl opacity-60 animate-glow"></div>
                    <div class="relative bg-gradient-to-br from-purple-600 via-pink-600 to-blue-600 p-5 rounded-2xl shadow-2xl animate-gradient">
                        <svg class="w-14 h-14 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                        </svg>
                    </div>
                </div>
            </div>
            <h1 class="text-7xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 mb-3 text-glow animate-gradient">
                PicBot
            </h1>
            <p class="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-pink-300 via-purple-300 to-blue-300 mb-6 text-glow">
                Dream It. Create It. Own It.
            </p>
            <p class="text-blue-200 text-lg font-light max-w-2xl mx-auto mb-6">
                Your AI-powered creative companion that transforms imagination into stunning visual reality
            </p>
            <div class="flex items-center justify-center gap-4 flex-wrap">
                <div class="flex items-center gap-2 glass rounded-full px-5 py-2.5 hover-lift">
                    <div class="w-2.5 h-2.5 bg-green-400 rounded-full animate-pulse"></div>
                    <span class="text-sm text-gray-200 font-semibold">AI Online</span>
                </div>
                <div class="flex items-center gap-2 glass rounded-full px-5 py-2.5 hover-lift">
                    <svg class="w-4 h-4 text-yellow-400 animate-pulse" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                    </svg>
                    <span class="text-sm text-gray-200 font-semibold">Premium Studio</span>
                </div>
                <div class="flex items-center gap-2 glass rounded-full px-5 py-2.5 hover-lift">
                    <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                    </svg>
                    <span class="text-sm text-gray-200 font-semibold">Lightning Fast</span>
                </div>
            </div>
        </div>

        <!-- Main Content -->
        <div class="grid lg:grid-cols-2 gap-8 mb-8">
            <!-- Left Panel -->
            <div class="space-y-6">
                <!-- Prompt Input -->
                <div class="glass rounded-2xl p-6 shadow-2xl hover:shadow-purple-500/20 transition-all duration-300">
                    <label class="block text-white text-lg font-semibold mb-3">🪄 Your Prompt</label>
                    <textarea id="promptInput" placeholder="Describe the image you want to create..." class="w-full px-4 py-3 bg-white/20 border border-white/30 rounded-xl text-white placeholder-blue-200 focus:outline-none focus:ring-2 focus:ring-purple-500 resize-none" rows="4"></textarea>
                    <div class="flex gap-3 mt-4">
                        <button onclick="generateImage()" id="generateBtn" class="flex-1 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-300 transform hover:scale-105">
                            🎨 Generate Image
                        </button>
                        <button onclick="refreshSuggestions()" class="bg-white/20 hover:bg-white/30 text-white p-3 rounded-xl transition-all duration-300">
                            🔄
                        </button>
                    </div>
                </div>

                <!-- Error/Status Message -->
                <div id="statusMessage" class="hidden glass rounded-xl p-4"></div>

                <!-- Trending Suggestions -->
                <div class="glass rounded-2xl p-6 shadow-2xl">
                    <h3 class="text-white text-lg font-semibold mb-4">✨ Trending Prompts</h3>
                    <div id="suggestions" class="grid grid-cols-1 gap-2"></div>
                </div>
            </div>

            <!-- Right Panel -->
            <div class="space-y-6">
                <div class="glass rounded-2xl p-6 shadow-2xl">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-white text-lg font-semibold">Generated Image</h3>
                        <button onclick="downloadImage()" id="downloadBtn" class="hidden bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-all">
                            📥 Download
                        </button>
                    </div>
                    <div id="imageContainer" class="aspect-square bg-white/5 rounded-xl flex items-center justify-center border-2 border-dashed border-white/20">
                        <div class="text-center p-8">
                            <div class="text-6xl mb-4">🖼️</div>
                            <p class="text-blue-200">Your generated image will appear here</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- History -->
        <div id="historySection" class="hidden glass-strong rounded-3xl p-8 shadow-2xl slide-in">
            <div class="flex items-center justify-between mb-6">
                <h3 class="text-white text-xl font-bold flex items-center">
                    <svg class="w-6 h-6 mr-3 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    Recent Creations
                    <span id="historyCount" class="ml-3 text-sm bg-indigo-600 px-3 py-1 rounded-full">0</span>
                </h3>
                <button onclick="clearHistory()" class="text-sm text-gray-400 hover:text-red-400 transition-colors">
                    Clear All
                </button>
            </div>
            <div id="historyGrid" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4"></div>
        </div>
    </div>

    <script>
        let history = [];
        let currentImage = null;
        let enhancedPromptText = '';

        function toggleEnhancer() {
            const section = document.getElementById('enhancerSection');
            section.classList.toggle('hidden');
        }

        async function enhancePrompt() {
            const prompt = document.getElementById('promptInput').value.trim();
            if (!prompt) {
                showStatus('Please enter a prompt first', 'error');
                return;
            }

            const btn = document.getElementById('enhanceBtn');
            const originalText = btn.innerHTML;
            btn.disabled = true;
            btn.innerHTML = '<svg class="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg> Enhancing...';

            try {
                const response = await fetch('/api/enhance-prompt', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt })
                });

                const data = await response.json();
                enhancedPromptText = data.enhanced || prompt;
                
                document.getElementById('enhancedPrompt').textContent = enhancedPromptText;
                document.getElementById('enhancerSection').classList.remove('hidden');
                showStatus('Prompt enhanced successfully!', 'success');
            } catch (error) {
                showStatus('Enhancement failed. Using original prompt.', 'error');
                enhancedPromptText = prompt;
            } finally {
                btn.disabled = false;
                btn.innerHTML = originalText;
            }
        }

        function useEnhancedPrompt() {
            if (enhancedPromptText) {
                document.getElementById('promptInput').value = enhancedPromptText;
                showStatus('Enhanced prompt applied!', 'success');
            }
        }

        async function generateImage() {
            const prompt = document.getElementById('promptInput').value.trim();
            if (!prompt) {
                showStatus('Please enter a prompt', 'error');
                return;
            }

            const btn = document.getElementById('generateBtn');
            btn.disabled = true;
            btn.innerHTML = '⏳ Generating...';
            
            showStatus('Creating your masterpiece...', 'info');
            document.getElementById('imageContainer').innerHTML = '<div class="text-center"><div class="text-6xl animate-spin">⚙️</div><p class="text-blue-200 mt-4">Generating image...</p></div>';

            try {
                const response = await fetch('/api/generate-image', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt })
                });

                const data = await response.json();

                if (data.error) {
                    showStatus(data.error, 'error');
                    if (data.retry) {
                        setTimeout(() => generateImage(), 20000);
                    }
                    document.getElementById('imageContainer').innerHTML = '<div class="text-center p-8"><div class="text-6xl mb-4">⚠️</div><p class="text-red-200">Generation failed. Please try again.</p></div>';
                } else {
                    currentImage = data.image;
                    document.getElementById('imageContainer').innerHTML = `<img src="${data.image}" alt="Generated" class="w-full h-full object-cover rounded-xl">`;
                    document.getElementById('downloadBtn').classList.remove('hidden');
                    showStatus('Image generated successfully!', 'success');
                    
                    history.unshift({ prompt, image: data.image });
                    if (history.length > 6) history.pop();
                    updateHistory();
                }
            } catch (error) {
                showStatus('Failed to generate image. Please try again.', 'error');
                document.getElementById('imageContainer').innerHTML = '<div class="text-center p-8"><div class="text-6xl mb-4">❌</div><p class="text-red-200">Connection error</p></div>';
            } finally {
                btn.disabled = false;
                btn.innerHTML = '🎨 Generate Image';
            }
        }

        function showStatus(message, type) {
            const status = document.getElementById('statusMessage');
            status.classList.remove('hidden', 'bg-red-500/20', 'bg-green-500/20', 'bg-blue-500/20', 'border-red-500/50', 'border-green-500/50', 'border-blue-500/50');
            
            const bgColor = type === 'error' ? 'bg-red-500/20' : type === 'success' ? 'bg-green-500/20' : 'bg-blue-500/20';
            const borderColor = type === 'error' ? 'border-red-500/50' : type === 'success' ? 'border-green-500/50' : 'border-blue-500/50';
            const icon = type === 'error' ? '⚠️' : type === 'success' ? '✅' : 'ℹ️';
            
            status.className = `glass rounded-xl p-4 border-2 ${bgColor} ${borderColor} slide-in`;
            status.innerHTML = `
                <div class="flex items-center gap-3">
                    <span class="text-2xl">${icon}</span>
                    <span class="text-white font-medium">${message}</span>
                </div>
            `;
        }

        async function refreshSuggestions() {
            try {
                const response = await fetch('/api/suggestions');
                const data = await response.json();
                const container = document.getElementById('suggestions');
                container.innerHTML = data.suggestions.map(s => 
                    `<button onclick="useSuggestion(\`${s.replace(/`/g, '\\`')}\`)" class="text-left px-5 py-3 bg-white/10 hover:bg-gradient-to-r hover:from-purple-600/30 hover:to-blue-600/30 text-gray-200 rounded-xl transition-all duration-300 text-sm border border-white/20 hover:border-purple-400/60 transform hover:scale-105 hover:-translate-y-1 card-hover shadow-lg">
                        <div class="flex items-center gap-2">
                            <svg class="w-4 h-4 text-purple-400" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 1.414L10.586 9H7a1 1 0 100 2h3.586l-1.293 1.293a1 1 0 101.414 1.414l3-3a1 1 0 000-1.414z" clip-rule="evenodd"></path>
                            </svg>
                            <span>${s}</span>
                        </div>
                    </button>`
                ).join('');
            } catch (error) {
                console.error('Failed to fetch suggestions:', error);
            }
        }

        function useSuggestion(suggestion) {
            document.getElementById('promptInput').value = suggestion;
            showStatus('Prompt suggestion applied!', 'success');
        }

        function downloadImage() {
            if (!currentImage) return;
            const link = document.createElement('a');
            link.href = currentImage;
            link.download = `ai-generated-${Date.now()}.jpg`;
            link.click();
            showStatus('Image downloaded successfully!', 'success');
        }

        function updateHistory() {
            if (history.length === 0) return;
            document.getElementById('historySection').classList.remove('hidden');
            document.getElementById('historyCount').textContent = history.length;
            const grid = document.getElementById('historyGrid');
            grid.innerHTML = history.map((item, i) => 
                `<div class="group relative aspect-square bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl overflow-hidden border-2 border-white/20 hover:border-purple-500/60 transition-all duration-300 transform hover:scale-105 hover:-translate-y-2 cursor-pointer shadow-lg hover:shadow-2xl hover:shadow-purple-500/30 history-card" onclick="viewHistoryImage(${i})" title="${item.prompt}">
                    <img src="${item.image}" alt="${item.prompt}" class="w-full h-full object-cover">
                    <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                        <div class="absolute bottom-2 left-2 right-2">
                            <p class="text-white text-xs font-medium truncate">${item.prompt}</p>
                        </div>
                    </div>
                    <div class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button class="bg-purple-600 hover:bg-purple-700 text-white p-1.5 rounded-lg transform hover:scale-110 transition-all">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                            </svg>
                        </button>
                    </div>
                </div>`
            ).join('');
        }

        function randomPrompt() {
            const magicPrompts = [
                "An ethereal goddess with flowing cosmic hair in a starlit dimension",
                "A neon-lit cyberpunk samurai standing in rain-soaked Tokyo streets",
                "A majestic phoenix rising from crystal flames in an enchanted forest",
                "An ancient wizard's library with floating books and magical artifacts",
                "A steampunk airship battle above Victorian London at sunset",
                "A mystical underwater city with bioluminescent architecture",
                "A cosmic dragon weaving through nebula clouds in deep space",
                "A magical marketplace where reality bends and time flows differently",
                "An ice palace with aurora borealis dancing in the arctic sky",
                "A futuristic garden where nature and technology merge seamlessly"
            ];
            const randomIndex = Math.floor(Math.random() * magicPrompts.length);
            document.getElementById('promptInput').value = magicPrompts[randomIndex];
            showStatus('✨ Magic prompt applied! Ready to create?', 'success');
        }

        function viewHistoryImage(index) {
            currentImage = history[index].image;
            document.getElementById('imageContainer').innerHTML = `<img src="${currentImage}" alt="Generated" class="w-full h-full object-cover rounded-2xl transform hover:scale-105 transition-transform duration-500">`;
            document.getElementById('downloadBtn').classList.remove('hidden');
            document.getElementById('imageInfo').classList.remove('hidden');
            showStatus('Viewing image from history', 'info');
        }

        function clearHistory() {
            if (confirm('Are you sure you want to clear all history?')) {
                history = [];
                document.getElementById('historySection').classList.add('hidden');
                showStatus('History cleared', 'success');
            }
        }

        // Initialize
        refreshSuggestions();
        
        // Add keyboard shortcuts
        document.getElementById('promptInput').addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                generateImage();
            }
            if (e.ctrlKey && e.key === 'e') {
                e.preventDefault();
                enhancePrompt();
            }
            if (e.ctrlKey && e.key === 'm') {
                e.preventDefault();
                randomPrompt();
            }
        });

        // Welcome message
        setTimeout(() => {
            showStatus('👋 Welcome to PicBot! Start creating by entering a prompt or use our Magic button for instant inspiration.', 'info');
        }, 1000);
    </script>
</body>
</html>"""

# Create static directory and save HTML
os.makedirs('static', exist_ok=True)
with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(HTML_TEMPLATE)

# if __name__ == '__main__':
#     print("\n" + "="*60)
#     print("🚀 AI Image Generator - Starting Server")
#     print("="*60)
#     print(f"✓ Flask initialized")
#     print(f"✓ API Key configured: {bool(HUGGINGFACE_API_KEY)}")
#     print(f"✓ LangChain status: {'Active' if enhancement_chain else 'Fallback mode'}")
#     print(f"✓ Image Model: {IMAGE_MODEL}")
#     print(f"✓ Text Model: {TEXT_MODEL}")
#     print("\n📝 Access the app at: http://localhost:5000")
#     print("="*60 + "\n")
    
#     app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":

    from dotenv import load_dotenv 
    load_dotenv()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
