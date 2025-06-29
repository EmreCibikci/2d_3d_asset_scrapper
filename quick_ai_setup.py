#!/usr/bin/env python3
"""
Quick AI Setup
Simplified AI model setup and training for immediate testing
"""

import os
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import random
from pathlib import Path
from database import DatabaseManager
import base64
from io import BytesIO

class SimpleAssetGenerator:
    """Simplified asset generator for quick testing"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.templates = self._load_templates()
        
    def _load_templates(self):
        """Load asset templates from database"""
        assets = self.db.get_assets({'asset_type': '2d'})
        
        templates = {
            'character': [],
            'ui': [],
            'weapon': [],
            'background': [],
            'icon': [],
            'misc': []
        }
        
        for asset in assets:
            category = asset.get('category', 'misc')
            if category in templates:
                templates[category].append({
                    'title': asset.get('title', ''),
                    'description': asset.get('description', ''),
                    'keywords': self._extract_keywords(asset)
                })
        
        return templates
    
    def _extract_keywords(self, asset):
        """Extract keywords from asset data"""
        text = f"{asset.get('title', '')} {asset.get('description', '')}"
        words = text.lower().split()
        
        # Common game asset keywords
        keywords = []
        game_keywords = [
            'pixel', 'art', 'character', 'warrior', 'sword', 'magic', 'fantasy',
            'sci-fi', 'space', 'robot', 'alien', 'medieval', 'modern', 'cute',
            'dark', 'bright', 'colorful', 'simple', 'detailed', 'small', 'large',
            'blue', 'red', 'green', 'yellow', 'purple', 'orange', 'black', 'white'
        ]
        
        for word in words:
            if word in game_keywords:
                keywords.append(word)
        
        return keywords[:5]  # Max 5 keywords
    
    def generate_simple_asset(self, prompt: str) -> str:
        """Generate a simple procedural asset based on prompt"""
        try:
            # Parse prompt for category and style
            prompt_lower = prompt.lower()
            category = self._detect_category(prompt_lower)
            colors = self._detect_colors(prompt_lower)
            style = self._detect_style(prompt_lower)
            
            # Generate image based on category
            if category == 'character':
                image = self._generate_character(colors, style)
            elif category == 'ui':
                image = self._generate_ui_element(colors, style)
            elif category == 'weapon':
                image = self._generate_weapon(colors, style)
            elif category == 'icon':
                image = self._generate_icon(colors, style)
            else:
                image = self._generate_generic(colors, style, prompt)
            
            # Convert to base64
            buffer = BytesIO()
            image.save(buffer, format='PNG')
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            return image_base64
            
        except Exception as e:
            print(f"Error generating asset: {e}")
            return self._generate_placeholder()
    
    def _detect_category(self, prompt: str) -> str:
        """Detect asset category from prompt"""
        if any(word in prompt for word in ['character', 'warrior', 'hero', 'player', 'npc']):
            return 'character'
        elif any(word in prompt for word in ['button', 'ui', 'interface', 'menu', 'panel']):
            return 'ui'
        elif any(word in prompt for word in ['sword', 'weapon', 'gun', 'bow', 'staff']):
            return 'weapon'
        elif any(word in prompt for word in ['icon', 'symbol', 'logo', 'badge']):
            return 'icon'
        else:
            return 'misc'
    
    def _detect_colors(self, prompt: str) -> list:
        """Detect colors from prompt"""
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
            'white': (240, 240, 240)
        }
        
        detected_colors = []
        for color_name, rgb in color_map.items():
            if color_name in prompt:
                detected_colors.append(rgb)
        
        # Default colors if none detected
        if not detected_colors:
            detected_colors = [(100, 150, 255), (255, 100, 100)]  # Blue and red
        
        return detected_colors
    
    def _detect_style(self, prompt: str) -> str:
        """Detect art style from prompt"""
        if 'pixel' in prompt:
            return 'pixel'
        elif any(word in prompt for word in ['modern', 'clean', 'minimal']):
            return 'modern'
        elif any(word in prompt for word in ['fantasy', 'medieval', 'magic']):
            return 'fantasy'
        elif any(word in prompt for word in ['sci-fi', 'space', 'futuristic']):
            return 'scifi'
        else:
            return 'generic'
    
    def _generate_character(self, colors, style) -> Image.Image:
        """Generate a simple character sprite"""
        size = (64, 64) if style == 'pixel' else (256, 256)
        image = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        color1 = colors[0] if colors else (100, 150, 255)
        color2 = colors[1] if len(colors) > 1 else (255, 100, 100)
        
        # Simple character shape
        # Head
        head_size = size[0] // 4
        head_x = size[0] // 2 - head_size // 2
        head_y = size[1] // 6
        draw.ellipse([head_x, head_y, head_x + head_size, head_y + head_size], fill=color1)
        
        # Body
        body_width = size[0] // 3
        body_height = size[1] // 2
        body_x = size[0] // 2 - body_width // 2
        body_y = head_y + head_size
        draw.rectangle([body_x, body_y, body_x + body_width, body_y + body_height], fill=color2)
        
        # Arms
        arm_width = size[0] // 8
        arm_height = size[1] // 3
        # Left arm
        draw.rectangle([body_x - arm_width, body_y + 5, body_x, body_y + arm_height], fill=color1)
        # Right arm
        draw.rectangle([body_x + body_width, body_y + 5, body_x + body_width + arm_width, body_y + arm_height], fill=color1)
        
        # Legs
        leg_width = size[0] // 8
        leg_height = size[1] // 4
        leg_y = body_y + body_height
        # Left leg
        draw.rectangle([body_x + 5, leg_y, body_x + 5 + leg_width, leg_y + leg_height], fill=color1)
        # Right leg
        draw.rectangle([body_x + body_width - 5 - leg_width, leg_y, body_x + body_width - 5, leg_y + leg_height], fill=color1)
        
        return image
    
    def _generate_ui_element(self, colors, style) -> Image.Image:
        """Generate a UI element"""
        size = (128, 48)
        image = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        color1 = colors[0] if colors else (100, 150, 255)
        
        # Button with gradient effect
        for i in range(size[1]):
            alpha = int(255 * (1 - i / size[1] * 0.3))
            button_color = tuple(list(color1) + [alpha])
            draw.rectangle([0, i, size[0], i + 1], fill=button_color)
        
        # Border
        draw.rectangle([0, 0, size[0] - 1, size[1] - 1], outline=(255, 255, 255, 200), width=2)
        
        return image
    
    def _generate_weapon(self, colors, style) -> Image.Image:
        """Generate a weapon sprite"""
        size = (64, 64)
        image = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        color1 = colors[0] if colors else (200, 200, 200)  # Metal color
        color2 = colors[1] if len(colors) > 1 else (139, 69, 19)  # Handle color
        
        # Simple sword
        # Blade
        blade_width = 8
        blade_height = 40
        blade_x = size[0] // 2 - blade_width // 2
        blade_y = 5
        draw.rectangle([blade_x, blade_y, blade_x + blade_width, blade_y + blade_height], fill=color1)
        
        # Handle
        handle_width = 6
        handle_height = 15
        handle_x = size[0] // 2 - handle_width // 2
        handle_y = blade_y + blade_height
        draw.rectangle([handle_x, handle_y, handle_x + handle_width, handle_y + handle_height], fill=color2)
        
        # Guard
        guard_width = 20
        guard_height = 4
        guard_x = size[0] // 2 - guard_width // 2
        guard_y = blade_y + blade_height - 2
        draw.rectangle([guard_x, guard_y, guard_x + guard_width, guard_y + guard_height], fill=color1)
        
        return image
    
    def _generate_icon(self, colors, style) -> Image.Image:
        """Generate an icon"""
        size = (48, 48)
        image = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        color1 = colors[0] if colors else (255, 200, 100)
        
        # Simple star icon
        center_x, center_y = size[0] // 2, size[1] // 2
        radius = 15
        
        # Star points
        points = []
        for i in range(10):
            angle = i * 36 * 3.14159 / 180
            if i % 2 == 0:
                r = radius
            else:
                r = radius // 2
            x = center_x + r * np.cos(angle)
            y = center_y + r * np.sin(angle)
            points.append((x, y))
        
        draw.polygon(points, fill=color1)
        
        return image
    
    def _generate_generic(self, colors, style, prompt) -> Image.Image:
        """Generate a generic asset"""
        size = (128, 128)
        image = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        color1 = colors[0] if colors else (100, 150, 255)
        
        # Simple geometric shape
        shape_size = 60
        x = (size[0] - shape_size) // 2
        y = (size[1] - shape_size) // 2
        
        if 'circle' in prompt or 'round' in prompt:
            draw.ellipse([x, y, x + shape_size, y + shape_size], fill=color1)
        elif 'triangle' in prompt:
            points = [(x + shape_size // 2, y), (x, y + shape_size), (x + shape_size, y + shape_size)]
            draw.polygon(points, fill=color1)
        else:
            draw.rectangle([x, y, x + shape_size, y + shape_size], fill=color1)
        
        return image
    
    def _generate_placeholder(self) -> str:
        """Generate a placeholder image"""
        size = (128, 128)
        image = Image.new('RGB', size, (100, 100, 100))
        draw = ImageDraw.Draw(image)
        
        # Draw "?" in center
        try:
            font = ImageFont.load_default()
            text = "?"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (size[0] - text_width) // 2
            y = (size[1] - text_height) // 2
            draw.text((x, y), text, fill=(255, 255, 255), font=font)
        except:
            # Fallback if font fails
            draw.rectangle([50, 50, 78, 78], fill=(255, 255, 255))
        
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        return base64.b64encode(buffer.getvalue()).decode()

def test_simple_generator():
    """Test the simple generator"""
    print("🧪 Testing Simple AI Asset Generator")
    print("=" * 50)
    
    generator = SimpleAssetGenerator()
    
    test_prompts = [
        "pixel art character warrior",
        "blue ui button modern",
        "red sword weapon fantasy",
        "yellow star icon",
        "green circle background"
    ]
    
    for prompt in test_prompts:
        print(f"Generating: {prompt}")
        result = generator.generate_simple_asset(prompt)
        if result:
            print(f"✅ Generated {len(result)} bytes")
        else:
            print("❌ Failed")
        print()

if __name__ == "__main__":
    test_simple_generator()
