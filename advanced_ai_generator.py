#!/usr/bin/env python3
"""
Advanced AI Asset Generator
Real neural network-based asset generation using our scraped data
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import json
import requests
from pathlib import Path
from database import DatabaseManager
import base64
from io import BytesIO
import random
import os

class StyleGAN_Generator(nn.Module):
    """Simplified StyleGAN-like generator for asset creation"""
    
    def __init__(self, latent_dim=100, text_embed_dim=256, img_size=128):
        super().__init__()
        self.img_size = img_size
        self.latent_dim = latent_dim
        
        # Text encoder
        self.text_encoder = nn.Sequential(
            nn.Linear(text_embed_dim, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, latent_dim)
        )
        
        # Generator network
        self.generator = nn.Sequential(
            # Input: latent_dim
            nn.Linear(latent_dim, 256 * 8 * 8),
            nn.ReLU(),
            
            # Reshape to feature maps
            nn.Unflatten(1, (256, 8, 8)),
            
            # Upsampling layers
            nn.ConvTranspose2d(256, 128, 4, 2, 1),  # 8x8 -> 16x16
            nn.BatchNorm2d(128),
            nn.ReLU(),
            
            nn.ConvTranspose2d(128, 64, 4, 2, 1),   # 16x16 -> 32x32
            nn.BatchNorm2d(64),
            nn.ReLU(),
            
            nn.ConvTranspose2d(64, 32, 4, 2, 1),    # 32x32 -> 64x64
            nn.BatchNorm2d(32),
            nn.ReLU(),
            
            nn.ConvTranspose2d(32, 16, 4, 2, 1),    # 64x64 -> 128x128
            nn.BatchNorm2d(16),
            nn.ReLU(),
            
            # Final layer
            nn.Conv2d(16, 4, 3, 1, 1),              # RGBA output
            nn.Tanh()
        )
        
    def forward(self, noise, text_embedding):
        # Combine noise with text
        text_features = self.text_encoder(text_embedding)
        combined = noise + text_features
        
        # Generate image
        img = self.generator(combined)
        return img

class AssetDiscriminator(nn.Module):
    """Discriminator for GAN training"""
    
    def __init__(self, img_size=128):
        super().__init__()
        
        self.discriminator = nn.Sequential(
            # Input: 4 x 128 x 128 (RGBA)
            nn.Conv2d(4, 16, 4, 2, 1),              # 128x128 -> 64x64
            nn.LeakyReLU(0.2),
            
            nn.Conv2d(16, 32, 4, 2, 1),             # 64x64 -> 32x32
            nn.BatchNorm2d(32),
            nn.LeakyReLU(0.2),
            
            nn.Conv2d(32, 64, 4, 2, 1),             # 32x32 -> 16x16
            nn.BatchNorm2d(64),
            nn.LeakyReLU(0.2),
            
            nn.Conv2d(64, 128, 4, 2, 1),            # 16x16 -> 8x8
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2),
            
            nn.Conv2d(128, 256, 4, 2, 1),           # 8x8 -> 4x4
            nn.BatchNorm2d(256),
            nn.LeakyReLU(0.2),
            
            # Flatten and classify
            nn.Flatten(),
            nn.Linear(256 * 4 * 4, 1),
            nn.Sigmoid()
        )
        
    def forward(self, img):
        return self.discriminator(img)

class RealAssetDataset(Dataset):
    """Dataset using our real scraped assets"""
    
    def __init__(self, db_manager, transform=None, max_samples=1000):
        self.db = db_manager
        self.transform = transform
        self.assets = self._load_assets(max_samples)
        self.vocab = self._build_vocab()
        
    def _load_assets(self, max_samples):
        """Load assets from database"""
        assets = self.db.get_assets({'asset_type': '2d'})
        
        # Filter assets with good descriptions and available images
        filtered_assets = []
        for asset in assets[:max_samples]:
            title = asset.get('title', '')
            description = asset.get('description', '')
            preview_url = asset.get('preview_url', '')
            
            if len(title) > 3 and (preview_url or self._has_local_file(asset)):
                filtered_assets.append(asset)
        
        print(f"Loaded {len(filtered_assets)} assets for training")
        return filtered_assets
    
    def _has_local_file(self, asset):
        """Check if asset has local file"""
        downloads_dir = Path("downloads")
        site = asset.get('source_site', 'unknown')
        category = asset.get('category', 'other')
        title = asset.get('title', 'unknown')
        
        clean_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
        
        possible_paths = [
            downloads_dir / site / category / f"{clean_title}.png",
            downloads_dir / site / category / f"{clean_title}.jpg",
            downloads_dir / site / f"{clean_title}.png",
        ]
        
        return any(path.exists() for path in possible_paths)
    
    def _build_vocab(self):
        """Build vocabulary from asset descriptions"""
        vocab = {'<PAD>': 0, '<UNK>': 1}
        word_count = {}
        
        for asset in self.assets:
            text = f"{asset.get('title', '')} {asset.get('description', '')} {asset.get('category', '')}"
            words = text.lower().split()
            
            for word in words:
                if word.isalpha():  # Only alphabetic words
                    word_count[word] = word_count.get(word, 0) + 1
        
        # Add frequent words to vocabulary
        for word, count in word_count.items():
            if count >= 2 and word not in vocab:
                vocab[word] = len(vocab)
        
        return vocab
    
    def _text_to_embedding(self, text, max_length=50):
        """Convert text to embedding vector"""
        words = text.lower().split()
        indices = []
        
        for word in words[:max_length]:
            if word.isalpha():
                indices.append(self.vocab.get(word, self.vocab['<UNK>']))
        
        # Pad or truncate to fixed length
        while len(indices) < max_length:
            indices.append(self.vocab['<PAD>'])
        
        indices = indices[:max_length]
        
        # Convert to embedding (simple one-hot average)
        embedding = torch.zeros(256)
        for idx in indices:
            if idx < 256:  # Limit to embedding dimension
                embedding[idx] = 1.0
        
        return embedding / (len(indices) + 1e-8)  # Normalize
    
    def _load_image(self, asset):
        """Load image from asset"""
        try:
            # Try local file first
            local_path = self._get_local_path(asset)
            if local_path and local_path.exists():
                img = Image.open(local_path).convert('RGBA')
            else:
                # Try preview URL
                preview_url = asset.get('preview_url')
                if preview_url:
                    response = requests.get(preview_url, timeout=10)
                    img = Image.open(BytesIO(response.content)).convert('RGBA')
                else:
                    # Create synthetic image based on description
                    img = self._create_synthetic_image(asset)
            
            # Resize to standard size
            img = img.resize((128, 128), Image.Resampling.LANCZOS)
            return img
            
        except Exception as e:
            print(f"Error loading image for {asset.get('title', 'unknown')}: {e}")
            return self._create_synthetic_image(asset)
    
    def _get_local_path(self, asset):
        """Get local file path"""
        downloads_dir = Path("downloads")
        site = asset.get('source_site', 'unknown')
        category = asset.get('category', 'other')
        title = asset.get('title', 'unknown')
        
        clean_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
        
        possible_paths = [
            downloads_dir / site / category / f"{clean_title}.png",
            downloads_dir / site / category / f"{clean_title}.jpg",
            downloads_dir / site / f"{clean_title}.png",
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        return None
    
    def _create_synthetic_image(self, asset):
        """Create synthetic training image based on asset metadata"""
        img = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Determine colors based on category
        category = asset.get('category', 'misc').lower()
        if 'character' in category:
            colors = [(255, 200, 150), (100, 150, 255)]  # Skin, clothing
        elif 'ui' in category:
            colors = [(100, 150, 255), (255, 255, 255)]  # Blue, white
        elif 'weapon' in category:
            colors = [(200, 200, 200), (139, 69, 19)]    # Metal, wood
        elif 'icon' in category:
            colors = [(255, 200, 100), (255, 255, 255)]  # Gold, white
        else:
            colors = [(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))]
        
        # Draw based on category
        if 'character' in category:
            self._draw_character(draw, colors)
        elif 'ui' in category:
            self._draw_ui_element(draw, colors)
        elif 'weapon' in category:
            self._draw_weapon(draw, colors)
        elif 'icon' in category:
            self._draw_icon(draw, colors)
        else:
            self._draw_generic(draw, colors)
        
        return img
    
    def _draw_character(self, draw, colors):
        """Draw character-like shape"""
        color1, color2 = colors[0], colors[1] if len(colors) > 1 else colors[0]
        
        # Head
        draw.ellipse([48, 20, 80, 52], fill=color1)
        # Body
        draw.rectangle([56, 52, 72, 90], fill=color2)
        # Arms
        draw.rectangle([40, 60, 56, 85], fill=color1)
        draw.rectangle([72, 60, 88, 85], fill=color1)
        # Legs
        draw.rectangle([58, 90, 66, 115], fill=color1)
        draw.rectangle([70, 90, 78, 115], fill=color1)
    
    def _draw_ui_element(self, draw, colors):
        """Draw UI element"""
        color1 = colors[0]
        draw.rounded_rectangle([20, 40, 108, 88], radius=8, fill=color1)
        draw.rounded_rectangle([20, 40, 108, 88], radius=8, outline=(255, 255, 255), width=2)
    
    def _draw_weapon(self, draw, colors):
        """Draw weapon"""
        color1, color2 = colors[0], colors[1] if len(colors) > 1 else colors[0]
        # Blade
        draw.rectangle([60, 20, 68, 80], fill=color1)
        # Handle
        draw.rectangle([62, 80, 66, 100], fill=color2)
        # Guard
        draw.rectangle([50, 78, 78, 82], fill=color1)
    
    def _draw_icon(self, draw, colors):
        """Draw icon"""
        color1 = colors[0]
        # Star shape
        points = []
        center_x, center_y = 64, 64
        for i in range(10):
            angle = i * 36 * 3.14159 / 180
            radius = 25 if i % 2 == 0 else 12
            x = center_x + radius * np.cos(angle)
            y = center_y + radius * np.sin(angle)
            points.append((x, y))
        draw.polygon(points, fill=color1)
    
    def _draw_generic(self, draw, colors):
        """Draw generic shape"""
        color1 = colors[0]
        draw.ellipse([32, 32, 96, 96], fill=color1)
    
    def __len__(self):
        return len(self.assets)
    
    def __getitem__(self, idx):
        asset = self.assets[idx]
        
        # Load image
        image = self._load_image(asset)
        if self.transform:
            image = self.transform(image)
        
        # Get text embedding
        text = f"{asset.get('title', '')} {asset.get('description', '')} {asset.get('category', '')}"
        text_embedding = self._text_to_embedding(text)
        
        return {
            'image': image,
            'text_embedding': text_embedding,
            'category': asset.get('category', 'misc')
        }

class AdvancedAIGenerator:
    """Advanced AI generator with real neural networks"""
    
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")
        
        self.db = DatabaseManager()
        self.generator = None
        self.discriminator = None
        
        # Image transforms
        self.transform = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5, 0.5])  # RGBA
        ])
        
    def train_model(self, epochs=50, batch_size=8, lr=0.0002):
        """Train the GAN model"""
        print("🚀 Starting Advanced AI Training...")
        
        # Prepare dataset
        dataset = RealAssetDataset(self.db, transform=self.transform)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        # Initialize models
        self.generator = StyleGAN_Generator().to(self.device)
        self.discriminator = AssetDiscriminator().to(self.device)
        
        # Optimizers
        g_optimizer = optim.Adam(self.generator.parameters(), lr=lr, betas=(0.5, 0.999))
        d_optimizer = optim.Adam(self.discriminator.parameters(), lr=lr, betas=(0.5, 0.999))
        
        # Loss function
        criterion = nn.BCELoss()
        
        print(f"Training on {len(dataset)} samples for {epochs} epochs")
        
        for epoch in range(epochs):
            g_loss_total = 0
            d_loss_total = 0
            batch_count = 0
            
            for batch in dataloader:
                real_images = batch['image'].to(self.device)
                text_embeddings = batch['text_embedding'].to(self.device)
                batch_size_actual = real_images.size(0)
                
                # Train Discriminator
                d_optimizer.zero_grad()
                
                # Real images
                real_labels = torch.ones(batch_size_actual, 1).to(self.device)
                real_output = self.discriminator(real_images)
                d_loss_real = criterion(real_output, real_labels)
                
                # Fake images
                noise = torch.randn(batch_size_actual, 100).to(self.device)
                fake_images = self.generator(noise, text_embeddings)
                fake_labels = torch.zeros(batch_size_actual, 1).to(self.device)
                fake_output = self.discriminator(fake_images.detach())
                d_loss_fake = criterion(fake_output, fake_labels)
                
                d_loss = d_loss_real + d_loss_fake
                d_loss.backward()
                d_optimizer.step()
                
                # Train Generator
                g_optimizer.zero_grad()
                
                fake_output = self.discriminator(fake_images)
                g_loss = criterion(fake_output, real_labels)  # Want discriminator to think fake is real
                g_loss.backward()
                g_optimizer.step()
                
                g_loss_total += g_loss.item()
                d_loss_total += d_loss.item()
                batch_count += 1
            
            avg_g_loss = g_loss_total / batch_count
            avg_d_loss = d_loss_total / batch_count
            
            print(f"Epoch [{epoch+1}/{epochs}] - G_Loss: {avg_g_loss:.4f}, D_Loss: {avg_d_loss:.4f}")
            
            # Save model every 10 epochs
            if (epoch + 1) % 10 == 0:
                self.save_model(f"advanced_model_epoch_{epoch+1}.pth")
        
        # Save final model
        self.save_model("advanced_model_final.pth")
        print("✅ Advanced training completed!")
    
    def save_model(self, filename):
        """Save the trained model"""
        model_dir = Path("ai_models")
        model_dir.mkdir(exist_ok=True)
        
        torch.save({
            'generator_state_dict': self.generator.state_dict(),
            'discriminator_state_dict': self.discriminator.state_dict(),
            'model_type': 'advanced_gan'
        }, model_dir / filename)
        
        print(f"Model saved: {model_dir / filename}")
    
    def load_model(self, filename="advanced_model_final.pth"):
        """Load trained model"""
        model_path = Path("ai_models") / filename
        
        if not model_path.exists():
            print(f"Model not found: {model_path}")
            return False
        
        checkpoint = torch.load(model_path, map_location=self.device)
        
        self.generator = StyleGAN_Generator().to(self.device)
        self.generator.load_state_dict(checkpoint['generator_state_dict'])
        self.generator.eval()
        
        print(f"✅ Advanced model loaded from {model_path}")
        return True
    
    def generate_asset(self, prompt):
        """Generate asset from text prompt"""
        if not self.generator:
            return None
        
        # Create text embedding (simplified)
        words = prompt.lower().split()
        text_embedding = torch.zeros(256).to(self.device)
        
        # Simple word-to-embedding mapping
        for i, word in enumerate(words[:10]):  # Max 10 words
            hash_val = hash(word) % 256
            text_embedding[hash_val] = 1.0
        
        text_embedding = text_embedding.unsqueeze(0)  # Add batch dimension
        
        # Generate noise
        noise = torch.randn(1, 100).to(self.device)
        
        # Generate image
        with torch.no_grad():
            generated_image = self.generator(noise, text_embedding)
            
            # Convert to PIL Image
            image_np = generated_image.squeeze().cpu().numpy()
            image_np = (image_np + 1) / 2  # Denormalize
            image_np = np.transpose(image_np, (1, 2, 0))
            image_np = (image_np * 255).astype(np.uint8)
            
            # Handle RGBA
            if image_np.shape[2] == 4:
                image = Image.fromarray(image_np, 'RGBA')
            else:
                image = Image.fromarray(image_np[:,:,:3], 'RGB')
            
            # Convert to base64
            buffer = BytesIO()
            image.save(buffer, format='PNG')
            return base64.b64encode(buffer.getvalue()).decode()

def main():
    """Main function"""
    print("🎮 Advanced AI Asset Generator")
    print("=" * 50)
    
    generator = AdvancedAIGenerator()
    
    print("1. Train new advanced model")
    print("2. Test existing advanced model")
    choice = input("Select option (1 or 2): ").strip()
    
    if choice == "1":
        print("🚀 Starting advanced model training...")
        generator.train_model(epochs=30, batch_size=4)
        
    elif choice == "2":
        if generator.load_model():
            test_prompts = [
                "pixel art character warrior with sword",
                "modern blue ui button interface",
                "fantasy magic staff weapon",
                "cute animal character sprite",
                "space background with stars"
            ]
            
            for prompt in test_prompts:
                print(f"Generating: {prompt}")
                result = generator.generate_asset(prompt)
                if result:
                    print(f"✅ Generated advanced asset")
                else:
                    print(f"❌ Failed to generate")

if __name__ == "__main__":
    main()
