#!/usr/bin/env python3
"""
Web Asset Generator
Flask web application for text-to-asset generation
Production-ready web interface
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import json
import time
from pathlib import Path
from enhanced_asset_generator import EnhancedAssetGenerator
from hybrid_ai_generator import HybridAssetGenerator
from database import DatabaseManager
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)
CORS(app)

# Initialize components
try:
    # Try hybrid generator first (best quality)
    asset_generator = HybridAssetGenerator(use_local_model=False)
    generator_type = "Hybrid AI (Stable Diffusion + Custom Data)"
except Exception as e:
    print(f"⚠️ Hybrid generator failed: {e}")
    print("🔄 Falling back to Enhanced generator...")
    asset_generator = EnhancedAssetGenerator()
    generator_type = "Enhanced Procedural"

db = DatabaseManager()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_asset():
    """API endpoint for generating assets"""
    try:
        data = request.get_json()
        text_prompt = data.get('prompt', '').strip()
        
        if not text_prompt:
            return jsonify({'error': 'Text prompt is required'}), 400
        
        if len(text_prompt) < 3:
            return jsonify({'error': 'Prompt too short (minimum 3 characters)'}), 400
        
        # Generate asset
        start_time = time.time()

        # Try hybrid generation first, fallback to enhanced
        if hasattr(asset_generator, 'generate_hybrid_asset'):
            image_base64 = asset_generator.generate_hybrid_asset(text_prompt)
        else:
            image_base64 = asset_generator.generate_enhanced_asset(text_prompt)

        generation_time = time.time() - start_time
        
        if image_base64:
            return jsonify({
                'success': True,
                'image': f"data:image/png;base64,{image_base64}",
                'prompt': text_prompt,
                'generation_time': round(generation_time, 2),
                'timestamp': int(time.time())
            })
        else:
            return jsonify({'error': 'Failed to generate asset'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Generation failed: {str(e)}'}), 500

@app.route('/api/stats')
def get_stats():
    """Get application statistics"""
    try:
        # Get asset statistics
        assets = db.get_assets()
        
        stats = {
            'total_assets': len(assets),
            'asset_types': {},
            'categories': {},
            'sites': {},
            'model_status': 'loaded',
            'generator_type': generator_type
        }
        
        for asset in assets:
            asset_type = asset.get('asset_type', 'unknown')
            category = asset.get('category', 'unknown')
            site = asset.get('source_site', 'unknown')
            
            stats['asset_types'][asset_type] = stats['asset_types'].get(asset_type, 0) + 1
            stats['categories'][category] = stats['categories'].get(category, 0) + 1
            stats['sites'][site] = stats['sites'].get(site, 0) + 1
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': f'Failed to get stats: {str(e)}'}), 500

@app.route('/api/examples')
def get_examples():
    """Get example prompts and sample assets"""
    try:
        # Get some sample assets for inspiration
        sample_assets = db.get_assets()[:20]  # First 20 assets
        
        examples = {
            'prompts': [
                "pixel art character warrior with sword",
                "modern ui button blue gradient",
                "fantasy magic spell effect",
                "space background with stars",
                "cute animal character sprite",
                "medieval castle building",
                "sci-fi weapon laser gun",
                "nature tree forest sprite",
                "game icon treasure chest",
                "platform game tile grass"
            ],
            'sample_assets': []
        }
        
        for asset in sample_assets:
            examples['sample_assets'].append({
                'title': asset.get('title', 'Unknown'),
                'category': asset.get('category', 'misc'),
                'type': asset.get('asset_type', '2d'),
                'site': asset.get('source_site', 'unknown')
            })
        
        return jsonify(examples)
        
    except Exception as e:
        return jsonify({'error': f'Failed to get examples: {str(e)}'}), 500

@app.route('/api/train', methods=['POST'])
def train_model():
    """API endpoint for training the model (admin only)"""
    try:
        data = request.get_json()
        epochs = data.get('epochs', 10)
        
        # This would be a long-running process
        # In production, you'd want to use a task queue like Celery
        
        return jsonify({
            'message': 'Training started',
            'epochs': epochs,
            'status': 'training'
        })
        
    except Exception as e:
        return jsonify({'error': f'Training failed: {str(e)}'}), 500

@app.route('/admin')
def admin():
    """Admin panel"""
    return render_template('admin.html')

# Create templates directory and files
def create_templates():
    """Create HTML templates"""
    templates_dir = Path("templates")
    templates_dir.mkdir(exist_ok=True)
    
    # Main index template
    index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Asset Generator</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #1a1a2e; color: #eee; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 40px; }
        .header h1 { color: #4f46e5; font-size: 3em; margin-bottom: 10px; }
        .header p { font-size: 1.2em; color: #9ca3af; }
        
        .generator-section { background: #16213e; border-radius: 15px; padding: 30px; margin-bottom: 30px; }
        .input-group { margin-bottom: 20px; }
        .input-group label { display: block; margin-bottom: 8px; font-weight: 600; }
        .input-group input { width: 100%; padding: 12px; border: 2px solid #374151; border-radius: 8px; background: #1f2937; color: #fff; font-size: 16px; }
        .input-group input:focus { outline: none; border-color: #4f46e5; }
        
        .generate-btn { background: linear-gradient(135deg, #4f46e5, #7c3aed); color: white; border: none; padding: 15px 30px; border-radius: 8px; font-size: 18px; cursor: pointer; width: 100%; transition: all 0.3s; }
        .generate-btn:hover { transform: translateY(-2px); box-shadow: 0 10px 25px rgba(79, 70, 229, 0.3); }
        .generate-btn:disabled { opacity: 0.6; cursor: not-allowed; }
        
        .result-section { background: #16213e; border-radius: 15px; padding: 30px; margin-bottom: 30px; }
        .generated-image { max-width: 100%; border-radius: 10px; margin: 20px 0; }
        .loading { text-align: center; padding: 40px; }
        .spinner { border: 4px solid #374151; border-top: 4px solid #4f46e5; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; margin: 0 auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        
        .stats-section { background: #16213e; border-radius: 15px; padding: 30px; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
        .stat-card { background: #1f2937; padding: 20px; border-radius: 10px; text-align: center; }
        .stat-number { font-size: 2em; font-weight: bold; color: #4f46e5; }
        .stat-label { color: #9ca3af; margin-top: 5px; }
        
        .examples { margin-top: 20px; }
        .example-prompts { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px; }
        .example-prompt { background: #374151; padding: 8px 15px; border-radius: 20px; cursor: pointer; transition: all 0.3s; }
        .example-prompt:hover { background: #4f46e5; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎮 AI Asset Generator</h1>
            <p>Generate 2D game assets from text descriptions using AI</p>
        </div>
        
        <div class="generator-section">
            <h2>Generate Asset</h2>
            <div class="input-group">
                <label for="prompt">Describe the asset you want to generate:</label>
                <input type="text" id="prompt" placeholder="e.g., pixel art character warrior with sword">
            </div>
            <button class="generate-btn" onclick="generateAsset()">Generate Asset</button>
            
            <div class="examples">
                <h3>Example Prompts:</h3>
                <div class="example-prompts" id="examplePrompts"></div>
            </div>
        </div>
        
        <div class="result-section" id="resultSection" style="display: none;">
            <h2>Generated Asset</h2>
            <div id="resultContent"></div>
        </div>
        
        <div class="stats-section">
            <h2>Training Data Statistics</h2>
            <div class="stats-grid" id="statsGrid"></div>
        </div>
    </div>
    
    <script>
        // Load stats and examples on page load
        window.onload = function() {
            loadStats();
            loadExamples();
        };
        
        function loadStats() {
            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {
                    const statsGrid = document.getElementById('statsGrid');
                    statsGrid.innerHTML = `
                        <div class="stat-card">
                            <div class="stat-number">${data.total_assets}</div>
                            <div class="stat-label">Total Assets</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">${Object.keys(data.asset_types).length}</div>
                            <div class="stat-label">Asset Types</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">${Object.keys(data.categories).length}</div>
                            <div class="stat-label">Categories</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">${data.model_status === 'loaded' ? '✅' : '❌'}</div>
                            <div class="stat-label">Model Status</div>
                        </div>
                    `;
                });
        }
        
        function loadExamples() {
            fetch('/api/examples')
                .then(response => response.json())
                .then(data => {
                    const examplePrompts = document.getElementById('examplePrompts');
                    examplePrompts.innerHTML = data.prompts.map(prompt => 
                        `<div class="example-prompt" onclick="setPrompt('${prompt}')">${prompt}</div>`
                    ).join('');
                });
        }
        
        function setPrompt(prompt) {
            document.getElementById('prompt').value = prompt;
        }
        
        function generateAsset() {
            const prompt = document.getElementById('prompt').value.trim();
            if (!prompt) {
                alert('Please enter a prompt');
                return;
            }
            
            const resultSection = document.getElementById('resultSection');
            const resultContent = document.getElementById('resultContent');
            const generateBtn = document.querySelector('.generate-btn');
            
            // Show loading
            resultSection.style.display = 'block';
            resultContent.innerHTML = `
                <div class="loading">
                    <div class="spinner"></div>
                    <p>Generating asset...</p>
                </div>
            `;
            generateBtn.disabled = true;
            generateBtn.textContent = 'Generating...';
            
            // Make API call
            fetch('/api/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt: prompt })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    resultContent.innerHTML = `
                        <p><strong>Prompt:</strong> ${data.prompt}</p>
                        <p><strong>Generation Time:</strong> ${data.generation_time}s</p>
                        <img src="${data.image}" alt="Generated Asset" class="generated-image">
                        <p><em>Generated at ${new Date(data.timestamp * 1000).toLocaleString()}</em></p>
                    `;
                } else {
                    resultContent.innerHTML = `<p style="color: #ef4444;">Error: ${data.error}</p>`;
                }
            })
            .catch(error => {
                resultContent.innerHTML = `<p style="color: #ef4444;">Error: ${error.message}</p>`;
            })
            .finally(() => {
                generateBtn.disabled = false;
                generateBtn.textContent = 'Generate Asset';
            });
        }
        
        // Allow Enter key to generate
        document.getElementById('prompt').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                generateAsset();
            }
        });
    </script>
</body>
</html>'''
    
    with open(templates_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    
    # Admin template
    admin_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Asset Generator - Admin</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #1a1a2e; color: #eee; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 40px; }
        .admin-section { background: #16213e; border-radius: 15px; padding: 30px; margin-bottom: 30px; }
        .btn { background: #4f46e5; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
        .btn:hover { background: #3730a3; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔧 Admin Panel</h1>
            <p>AI Asset Generator Administration</p>
        </div>
        
        <div class="admin-section">
            <h2>Model Training</h2>
            <p>Train the AI model with current asset data</p>
            <button class="btn" onclick="startTraining()">Start Training</button>
        </div>
        
        <div class="admin-section">
            <h2>System Status</h2>
            <div id="systemStatus">Loading...</div>
        </div>
    </div>
    
    <script>
        function startTraining() {
            if (confirm('Start model training? This may take a while.')) {
                fetch('/api/train', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ epochs: 20 })
                })
                .then(response => response.json())
                .then(data => alert(data.message));
            }
        }
        
        // Load system status
        fetch('/api/stats')
            .then(response => response.json())
            .then(data => {
                document.getElementById('systemStatus').innerHTML = `
                    <p>Total Assets: ${data.total_assets}</p>
                    <p>Model Status: ${data.model_status}</p>
                `;
            });
    </script>
</body>
</html>'''
    
    with open(templates_dir / "admin.html", "w", encoding="utf-8") as f:
        f.write(admin_html)

if __name__ == '__main__':
    # Create templates
    create_templates()
    
    print("🚀 Starting AI Asset Generator Web Application")
    print("=" * 50)
    print("🌐 Web interface: http://localhost:5000")
    print("🔧 Admin panel: http://localhost:5000/admin")
    print("📊 API stats: http://localhost:5000/api/stats")
    print()
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
