#!/usr/bin/env python3
"""
AI Asset Generator
Text-to-Asset AI model training and generation system
Web-ready implementation for generating 2D game assets
"""

import os
import json
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple
import sqlite3
from database import DatabaseManager
import requests
from io import BytesIO
import base64

class AssetDataset(Dataset):
    """Dataset class for training AI model with our scraped assets"""
    
    def __init__(self, assets_data: List[Dict], transform=None, max_size=512):
        self.assets_data = assets_data
        self.transform = transform
        self.max_size = max_size
        
        # Text preprocessing
        self.vocab = self._build_vocabulary()
        self.max_text_length = 50
        
    def _build_vocabulary(self):
        """Build vocabulary from asset titles and descriptions"""
        vocab = {'<PAD>': 0, '<UNK>': 1, '<START>': 2, '<END>': 3}
        word_count = {}
        
        for asset in self.assets_data:
            text = f"{asset.get('title', '')} {asset.get('description', '')} {asset.get('category', '')}"
            words = text.lower().split()
            
            for word in words:
                word_count[word] = word_count.get(word, 0) + 1
        
        # Add words that appear at least 2 times
        for word, count in word_count.items():
            if count >= 2 and word not in vocab:
                vocab[word] = len(vocab)
        
        return vocab
    
    def _text_to_tensor(self, text: str) -> torch.Tensor:
        """Convert text to tensor"""
        words = text.lower().split()
        indices = [self.vocab.get('<START>')]
        
        for word in words[:self.max_text_length-2]:
            indices.append(self.vocab.get(word, self.vocab['<UNK>']))
        
        indices.append(self.vocab.get('<END>'))
        
        # Pad to max length
        while len(indices) < self.max_text_length:
            indices.append(self.vocab.get('<PAD>'))
        
        return torch.tensor(indices[:self.max_text_length])
    
    def _load_image(self, asset: Dict) -> Image.Image:
        """Load image from asset data"""
        try:
            # Try to load from local downloads first
            local_path = self._get_local_path(asset)
            if local_path and local_path.exists():
                return Image.open(local_path).convert('RGB')
            
            # Fallback to preview URL
            preview_url = asset.get('preview_url')
            if preview_url:
                response = requests.get(preview_url, timeout=10)
                return Image.open(BytesIO(response.content)).convert('RGB')
            
            # Create placeholder image
            return Image.new('RGB', (256, 256), color='white')
            
        except Exception as e:
            print(f"Error loading image for {asset.get('title', 'unknown')}: {e}")
            return Image.new('RGB', (256, 256), color='white')
    
    def _get_local_path(self, asset: Dict) -> Path:
        """Get local file path for asset"""
        downloads_dir = Path("downloads")
        site = asset.get('source_site', 'unknown')
        category = asset.get('category', 'other')
        title = asset.get('title', 'unknown')
        
        # Clean filename
        clean_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
        
        possible_paths = [
            downloads_dir / site / category / f"{clean_title}.png",
            downloads_dir / site / category / f"{clean_title}.jpg",
            downloads_dir / site / category / f"{clean_title}.jpeg",
            downloads_dir / site / f"{clean_title}.png",
            downloads_dir / site / f"{clean_title}.jpg",
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        
        return None
    
    def __len__(self):
        return len(self.assets_data)
    
    def __getitem__(self, idx):
        asset = self.assets_data[idx]
        
        # Load and process image
        image = self._load_image(asset)
        if self.transform:
            image = self.transform(image)
        
        # Process text
        text = f"{asset.get('title', '')} {asset.get('description', '')} {asset.get('category', '')}"
        text_tensor = self._text_to_tensor(text)
        
        return {
            'image': image,
            'text': text_tensor,
            'category': asset.get('category', 'misc'),
            'asset_type': asset.get('asset_type', '2d')
        }

class TextToAssetGenerator(nn.Module):
    """Neural network for generating assets from text descriptions"""
    
    def __init__(self, vocab_size: int, embed_dim: int = 256, hidden_dim: int = 512):
        super().__init__()
        
        # Text encoder
        self.text_embedding = nn.Embedding(vocab_size, embed_dim)
        self.text_lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True)
        self.text_fc = nn.Linear(hidden_dim, 256)
        
        # Image generator (simplified GAN-like structure)
        self.generator = nn.Sequential(
            nn.Linear(256, 512),
            nn.ReLU(),
            nn.Linear(512, 1024),
            nn.ReLU(),
            nn.Linear(1024, 2048),
            nn.ReLU(),
            nn.Linear(2048, 256 * 256 * 3),  # 256x256 RGB image
            nn.Tanh()
        )
        
    def forward(self, text_input):
        # Encode text
        embedded = self.text_embedding(text_input)
        lstm_out, (hidden, _) = self.text_lstm(embedded)
        text_features = self.text_fc(hidden[-1])
        
        # Generate image
        generated_image = self.generator(text_features)
        generated_image = generated_image.view(-1, 3, 256, 256)
        
        return generated_image

class AIAssetTrainer:
    """Main trainer class for the AI asset generation model"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")
        
        # Data transforms
        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])
        
    def prepare_dataset(self) -> AssetDataset:
        """Prepare dataset from scraped assets"""
        print("📊 Preparing dataset from scraped assets...")
        
        # Get 2D assets only (best for image generation)
        assets = self.db.get_assets({'asset_type': '2d'})
        print(f"Found {len(assets)} 2D assets")
        
        # Filter assets with good descriptions
        filtered_assets = []
        for asset in assets:
            title = asset.get('title', '')
            description = asset.get('description', '')
            
            if len(title) > 3 and (len(description) > 10 or asset.get('category') != 'misc'):
                filtered_assets.append(asset)
        
        print(f"Filtered to {len(filtered_assets)} assets with good descriptions")
        
        return AssetDataset(filtered_assets, transform=self.transform)
    
    def train_model(self, epochs: int = 50, batch_size: int = 8, learning_rate: float = 0.001):
        """Train the AI model"""
        print("🚀 Starting AI model training...")
        
        # Prepare dataset
        dataset = self.prepare_dataset()
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        # Initialize model
        vocab_size = len(dataset.vocab)
        model = TextToAssetGenerator(vocab_size).to(self.device)
        
        # Loss and optimizer
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=learning_rate)
        
        print(f"Model initialized with vocab size: {vocab_size}")
        print(f"Training on {len(dataset)} samples for {epochs} epochs")
        
        # Training loop
        model.train()
        for epoch in range(epochs):
            total_loss = 0
            batch_count = 0
            
            for batch in dataloader:
                text_input = batch['text'].to(self.device)
                real_images = batch['image'].to(self.device)
                
                # Forward pass
                optimizer.zero_grad()
                generated_images = model(text_input)
                
                # Calculate loss
                loss = criterion(generated_images, real_images)
                
                # Backward pass
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
                batch_count += 1
            
            avg_loss = total_loss / batch_count
            print(f"Epoch [{epoch+1}/{epochs}], Loss: {avg_loss:.4f}")
            
            # Save model checkpoint every 10 epochs
            if (epoch + 1) % 10 == 0:
                self.save_model(model, dataset.vocab, f"model_epoch_{epoch+1}.pth")
        
        # Save final model
        self.save_model(model, dataset.vocab, "final_model.pth")
        print("✅ Training completed!")
        
        return model, dataset.vocab
    
    def save_model(self, model: nn.Module, vocab: Dict, filename: str):
        """Save trained model and vocabulary"""
        model_dir = Path("ai_models")
        model_dir.mkdir(exist_ok=True)
        
        torch.save({
            'model_state_dict': model.state_dict(),
            'vocab': vocab,
            'model_config': {
                'vocab_size': len(vocab),
                'embed_dim': 256,
                'hidden_dim': 512
            }
        }, model_dir / filename)
        
        print(f"Model saved: {model_dir / filename}")

class WebAssetGenerator:
    """Web-ready asset generator for production use"""
    
    def __init__(self, model_path: str = "ai_models/final_model.pth"):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model_path = Path(model_path)
        
        if self.model_path.exists():
            self.load_model()
        else:
            print("⚠️ No trained model found. Please train the model first.")
            self.model = None
            self.vocab = None
    
    def load_model(self):
        """Load trained model for inference"""
        checkpoint = torch.load(self.model_path, map_location=self.device)
        
        self.vocab = checkpoint['vocab']
        config = checkpoint['model_config']
        
        self.model = TextToAssetGenerator(
            vocab_size=config['vocab_size'],
            embed_dim=config['embed_dim'],
            hidden_dim=config['hidden_dim']
        ).to(self.device)
        
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model.eval()
        
        print(f"✅ Model loaded from {self.model_path}")
    
    def generate_asset(self, text_prompt: str) -> str:
        """Generate asset from text prompt and return as base64"""
        if not self.model or not self.vocab:
            return None
        
        # Preprocess text
        text_tensor = self._text_to_tensor(text_prompt).unsqueeze(0).to(self.device)
        
        # Generate image
        with torch.no_grad():
            generated_image = self.model(text_tensor)
            
            # Convert to PIL Image
            image_np = generated_image.squeeze().cpu().numpy()
            image_np = (image_np + 1) / 2  # Denormalize from [-1, 1] to [0, 1]
            image_np = np.transpose(image_np, (1, 2, 0))
            image_np = (image_np * 255).astype(np.uint8)
            
            image = Image.fromarray(image_np)
            
            # Convert to base64 for web
            buffer = BytesIO()
            image.save(buffer, format='PNG')
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            return image_base64
    
    def _text_to_tensor(self, text: str, max_length: int = 50) -> torch.Tensor:
        """Convert text to tensor using loaded vocabulary"""
        words = text.lower().split()
        indices = [self.vocab.get('<START>', 2)]
        
        for word in words[:max_length-2]:
            indices.append(self.vocab.get(word, self.vocab.get('<UNK>', 1)))
        
        indices.append(self.vocab.get('<END>', 3))
        
        # Pad to max length
        while len(indices) < max_length:
            indices.append(self.vocab.get('<PAD>', 0))
        
        return torch.tensor(indices[:max_length])

def main():
    """Main function for training or testing"""
    print("🎮 AI Asset Generator")
    print("=" * 50)
    
    trainer = AIAssetTrainer()
    
    print("1. Train new model")
    print("2. Test existing model")
    choice = input("Select option (1 or 2): ").strip()
    
    if choice == "1":
        print("🚀 Starting model training...")
        model, vocab = trainer.train_model(epochs=20, batch_size=4)
        print("✅ Training completed!")
        
    elif choice == "2":
        print("🧪 Testing existing model...")
        generator = WebAssetGenerator()
        
        if generator.model:
            test_prompts = [
                "pixel art character warrior",
                "ui button blue modern",
                "fantasy sword weapon",
                "space background stars",
                "cute animal sprite"
            ]
            
            for prompt in test_prompts:
                print(f"Generating: {prompt}")
                result = generator.generate_asset(prompt)
                if result:
                    print(f"✅ Generated asset for: {prompt}")
                else:
                    print(f"❌ Failed to generate: {prompt}")
        else:
            print("❌ No model available for testing")

if __name__ == "__main__":
    main()
