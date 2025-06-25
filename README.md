# MCP EdTech Analytics Demo

This demo showcases how MCP (Model Context Protocol) can be used to create natural language interfaces for business analytics queries.

## What This Demo Shows

- **Natural Language Queries**: Ask business questions in plain English
- **Automated Tool Selection**: MCP automatically selects the right tools to answer your questions
- **Real-time Analytics**: Get instant insights from your data

## Setup & Running

1. **Create and Activate Virtual Environment**:
   ```bash
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate Sample Data**:
   ```bash
   python3 setup-db.py
   ```

4. **Run the Demo**:
   
   **Option A - AI-Powered Web UI (Most Impressive!)**:
   ```bash
   streamlit run ai-web-ui.py
   ```
   *Requires OpenAI API key - shows true AI + MCP integration*
   
   **Option B - Pattern-Matching Web UI**:
   ```bash
   streamlit run web-ui.py
   ```
   *No API key needed - demonstrates MCP structure*
   
   **Option C - Command Line Demo**:
   ```bash
   python3 mcp-client.py
   ```
   *Shows programmatic MCP client usage*
   
   > **Note**: The MCP server runs automatically when you start the client or web UI. No need to start it separately!

## Sample Questions the Demo Answers

- "What's the completion rate for our Kubernetes course?"
- "Which students need immediate intervention?"
- "How many support tickets do Docker students typically create?"

## Architecture

- **setup-db.py**: Generates 1000 sample student records with course data
- **mcp-server.py**: MCP server with analytics tools
- **ai-web-ui.py**: AI-powered web interface (GPT-4 + MCP) 🤖
- **web-ui.py**: Pattern-matching web interface (no API key needed)
- **mcp-client.py**: Command-line demo client

## Demo Features

### 🤖 **AI-Powered Version** (`ai-web-ui.py`)
- **True AI Understanding**: GPT-4 interprets natural language questions
- **Intelligent Tool Selection**: AI automatically chooses the right MCP tools
- **Multi-tool Coordination**: AI can combine multiple tools for complex queries
- **Natural Language Responses**: AI synthesizes results into business-friendly answers
- **Transparent Process**: See exactly how AI analyzed your question and selected tools

### 🔧 **Pattern-Matching Version** (`web-ui.py`)
- **No API Key Required**: Works without external AI services
- **Educational Value**: Shows MCP structure and tool routing
- **Fast Responses**: Instant pattern-based tool selection
- **Predictable Behavior**: Consistent responses for demo purposes

The magic of MCP is that you can ask business questions in natural language, and it automatically figures out which tools to call and how to combine the results! 