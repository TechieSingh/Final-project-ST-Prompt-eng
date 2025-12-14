"""
Simple API proxy for OpenAI requests
This allows the web page to make API calls without CORS issues
Deploy this to a service like Render, Railway, or Heroku
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/generate', methods=['POST'])
def generate_content():
    """
    Proxy endpoint for OpenAI API calls
    """
    try:
        data = request.json
        
        # Validate required fields
        if not data.get('api_key'):
            return jsonify({'error': 'API key is required'}), 400
        if not data.get('messages'):
            return jsonify({'error': 'Messages are required'}), 400
        
        # Import OpenAI client
        from openai import OpenAI
        
        # Create OpenAI client with user's API key
        client = OpenAI(api_key=data['api_key'])
        
        # Make the API call
        response = client.chat.completions.create(
            model=data.get('model', 'gpt-3.5-turbo'),
            messages=data['messages'],
            temperature=data.get('temperature', 0.7),
            max_tokens=data.get('max_tokens', 2000)
        )
        
        return jsonify({
            'content': response.choices[0].message.content,
            'model': response.model,
            'usage': {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

