# -------- Stage 1: Build Stage --------
FROM python:3.12-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install pip-tools to safely compile requirements (optional but professional)
RUN pip install --no-cache-dir pip-tools

# Create working directory
WORKDIR /app

# Copy only requirement file
COPY requirements.txt .

# Install dependencies into /install directory (not system-wide)
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# -------- Stage 2: Production Stage --------
FROM python:3.12-slim

# Set environment variables again (best practice)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create app directory
WORKDIR /app

# Copy only installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy the application code
COPY . .

# Expose the app port
EXPOSE 5000

# Create non-root user for better security
RUN adduser --disabled-password --no-create-home appuser
USER appuser

# Run the app
CMD ["python", "app.py"]

