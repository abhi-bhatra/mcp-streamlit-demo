# cloud-mcp-server.py - MCP Server optimized for Cloud Run deployment
from fastmcp import FastMCP
import pandas as pd
import os

# Create MCP server instance
mcp = FastMCP("EdTech Analytics - Cloud Edition")

# Load the student data
if os.path.exists('student_data.csv'):
    df = pd.read_csv('student_data.csv')
    print(f"Loaded {len(df)} student records")
else:
    # Generate sample data if CSV doesn't exist (for Cloud Run)
    print("Generating sample data for Cloud Run deployment...")
    import random
    students = []
    for i in range(1000):
        students.append({
            'student_id': f'STU{i:04d}',
            'course': random.choice(['Docker', 'Kubernetes', 'AWS', 'Terraform']),
            'completion_rate': random.uniform(0.2, 1.0),
            'assessment_score': random.randint(60, 100),
            'support_tickets': random.randint(0, 5),
            'enrollment_date': f'2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}'
        })
    df = pd.DataFrame(students)
    print(f"Generated {len(df)} student records for demo")

@mcp.tool()
def get_course_completion_rates(course: str = None) -> str:
    """Get completion rates for courses"""
    if course:
        course_data = df[df['course'] == course]
        if len(course_data) == 0:
            return f"No data found for course: {course}"
        data = course_data['completion_rate'].mean()
        return f"Average completion rate for {course}: {data:.2%}"
    else:
        rates = df.groupby('course')['completion_rate'].mean()
        return f"Completion rates by course:\n{rates.to_string()}"

@mcp.tool()
def identify_struggling_students(threshold: float = 0.5) -> str:
    """Find students with low completion rates"""
    struggling = df[df['completion_rate'] < threshold]
    return f"Found {len(struggling)} students below {threshold:.0%} completion"

@mcp.tool()
def get_support_tickets_by_course(course: str = None) -> str:
    """Get support ticket statistics by course"""
    if course:
        course_data = df[df['course'] == course]
        if len(course_data) == 0:
            return f"No data found for course: {course}"
        avg_tickets = course_data['support_tickets'].mean()
        total_tickets = course_data['support_tickets'].sum()
        return f"{course} students: {avg_tickets:.1f} tickets per student on average ({total_tickets} total)"
    else:
        ticket_stats = df.groupby('course')['support_tickets'].agg(['mean', 'sum'])
        return f"Support tickets by course:\n{ticket_stats.to_string()}"

@mcp.tool()
def get_server_info() -> str:
    """Get information about this MCP server deployment"""
    return f"🌐 EdTech Analytics MCP Server - Running on Google Cloud Run\n📊 Serving {len(df)} student records\n🚀 Scalable, serverless analytics platform"

if __name__ == "__main__":
    # For Cloud Run, we need to use HTTP transport and listen on the port provided by Cloud Run
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting MCP server on Cloud Run, port {port}...")
    mcp.run(transport="sse", host="0.0.0.0", port=port) 