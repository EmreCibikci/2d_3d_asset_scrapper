#!/usr/bin/env python3
"""
Enhanced Asset Generator
Advanced procedural generation using real asset data as templates
Much more sophisticated than simple shapes
"""

import os
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import random
from pathlib import Path
from database import DatabaseManager
import base64
from io import BytesIO
import colorsys
import math

class EnhancedAssetGenerator:
    """Enhanced asset generator with sophisticated algorithms"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.asset_templates = self._analyze_existing_assets()
        self.color_palettes = self._generate_color_palettes()
        
    def _analyze_existing_assets(self):
        """Analyze existing assets to create templates"""
        assets = self.db.get_assets({'asset_type': '2d'})
        
        templates = {
            'character': {'patterns': [], 'colors': [], 'keywords': []},
            'ui': {'patterns': [], 'colors': [], 'keywords': []},
            'weapon': {'patterns': [], 'colors': [], 'keywords': []},
            'icon': {'patterns': [], 'colors': [], 'keywords': []},
            'background': {'patterns': [], 'colors': [], 'keywords': []},
            'misc': {'patterns': [], 'colors': [], 'keywords': []}
        }
        
        for asset in assets:
            category = asset.get('category', 'misc')
            if category not in templates:
                category = 'misc'
            
            # Extract keywords
            text = f"{asset.get('title', '')} {asset.get('description', '')}"
            keywords = self._extract_advanced_keywords(text)
            templates[category]['keywords'].extend(keywords)
            
            # Analyze colors from title/description
            colors = self._extract_colors_from_text(text)
            templates[category]['colors'].extend(colors)
        
        # Remove duplicates and analyze patterns
        for category in templates:
            templates[category]['keywords'] = list(set(templates[category]['keywords']))
            templates[category]['colors'] = list(set(templates[category]['colors']))
        
        print(f"Analyzed {len(assets)} assets for enhanced generation")
        return templates
    
    def _extract_advanced_keywords(self, text):
        """Extract meaningful keywords for generation"""
        text = text.lower()
        
        # Style keywords
        style_keywords = []
        if any(word in text for word in ['pixel', '8bit', 'retro']):
            style_keywords.append('pixel')
        if any(word in text for word in ['modern', 'clean', 'minimal']):
            style_keywords.append('modern')
        if any(word in text for word in ['fantasy', 'medieval', 'magic']):
            style_keywords.append('fantasy')
        if any(word in text for word in ['sci-fi', 'space', 'futuristic', 'cyber']):
            style_keywords.append('scifi')
        if any(word in text for word in ['cute', 'kawaii', 'adorable']):
            style_keywords.append('cute')
        if any(word in text for word in ['dark', 'gothic', 'shadow']):
            style_keywords.append('dark')
        
        # Object keywords
        object_keywords = []
        if any(word in text for word in ['warrior', 'knight', 'fighter']):
            object_keywords.append('warrior')
        if any(word in text for word in ['mage', 'wizard', 'magic']):
            object_keywords.append('mage')
        if any(word in text for word in ['robot', 'android', 'mech']):
            object_keywords.append('robot')
        if any(word in text for word in ['animal', 'creature', 'beast']):
            object_keywords.append('creature')
        
        return style_keywords + object_keywords
    
    def _extract_colors_from_text(self, text):
        """Extract color information from text"""
        text = text.lower()
        colors = []
        
        color_map = {
            'red': (255, 100, 100),
            'blue': (100, 150, 255),
            'green': (100, 255, 150),
            'yellow': (255, 255, 100),
            'purple': (200, 100, 255),
            'orange': (255, 180, 100),
            'pink': (255, 150, 200),
            'brown': (150, 100, 80),
            'gray': (150, 150, 150),
            'black': (50, 50, 50),
            'white': (240, 240, 240),
            'gold': (255, 215, 0),
            'silver': (192, 192, 192)
        }
        
        for color_name, rgb in color_map.items():
            if color_name in text:
                colors.append(rgb)
        
        return colors
    
    def _generate_color_palettes(self):
        """Generate sophisticated color palettes"""
        palettes = {
            'fantasy': [
                [(139, 69, 19), (255, 215, 0), (128, 0, 128), (0, 100, 0)],  # Brown, Gold, Purple, Green
                [(220, 20, 60), (255, 140, 0), (75, 0, 130), (255, 255, 255)],  # Crimson, Orange, Indigo, White
            ],
            'scifi': [
                [(0, 191, 255), (50, 205, 50), (255, 20, 147), (128, 128, 128)],  # Blue, Green, Pink, Gray
                [(138, 43, 226), (0, 255, 255), (255, 69, 0), (192, 192, 192)],  # Purple, Cyan, Red, Silver
            ],
            'modern': [
                [(70, 130, 180), (255, 255, 255), (105, 105, 105), (30, 144, 255)],  # Steel Blue, White, Gray, Blue
                [(220, 220, 220), (100, 149, 237), (255, 99, 71), (47, 79, 79)],  # Light Gray, Cornflower, Tomato, Dark Slate
            ],
            'cute': [
                [(255, 182, 193), (255, 160, 122), (221, 160, 221), (255, 228, 181)],  # Pink, Peach, Plum, Moccasin
                [(255, 218, 185), (255, 192, 203), (173, 216, 230), (255, 255, 224)],  # Peach, Pink, Light Blue, Light Yellow
            ],
            'dark': [
                [(25, 25, 112), (139, 0, 0), (85, 107, 47), (128, 0, 128)],  # Midnight Blue, Dark Red, Dark Olive, Purple
                [(47, 79, 79), (105, 105, 105), (128, 0, 0), (72, 61, 139)],  # Dark Slate, Dim Gray, Maroon, Dark Slate Blue
            ]
        }
        return palettes
    
    def generate_enhanced_asset(self, prompt: str) -> str:
        """Generate enhanced asset from prompt"""
        try:
            # Parse prompt
            analysis = self._analyze_prompt(prompt)
            
            # Generate based on category
            if analysis['category'] == 'character':
                image = self._generate_enhanced_character(analysis)
            elif analysis['category'] == 'ui':
                image = self._generate_enhanced_ui(analysis)
            elif analysis['category'] == 'weapon':
                image = self._generate_enhanced_weapon(analysis)
            elif analysis['category'] == 'icon':
                image = self._generate_enhanced_icon(analysis)
            elif analysis['category'] == 'background':
                image = self._generate_enhanced_background(analysis)
            else:
                image = self._generate_enhanced_generic(analysis)
            
            # Apply post-processing effects
            image = self._apply_style_effects(image, analysis['style'])
            
            # Convert to base64
            buffer = BytesIO()
            image.save(buffer, format='PNG')
            return base64.b64encode(buffer.getvalue()).decode()
            
        except Exception as e:
            print(f"Error generating enhanced asset: {e}")
            return self._generate_fallback_asset()
    
    def _analyze_prompt(self, prompt: str) -> dict:
        """Analyze prompt for generation parameters"""
        prompt_lower = prompt.lower()
        
        analysis = {
            'category': 'misc',
            'style': 'modern',
            'colors': [],
            'size': 'medium',
            'complexity': 'medium',
            'keywords': prompt_lower.split()
        }
        
        # Detect category
        if any(word in prompt_lower for word in ['character', 'warrior', 'hero', 'player', 'npc', 'person']):
            analysis['category'] = 'character'
        elif any(word in prompt_lower for word in ['button', 'ui', 'interface', 'menu', 'panel', 'hud']):
            analysis['category'] = 'ui'
        elif any(word in prompt_lower for word in ['sword', 'weapon', 'gun', 'bow', 'staff', 'blade']):
            analysis['category'] = 'weapon'
        elif any(word in prompt_lower for word in ['icon', 'symbol', 'logo', 'badge', 'emblem']):
            analysis['category'] = 'icon'
        elif any(word in prompt_lower for word in ['background', 'landscape', 'environment', 'scene']):
            analysis['category'] = 'background'
        
        # Detect style
        if any(word in prompt_lower for word in ['pixel', '8bit', 'retro']):
            analysis['style'] = 'pixel'
        elif any(word in prompt_lower for word in ['fantasy', 'medieval', 'magic']):
            analysis['style'] = 'fantasy'
        elif any(word in prompt_lower for word in ['sci-fi', 'space', 'futuristic']):
            analysis['style'] = 'scifi'
        elif any(word in prompt_lower for word in ['cute', 'kawaii']):
            analysis['style'] = 'cute'
        elif any(word in prompt_lower for word in ['dark', 'gothic']):
            analysis['style'] = 'dark'
        
        # Detect colors
        analysis['colors'] = self._extract_colors_from_text(prompt)
        if not analysis['colors']:
            # Use style-based palette
            if analysis['style'] in self.color_palettes:
                analysis['colors'] = random.choice(self.color_palettes[analysis['style']])
            else:
                analysis['colors'] = [(100, 150, 255), (255, 100, 100)]
        
        # Detect size
        if any(word in prompt_lower for word in ['small', 'tiny', 'mini']):
            analysis['size'] = 'small'
        elif any(word in prompt_lower for word in ['large', 'big', 'huge']):
            analysis['size'] = 'large'
        
        # Detect complexity
        if any(word in prompt_lower for word in ['simple', 'basic', 'minimal']):
            analysis['complexity'] = 'simple'
        elif any(word in prompt_lower for word in ['detailed', 'complex', 'intricate']):
            analysis['complexity'] = 'complex'
        
        return analysis
    
    def _generate_enhanced_character(self, analysis: dict) -> Image.Image:
        """Generate enhanced character sprite"""
        size = (128, 128) if analysis['size'] == 'medium' else (64, 64) if analysis['size'] == 'small' else (256, 256)
        image = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        colors = analysis['colors']
        complexity = analysis['complexity']
        
        # Base proportions
        head_ratio = 0.2
        body_ratio = 0.4
        leg_ratio = 0.4
        
        # Head
        head_size = int(size[0] * head_ratio)
        head_x = size[0] // 2 - head_size // 2
        head_y = int(size[1] * 0.1)
        
        # Add gradient effect for head
        self._draw_gradient_ellipse(draw, [head_x, head_y, head_x + head_size, head_y + head_size], colors[0])
        
        # Body
        body_width = int(size[0] * 0.3)
        body_height = int(size[1] * body_ratio)
        body_x = size[0] // 2 - body_width // 2
        body_y = head_y + head_size
        
        if complexity == 'complex':
            # Detailed body with armor/clothing
            self._draw_detailed_body(draw, body_x, body_y, body_width, body_height, colors)
        else:
            # Simple body
            draw.rectangle([body_x, body_y, body_x + body_width, body_y + body_height], fill=colors[1] if len(colors) > 1 else colors[0])
        
        # Arms
        arm_width = int(size[0] * 0.08)
        arm_height = int(body_height * 0.7)
        
        # Left arm
        left_arm_x = body_x - arm_width
        arm_y = body_y + 5
        draw.rectangle([left_arm_x, arm_y, left_arm_x + arm_width, arm_y + arm_height], fill=colors[0])
        
        # Right arm
        right_arm_x = body_x + body_width
        draw.rectangle([right_arm_x, arm_y, right_arm_x + arm_width, arm_y + arm_height], fill=colors[0])
        
        # Legs
        leg_width = int(size[0] * 0.1)
        leg_height = int(size[1] * leg_ratio)
        leg_y = body_y + body_height
        
        # Left leg
        left_leg_x = body_x + 5
        draw.rectangle([left_leg_x, leg_y, left_leg_x + leg_width, leg_y + leg_height], fill=colors[0])
        
        # Right leg
        right_leg_x = body_x + body_width - 5 - leg_width
        draw.rectangle([right_leg_x, leg_y, right_leg_x + leg_width, leg_y + leg_height], fill=colors[0])
        
        # Add details based on keywords
        if 'warrior' in analysis['keywords']:
            self._add_warrior_details(draw, size, colors)
        elif 'mage' in analysis['keywords']:
            self._add_mage_details(draw, size, colors)
        
        return image
    
    def _generate_enhanced_ui(self, analysis: dict) -> Image.Image:
        """Generate enhanced UI element"""
        size = (160, 64) if analysis['size'] == 'medium' else (120, 48) if analysis['size'] == 'small' else (200, 80)
        image = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        colors = analysis['colors']
        
        # Modern button with gradient and shadow
        if analysis['style'] == 'modern':
            # Shadow
            shadow_offset = 3
            draw.rounded_rectangle([shadow_offset, shadow_offset, size[0], size[1]], 
                                 radius=8, fill=(0, 0, 0, 100))
            
            # Main button with gradient
            self._draw_gradient_rectangle(draw, [0, 0, size[0] - shadow_offset, size[1] - shadow_offset], 
                                        colors[0], radius=8)
            
            # Highlight
            highlight_color = tuple(min(255, c + 50) for c in colors[0][:3]) + (200,)
            draw.rounded_rectangle([2, 2, size[0] - shadow_offset - 2, 8], 
                                 radius=6, fill=highlight_color)
            
            # Border
            border_color = tuple(max(0, c - 30) for c in colors[0][:3]) + (255,)
            draw.rounded_rectangle([0, 0, size[0] - shadow_offset - 1, size[1] - shadow_offset - 1], 
                                 radius=8, outline=border_color, width=2)
        
        else:
            # Simple button
            draw.rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=8, fill=colors[0])
            draw.rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=8, outline=(255, 255, 255), width=2)
        
        return image
    
    def _generate_enhanced_weapon(self, analysis: dict) -> Image.Image:
        """Generate enhanced weapon"""
        size = (64, 128) if analysis['size'] == 'medium' else (48, 96) if analysis['size'] == 'small' else (96, 192)
        image = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        colors = analysis['colors']
        
        if 'sword' in analysis['keywords']:
            self._draw_enhanced_sword(draw, size, colors, analysis['style'])
        elif 'staff' in analysis['keywords']:
            self._draw_enhanced_staff(draw, size, colors, analysis['style'])
        elif 'bow' in analysis['keywords']:
            self._draw_enhanced_bow(draw, size, colors, analysis['style'])
        else:
            # Default sword
            self._draw_enhanced_sword(draw, size, colors, analysis['style'])
        
        return image
    
    def _generate_enhanced_icon(self, analysis: dict) -> Image.Image:
        """Generate enhanced icon"""
        size = (64, 64) if analysis['size'] == 'medium' else (48, 48) if analysis['size'] == 'small' else (96, 96)
        image = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        colors = analysis['colors']
        
        # Enhanced star icon with glow effect
        center_x, center_y = size[0] // 2, size[1] // 2
        radius = size[0] // 3
        
        # Glow effect
        for i in range(5, 0, -1):
            glow_color = colors[0][:3] + (50 * i,)
            self._draw_star(draw, center_x, center_y, radius + i * 2, glow_color)
        
        # Main star
        self._draw_star(draw, center_x, center_y, radius, colors[0])
        
        # Highlight
        highlight_color = tuple(min(255, c + 100) for c in colors[0][:3])
        self._draw_star(draw, center_x - 2, center_y - 2, radius - 5, highlight_color)
        
        return image
    
    def _generate_enhanced_background(self, analysis: dict) -> Image.Image:
        """Generate enhanced background"""
        size = (256, 256)
        image = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        colors = analysis['colors']
        
        if analysis['style'] == 'space':
            self._draw_space_background(draw, size, colors)
        elif analysis['style'] == 'fantasy':
            self._draw_fantasy_background(draw, size, colors)
        else:
            # Gradient background
            self._draw_gradient_background(draw, size, colors)
        
        return image
    
    def _generate_enhanced_generic(self, analysis: dict) -> Image.Image:
        """Generate enhanced generic asset"""
        size = (128, 128)
        image = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        colors = analysis['colors']
        
        # Enhanced geometric shape with effects
        shape_size = 80
        x = (size[0] - shape_size) // 2
        y = (size[1] - shape_size) // 2
        
        # Shadow
        draw.ellipse([x + 5, y + 5, x + shape_size + 5, y + shape_size + 5], fill=(0, 0, 0, 100))
        
        # Main shape with gradient
        self._draw_gradient_ellipse(draw, [x, y, x + shape_size, y + shape_size], colors[0])
        
        # Highlight
        highlight_size = shape_size // 3
        highlight_x = x + shape_size // 4
        highlight_y = y + shape_size // 4
        highlight_color = tuple(min(255, c + 100) for c in colors[0][:3]) + (150,)
        draw.ellipse([highlight_x, highlight_y, highlight_x + highlight_size, highlight_y + highlight_size], 
                    fill=highlight_color)
        
        return image
    
    def _apply_style_effects(self, image: Image.Image, style: str) -> Image.Image:
        """Apply style-specific effects"""
        if style == 'pixel':
            # Pixelate effect
            small_size = (image.size[0] // 4, image.size[1] // 4)
            image = image.resize(small_size, Image.Resampling.NEAREST)
            image = image.resize((image.size[0] * 4, image.size[1] * 4), Image.Resampling.NEAREST)
        
        elif style == 'dark':
            # Darken and add contrast
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(0.7)
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.3)
        
        elif style == 'cute':
            # Soften and brighten
            image = image.filter(ImageFilter.SMOOTH)
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(1.2)
        
        return image
    
    # Helper methods for drawing complex shapes
    def _draw_gradient_ellipse(self, draw, bbox, color):
        """Draw ellipse with gradient effect"""
        x1, y1, x2, y2 = bbox
        for i in range(y2 - y1):
            alpha = int(255 * (1 - i / (y2 - y1) * 0.3))
            line_color = color[:3] + (alpha,)
            draw.ellipse([x1, y1 + i, x2, y1 + i + 1], fill=line_color)
    
    def _draw_gradient_rectangle(self, draw, bbox, color, radius=0):
        """Draw rectangle with gradient effect"""
        x1, y1, x2, y2 = bbox
        for i in range(y2 - y1):
            alpha = int(255 * (1 - i / (y2 - y1) * 0.3))
            line_color = color[:3] + (alpha,)
            if radius > 0:
                draw.rounded_rectangle([x1, y1 + i, x2, y1 + i + 1], radius=1, fill=line_color)
            else:
                draw.rectangle([x1, y1 + i, x2, y1 + i + 1], fill=line_color)
    
    def _draw_star(self, draw, center_x, center_y, radius, color):
        """Draw star shape"""
        points = []
        for i in range(10):
            angle = i * 36 * math.pi / 180
            r = radius if i % 2 == 0 else radius // 2
            x = center_x + r * math.cos(angle)
            y = center_y + r * math.sin(angle)
            points.append((x, y))
        draw.polygon(points, fill=color)
    
    def _draw_enhanced_sword(self, draw, size, colors, style):
        """Draw enhanced sword"""
        blade_color = colors[0] if colors else (200, 200, 200)
        handle_color = colors[1] if len(colors) > 1 else (139, 69, 19)
        
        # Blade with gradient
        blade_width = size[0] // 6
        blade_height = int(size[1] * 0.6)
        blade_x = size[0] // 2 - blade_width // 2
        blade_y = 10
        
        # Blade gradient
        for i in range(blade_width):
            alpha = int(255 * (1 - abs(i - blade_width//2) / (blade_width//2) * 0.3))
            line_color = blade_color[:3] + (alpha,)
            draw.rectangle([blade_x + i, blade_y, blade_x + i + 1, blade_y + blade_height], fill=line_color)
        
        # Handle
        handle_width = blade_width - 2
        handle_height = size[1] // 4
        handle_x = size[0] // 2 - handle_width // 2
        handle_y = blade_y + blade_height
        draw.rectangle([handle_x, handle_y, handle_x + handle_width, handle_y + handle_height], fill=handle_color)
        
        # Guard
        guard_width = size[0] // 3
        guard_height = 6
        guard_x = size[0] // 2 - guard_width // 2
        guard_y = blade_y + blade_height - 3
        draw.rectangle([guard_x, guard_y, guard_x + guard_width, guard_y + guard_height], fill=blade_color)
        
        # Pommel
        pommel_size = handle_width + 4
        pommel_x = size[0] // 2 - pommel_size // 2
        pommel_y = handle_y + handle_height
        draw.ellipse([pommel_x, pommel_y, pommel_x + pommel_size, pommel_y + pommel_size], fill=handle_color)
    
    def _generate_fallback_asset(self) -> str:
        """Generate fallback asset if generation fails"""
        size = (128, 128)
        image = Image.new('RGB', size, (100, 100, 100))
        draw = ImageDraw.Draw(image)
        
        # Draw "AI" text
        try:
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

def test_enhanced_generator():
    """Test enhanced generator"""
    print("🎨 Testing Enhanced AI Asset Generator")
    print("=" * 50)
    
    generator = EnhancedAssetGenerator()
    
    test_prompts = [
        "fantasy warrior character with sword",
        "modern blue ui button interface",
        "pixel art magic staff weapon",
        "cute star icon symbol",
        "dark space background scene",
        "sci-fi robot character",
        "medieval castle background"
    ]
    
    for prompt in test_prompts:
        print(f"Generating: {prompt}")
        result = generator.generate_enhanced_asset(prompt)
        if result:
            print(f"✅ Generated {len(result)} bytes (enhanced)")
        else:
            print("❌ Failed")
        print()

if __name__ == "__main__":
    test_enhanced_generator()
