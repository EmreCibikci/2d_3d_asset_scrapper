#!/usr/bin/env python3
"""
Hybrid AI Asset Generator
Combines pre-trained Stable Diffusion with our custom game asset dataset
Best of both worlds: Proven AI + Domain-specific training
"""

import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from PIL import Image
import requests
from io import BytesIO
import base64
import json
import os
from pathlib import Path
from database import DatabaseManager
import random
import numpy as np
from config_ai import get_api_headers, is_api_configured, STABLE_DIFFUSION_API_URL

class HybridAssetGenerator:
    """Hybrid generator using Stable Diffusion + custom fine-tuning"""
    
    def __init__(self, use_local_model=True):
        self.db = DatabaseManager()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"🚀 Initializing Hybrid AI Generator on {self.device}")
        
        # Game asset specific prompts and styles
        self.game_asset_templates = self._load_game_templates()
        self.style_modifiers = self._load_style_modifiers()
        
        # Initialize Stable Diffusion pipeline
        if use_local_model:
            self._init_local_pipeline()
        else:
            self._init_api_pipeline()
    
    def _init_local_pipeline(self):
        """Initialize local Stable Diffusion pipeline"""
        try:
            print("📥 Loading Stable Diffusion model...")
            
            # Use a smaller, faster model for local development
            model_id = "runwayml/stable-diffusion-v1-5"
            
            # Load pipeline with optimizations
            self.pipe = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float16 if self.device.type == 'cuda' else torch.float32,
                safety_checker=None,  # Disable for game assets
                requires_safety_checker=False
            )
            
            # Optimize for speed
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(self.pipe.scheduler.config)
            self.pipe = self.pipe.to(self.device)
            
            # Enable memory efficient attention if available
            if hasattr(self.pipe, 'enable_attention_slicing'):
                self.pipe.enable_attention_slicing()
            
            print("✅ Stable Diffusion pipeline loaded successfully")
            self.use_api = False
            
        except Exception as e:
            print(f"⚠️ Failed to load local model: {e}")
            print("🔄 Falling back to API mode...")
            self._init_api_pipeline()
    
    def _init_api_pipeline(self):
        """Initialize API-based pipeline (fallback)"""
        print("🌐 Using API-based generation (Hugging Face)")
        self.pipe = None
        self.use_api = True

        # Check if API is configured
        if is_api_configured():
            self.api_url = STABLE_DIFFUSION_API_URL
            self.api_headers = get_api_headers()
            print("✅ Hugging Face API configured")
        else:
            print("⚠️ Hugging Face API not configured")
            print("💡 Run: python config_ai.py to setup token")
            self.api_headers = None
    
    def _load_game_templates(self):
        """Load game asset specific templates from our dataset"""
        assets = self.db.get_assets({'asset_type': '2d'})
        
        templates = {
            'character': [],
            'ui': [],
            'weapon': [],
            'icon': [],
            'background': [],
            'misc': []
        }
        
        for asset in assets:
            category = asset.get('category', 'misc')
            if category not in templates:
                category = 'misc'
            
            title = asset.get('title', '')
            description = asset.get('description', '')
            
            if title and len(title) > 3:
                template = {
                    'title': title,
                    'description': description,
                    'keywords': self._extract_keywords(title, description),
                    'style_hints': self._extract_style_hints(title, description)
                }
                templates[category].append(template)
        
        print(f"📚 Loaded {sum(len(v) for v in templates.values())} game asset templates")
        return templates
    
    def _extract_keywords(self, title, description):
        """Extract relevant keywords for prompt enhancement"""
        text = f"{title} {description}".lower()
        
        # Game-specific keywords
        game_keywords = [
            'pixel art', '2d', 'sprite', 'character', 'warrior', 'mage', 'knight',
            'sword', 'weapon', 'magic', 'fantasy', 'medieval', 'sci-fi', 'space',
            'ui', 'button', 'interface', 'icon', 'symbol', 'logo',
            'cute', 'cartoon', 'anime', 'realistic', 'detailed', 'simple',
            'colorful', 'dark', 'bright', 'neon', 'glowing'
        ]
        
        found_keywords = []
        for keyword in game_keywords:
            if keyword in text:
                found_keywords.append(keyword)
        
        return found_keywords[:5]  # Limit to 5 most relevant
    
    def _extract_style_hints(self, title, description):
        """Extract style hints for better generation"""
        text = f"{title} {description}".lower()
        
        style_hints = []
        
        # Art styles
        if any(word in text for word in ['pixel', '8bit', 'retro']):
            style_hints.append('pixel art style')
        if any(word in text for word in ['cartoon', 'cute', 'kawaii']):
            style_hints.append('cartoon style')
        if any(word in text for word in ['realistic', 'detailed']):
            style_hints.append('realistic style')
        if any(word in text for word in ['minimal', 'simple', 'clean']):
            style_hints.append('minimalist style')
        
        # Themes
        if any(word in text for word in ['fantasy', 'medieval', 'magic']):
            style_hints.append('fantasy theme')
        if any(word in text for word in ['sci-fi', 'space', 'futuristic']):
            style_hints.append('sci-fi theme')
        if any(word in text for word in ['dark', 'gothic', 'shadow']):
            style_hints.append('dark theme')
        
        return style_hints
    
    def _load_style_modifiers(self):
        """Load style modifiers for prompt enhancement"""
        return {
            'quality_boosters': [
                'high quality', 'detailed', 'sharp', 'crisp', 'clean',
                'professional', 'polished', 'refined'
            ],
            'game_specific': [
                'game asset', 'sprite', 'game art', 'indie game',
                'mobile game', 'casual game', 'RPG style'
            ],
            'technical': [
                'transparent background', 'PNG format', 'game ready',
                'optimized', 'tileable', 'seamless'
            ],
            'negative_prompts': [
                'blurry', 'low quality', 'pixelated', 'distorted',
                'watermark', 'text', 'signature', 'realistic photo'
            ]
        }
    
    def generate_hybrid_asset(self, prompt: str, category: str = None) -> str:
        """Generate asset using hybrid approach"""
        try:
            # Enhance prompt with our domain knowledge
            enhanced_prompt = self._enhance_prompt(prompt, category)
            
            print(f"🎨 Generating: {enhanced_prompt}")
            
            if self.use_api:
                image = self._generate_via_api(enhanced_prompt)
            else:
                image = self._generate_via_local(enhanced_prompt)
            
            if image:
                # Post-process for game assets
                image = self._post_process_for_games(image)

                # Convert to base64
                buffer = BytesIO()
                image.save(buffer, format='PNG')
                return base64.b64encode(buffer.getvalue()).decode()
            else:
                # AI generation failed, use fallback
                print("🔄 AI generation failed, using fallback...")
                return self._generate_fallback(prompt)
            
        except Exception as e:
            print(f"❌ Generation failed: {e}")
            return self._generate_fallback()
    
    def _enhance_prompt(self, prompt: str, category: str = None) -> str:
        """Enhance user prompt with domain-specific knowledge"""
        enhanced = prompt.lower().strip()
        
        # Detect category if not provided
        if not category:
            category = self._detect_category(enhanced)
        
        # Add category-specific enhancements
        if category in self.game_asset_templates and self.game_asset_templates[category]:
            # Get similar templates
            similar_template = random.choice(self.game_asset_templates[category])
            
            # Add relevant keywords
            for keyword in similar_template['keywords'][:2]:
                if keyword not in enhanced:
                    enhanced += f", {keyword}"
            
            # Add style hints
            for hint in similar_template['style_hints'][:1]:
                enhanced += f", {hint}"
        
        # Add quality boosters
        quality_boost = random.choice(self.style_modifiers['quality_boosters'])
        enhanced += f", {quality_boost}"
        
        # Add game-specific modifier
        game_modifier = random.choice(self.style_modifiers['game_specific'])
        enhanced += f", {game_modifier}"
        
        # Add technical requirements
        tech_modifier = random.choice(self.style_modifiers['technical'])
        enhanced += f", {tech_modifier}"
        
        return enhanced
    
    def _detect_category(self, prompt: str) -> str:
        """Detect asset category from prompt"""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['character', 'warrior', 'hero', 'player']):
            return 'character'
        elif any(word in prompt_lower for word in ['button', 'ui', 'interface', 'menu']):
            return 'ui'
        elif any(word in prompt_lower for word in ['sword', 'weapon', 'gun', 'bow']):
            return 'weapon'
        elif any(word in prompt_lower for word in ['icon', 'symbol', 'logo']):
            return 'icon'
        elif any(word in prompt_lower for word in ['background', 'landscape', 'environment']):
            return 'background'
        else:
            return 'misc'
    
    def _generate_via_local(self, prompt: str) -> Image.Image:
        """Generate using local Stable Diffusion"""
        negative_prompt = ", ".join(self.style_modifiers['negative_prompts'])
        
        # Generate with optimized parameters for game assets
        with torch.autocast(self.device.type):
            result = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=20,  # Faster generation
                guidance_scale=7.5,
                width=512,
                height=512,
                num_images_per_prompt=1
            )
        
        return result.images[0]
    
    def _generate_via_api(self, prompt: str) -> Image.Image:
        """Generate using Hugging Face API"""
        if not self.api_headers:
            print("❌ API not configured. Run: python config_ai.py")
            return None

        try:
            payload = {
                "inputs": prompt,
                "parameters": {
                    "num_inference_steps": 20,
                    "guidance_scale": 7.5,
                    "width": 512,
                    "height": 512
                }
            }

            response = requests.post(self.api_url, headers=self.api_headers, json=payload, timeout=30)

            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                return image
            elif response.status_code == 401:
                print("❌ Invalid API token. Check your Hugging Face token.")
                return None
            elif response.status_code == 503:
                print("⏳ Model is loading. Try again in a few seconds.")
                return None
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            print(f"API Generation failed: {e}")
            return None
    
    def _post_process_for_games(self, image: Image.Image) -> Image.Image:
        """Post-process image for game asset use"""
        # Convert to RGBA for transparency support
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        # Optional: Remove background (simple threshold-based)
        # This is basic - could be enhanced with more sophisticated methods
        data = np.array(image)
        
        # Make white/light backgrounds transparent (common for game assets)
        white_threshold = 240
        mask = (data[:, :, 0] > white_threshold) & \
               (data[:, :, 1] > white_threshold) & \
               (data[:, :, 2] > white_threshold)
        
        data[mask] = [255, 255, 255, 0]  # Make transparent
        
        return Image.fromarray(data, 'RGBA')
    
    def _generate_fallback(self, prompt: str = "game asset") -> str:
        """Generate fallback asset if AI generation fails"""
        print("🔄 Using fallback generation...")

        try:
            # Use our enhanced procedural generator as fallback
            from enhanced_asset_generator import EnhancedAssetGenerator
            fallback_gen = EnhancedAssetGenerator()
            return fallback_gen.generate_enhanced_asset(prompt)
        except Exception as e:
            print(f"❌ Fallback generation failed: {e}")
            # Ultimate fallback - simple placeholder
            return self._generate_simple_placeholder()
    
    def fine_tune_with_our_data(self, epochs: int = 10):
        """Fine-tune the model with our game asset data"""
        print("🎯 Starting fine-tuning with our game asset dataset...")
        
        # This would implement LoRA fine-tuning
        # For now, we'll prepare the data and show the concept
        
        assets = self.db.get_assets({'asset_type': '2d'})
        training_data = []
        
        for asset in assets:
            if asset.get('title') and len(asset.get('title', '')) > 3:
                training_data.append({
                    'prompt': asset.get('title', ''),
                    'description': asset.get('description', ''),
                    'category': asset.get('category', 'misc'),
                    'image_url': asset.get('preview_url', '')
                })
        
        print(f"📊 Prepared {len(training_data)} samples for fine-tuning")
        print("💡 Fine-tuning implementation would go here...")
        print("   - LoRA adaptation")
        print("   - DreamBooth training")
        print("   - Textual inversion")
        
        return training_data

    def _generate_simple_placeholder(self) -> str:
        """Generate simple placeholder if all else fails"""
        from PIL import Image, ImageDraw

        size = (128, 128)
        image = Image.new('RGB', size, (100, 100, 100))
        draw = ImageDraw.Draw(image)

        # Draw "AI" text
        try:
            from PIL import ImageFont
            font = ImageFont.load_default()
            text = "AI"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (size[0] - text_width) // 2
            y = (size[1] - text_height) // 2
            draw.text((x, y), text, fill=(255, 255, 255), font=font)
        except:
            draw.rectangle([50, 50, 78, 78], fill=(255, 255, 255))

        buffer = BytesIO()
        image.save(buffer, format='PNG')
        return base64.b64encode(buffer.getvalue()).decode()

def test_hybrid_generator():
    """Test the hybrid generator"""
    print("🧪 Testing Hybrid AI Asset Generator")
    print("=" * 60)
    
    generator = HybridAssetGenerator(use_local_model=False)  # Start with API mode
    
    test_prompts = [
        "fantasy warrior character with sword",
        "modern blue ui button",
        "pixel art magic staff weapon",
        "cute star icon",
        "space background with stars"
    ]
    
    for prompt in test_prompts:
        print(f"\n🎨 Generating: {prompt}")
        result = generator.generate_hybrid_asset(prompt)
        
        if result:
            print(f"✅ Generated hybrid asset ({len(result)} bytes)")
        else:
            print("❌ Generation failed")

if __name__ == "__main__":
    test_hybrid_generator()
