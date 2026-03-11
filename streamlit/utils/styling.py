"""
Custom CSS styling for the Streamlit app
"""

def get_custom_css() -> str:
    """Return custom CSS for the app"""
    return """
    <style>
        /* Main container with gradient */
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        /* Chat message styling */
        .stChatMessage {
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #f8f9fa;
        }
        
        /* Button styling */
        .stButton>button {
            background-color: #667eea;
            color: white;
            border-radius: 10px;
            border: none;
            padding: 10px 24px;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .stButton>button:hover {
            background-color: #764ba2;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        /* Input box styling */
        .stTextInput>div>div>input {
            border-radius: 10px;
            border: 2px solid #667eea;
        }
        
        /* Header text */
        h1 {
            color: white;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        h2, h3 {
            color: #667eea;
        }
        
        /* Alert boxes */
        .stAlert {
            border-radius: 10px;
        }
        
        /* Custom card style */
        .card {
            background-color: white;
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
    </style>
    """
