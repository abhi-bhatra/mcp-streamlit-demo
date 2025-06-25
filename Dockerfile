# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY cloud-mcp-server.py .
COPY student_data.csv* ./

# Expose port (Cloud Run will set the PORT environment variable)
EXPOSE 8080

# Run the MCP server
CMD ["python", "cloud-mcp-server.py"]
