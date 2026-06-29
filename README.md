# Architecture Review Copilot (ARC) 🚀

ARC is an enterprise-grade agentic AI platform that analyzes PowerPoint solution architecture documents, reconstructs system designs, identifies architectural flaws, and generates corrected cloud-native architectures with diagrams.

## 🌟 Features

- **PPTX Ingestion**: Extract text and images from PowerPoint files.
- **OCR Support**: Analyze diagrams and text within images using Tesseract.
- **AI Reconstruction**: Infer structured system architecture from unstructured slide data.
- **Multi-Agent Review**: Specialized agents for Security, Scalability, Reliability, GCP Best Practices, and FinOps.
- **Auto-Correction**: Generate an "ideal" GCP-native architecture based on findings.
- **Diagram Generation**: Automatically produce Mermaid diagrams and JSON graph models.

## 🏗️ Architecture

The system is built with FastAPI and follows a modular, agentic design:

- `app/parsers`: PPTX and OCR logic.
- `app/agents`: Specialized AI reviewers.
- `app/services`: Core logic for reconstruction, synthesis, and correction.
- `app/diagrams`: Mermaid and graph generation.
- `app/models`: Pydantic data models.

## 🚀 Quick Start

### Using Docker

```bash
docker-compose up --build
```

### Manual Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up environment variables in `.env`:
   ```bash
   OPENAI_API_KEY=your_key
   ```
3. Run the application:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## 🌐 Local Network Access

To access ARC from other devices on your local network:

1. **Find your Local IP Address**:
   - On Windows: Run `ipconfig` in CMD. Look for `IPv4 Address` (e.g., `192.168.1.50`).
   - On Linux/Mac: Run `ifconfig` or `ip addr`.
2. **Access the Web UI**:
   - From another device, open a browser and go to `http://<YOUR_IP>:8000`.

## 🧪 Testing

Run tests using pytest:
```bash
pytest
```

## 🛠️ Technology Stack

- **Backend**: Python 3.11, FastAPI, Pydantic
- **AI Layer**: OpenAI GPT-4 (or compatible)
- **Parsing**: python-pptx, Tesseract OCR
- **Graph/Diagrams**: NetworkX, Mermaid
