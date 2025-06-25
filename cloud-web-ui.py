import streamlit as st
from fastmcp import FastMCP, Client
import pandas as pd
import asyncio
import json
from openai import OpenAI

# Page config
st.set_page_config(
    page_title="Cloud MCP Demo - EdTech Analytics",
    page_icon="☁️",
    layout="wide"
)

# Title and description
st.title("☁️ Cloud MCP Demo - EdTech Analytics")
st.markdown("### Demonstrating Local vs Cloud MCP Server Deployment")
st.markdown("**Compare**: Local MCP server vs Production Cloud Run deployment")

# Configuration sidebar
with st.sidebar:
    st.header("🔧 Demo Configuration")
    
    # Server selection
    server_type = st.radio(
        "Select MCP Server:",
        ["Local Server", "Cloud Run Server"],
        help="Choose between local development server or production Cloud Run deployment"
    )
    
    if server_type == "Local Server":
        st.info("🏠 **Local Mode**\n- Fast development\n- Single user\n- Local data")
        server_url = "mcp-server.py"
    else:
        st.info("☁️ **Cloud Mode**\n- Production deployment\n- Multi-user\n- Scalable")
        cloud_url = st.text_input(
            "Cloud Run URL:", 
            value="https://poc-abhi-mcp-406451179998.us-central1.run.app/sse",
            help="Enter your Cloud Run MCP server URL"
        )
        server_url = cloud_url if cloud_url else "https://your-mcp-server-xyz.run.app/sse"
    
    st.divider()
    
    # AI Configuration
    st.header("🤖 AI Configuration")
    api_key = st.text_input("OpenAI API Key", type="password", help="Required for AI-powered queries")
    
    if not api_key:
        st.warning("⚠️ Enter OpenAI API key for AI features")

# Server status check
def test_server_connection(server_url):
    try:
        if server_url == "mcp-server.py":
            # Local server check
            import os
            if not os.path.exists("mcp-server.py"):
                return False, "mcp-server.py not found"
            if not os.path.exists("student_data.csv"):
                return False, "student_data.csv not found - run: python setup-db.py"
            return True, "Local server files ready"
        else:
            # Cloud server check - we'll test connection during query
            return True, f"Cloud server configured: {server_url}"
    except Exception as e:
        return False, str(e)

server_ok, server_status = test_server_connection(server_url)

# Display server status
if server_ok:
    st.success(f"✅ {server_status}")
else:
    st.error(f"❌ Server Issue: {server_status}")
    st.stop()

# AI-powered MCP query function
async def query_mcp_server(question: str, server_url: str, api_key: str):
    """Query the MCP server (local or cloud) with AI assistance"""
    
    # Initialize OpenAI client
    openai_client = OpenAI(api_key=api_key)
    
    # Define available MCP tools for the AI
    tools_description = """
    You are an AI assistant that can analyze student data using MCP tools. You have access to these tools:

    1. get_course_completion_rates(course: str | None) 
       - Get completion rates for a specific course or all courses
       - Course options: Docker, Kubernetes, AWS, Terraform
    
    2. identify_struggling_students(threshold: float)
       - Find students with completion rate below threshold (0.0 to 1.0)
    
    3. get_support_tickets_by_course(course: str | None)
       - Get support ticket statistics by course or all courses
    
    4. get_server_info()
       - Get information about the MCP server deployment

    Based on the user's question, determine which tool(s) to call and with what parameters.
    """
    
    # Ask AI to analyze the question
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": tools_description},
            {"role": "user", "content": f"""
            Analyze this question and create a plan: "{question}"
            
            Return JSON with:
            {{
                "analysis": "What the user is asking",
                "tool_calls": [
                    {{
                        "tool": "tool_name",
                        "parameters": {{"param": "value"}},
                        "reasoning": "Why this tool"
                    }}
                ]
            }}
            """}
        ],
        temperature=0.1
    )
    
    try:
        ai_plan = json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        return {"error": "AI response was not valid JSON"}
    
    # Execute the MCP tool calls
    results = []
    
    try:
        # Create client based on server type
        if server_url.endswith(".py"):
            # Local server
            client = Client(server_url)
        else:
            # Cloud server (HTTP/SSE)
            client = Client(server_url)
        
        async with client:
            for tool_call in ai_plan.get("tool_calls", []):
                tool_name = tool_call.get("tool")
                parameters = tool_call.get("parameters", {})
                
                try:
                    result = await client.call_tool(tool_name, parameters)
                    results.append({
                        "tool": tool_name,
                        "parameters": parameters,
                        "result": result.content[0].text if hasattr(result, 'content') and result.content else str(result),
                        "reasoning": tool_call.get("reasoning", "")
                    })
                except Exception as e:
                    results.append({
                        "tool": tool_name,
                        "parameters": parameters,
                        "error": str(e),
                        "reasoning": tool_call.get("reasoning", "")
                    })
    
    except Exception as e:
        return {"error": f"Failed to connect to MCP server: {str(e)}"}
    
    # Synthesize final answer
    results_text = "\n\n".join([
        f"Tool: {r['tool']}\nResult: {r.get('result', r.get('error', 'No result'))}"
        for r in results
    ])
    
    final_response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a business analyst. Provide clear, actionable insights."},
            {"role": "user", "content": f"""
            Question: "{question}"
            
            MCP Results:
            {results_text}
            
            Provide a clear business answer.
            """}
        ],
        temperature=0.3
    )
    
    return {
        "ai_analysis": ai_plan,
        "tool_results": results,
        "final_answer": final_response.choices[0].message.content,
        "server_type": "Local" if server_url.endswith(".py") else "Cloud"
    }

# Main demo interface
st.header("🚀 Query Interface")

# Example questions based on server type
if server_type == "Local Server":
    example_questions = [
        "What's the completion rate for Docker?",
        "Which students need help?",
        "Show me server information"
    ]
else:
    example_questions = [
        "Compare all course completion rates",
        "Which course needs the most attention?",
        "Tell me about this cloud deployment"
    ]

# Question input
col1, col2 = st.columns([3, 1])
with col1:
    user_question = st.selectbox(
        "Try these example questions:",
        [""] + example_questions,
        key="question_select"
    )

with col2:
    if st.button("🔄 Get Server Info"):
        user_question = "Tell me about this server deployment"

# Custom question input
custom_question = st.text_input(
    "Or ask your own question:",
    placeholder="e.g., Which course has the highest support ticket volume?"
)

# Use custom question if provided
final_question = custom_question if custom_question.strip() else user_question

# Query button
if st.button("🧠 Query MCP Server", type="primary", disabled=not (api_key and final_question)):
    if not api_key:
        st.error("Please enter your OpenAI API key")
    elif not final_question:
        st.error("Please select or enter a question")
    else:
        with st.spinner(f"🔍 Querying {server_type}..."):
            try:
                result = asyncio.run(query_mcp_server(final_question, server_url, api_key))
                
                if "error" in result:
                    st.error(f"❌ Error: {result['error']}")
                else:
                    # Success display
                    st.success(f"✅ **Query Complete!** (via {result['server_type']} Server)")
                    
                    # Show the answer
                    st.subheader("🎯 Answer:")
                    st.markdown(result["final_answer"])
                    
                    # Show technical details
                    with st.expander("🔍 Technical Details", expanded=False):
                        st.json(result["ai_analysis"])
                        
                        st.subheader("Tool Execution:")
                        for tool_result in result["tool_results"]:
                            st.write(f"**{tool_result['tool']}** - {tool_result['reasoning']}")
                            if 'result' in tool_result:
                                st.code(tool_result['result'])
                            else:
                                st.error(tool_result['error'])
                            st.divider()
                    
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 14px;'>
    <p>🚀 Made with ❤️ by Abhinav for GCCD, Delhi 2025!</p>
</div>
""", unsafe_allow_html=True)
