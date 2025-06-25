# server.py - Our MCP Server
from fastmcp import FastMCP
import pandas as pd
import os

mcp = FastMCP("EdTech Analytics")

# Load the student data
if os.path.exists('student_data.csv'):
    df = pd.read_csv('student_data.csv')
    print(f"Loaded {len(df)} student records")
else:
    print("No student data found. Please run setup-db.py first.")
    exit(1)

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

if __name__ == "__main__":
    print("Starting MCP server...")
    mcp.run()
