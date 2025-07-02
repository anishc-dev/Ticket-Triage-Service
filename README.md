## Flow Diagram
![image](https://github.com/user-attachments/assets/1ab5f75c-0a04-4238-ad62-84914c7113e1)


# Ticket Triage Service

A comprehensive ticket classification and response system built with FastAPI, ChromaDB, PostgreSQL, and Google Gemini AI. This service automatically classifies incoming support tickets by product area and urgency, stores metadata in PostgreSQL, and provides intelligent responses using a RAG (Retrieval-Augmented Generation) system.

## Features

- **Automatic Ticket Classification**: Uses Google Gemini AI to classify tickets by product area and urgency
- **Document Ingestion & Search**: Ingests documentation from Netskope docs and provides semantic search
- **RAG System**: Retrieval-Augmented Generation for intelligent ticket responses
- **PostgreSQL Storage**: Persistent storage of ticket metadata and classification results
- **Interactive Web Interface**: HTML forms for ticket classification and query responses
- **Docker Containerization**: Easy deployment and scaling

## Architecture

- **FastAPI**: Web framework for API endpoints
- **ChromaDB**: Vector database for document storage and semantic search
- **PostgreSQL**: Relational database for ticket metadata
- **Google Gemini AI**: LLM for ticket classification and response generation
- **Docker & Docker Compose**: Containerization and orchestration

## Prerequisites

- Docker and Docker Compose
- Google Gemini API key
- Internet connection (for initial document ingestion)

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Ticket-Triage-Service
   ```

2. **Set up environment variables**
   - Add your Google Gemini API key to `docker-compose.yml`:
   ```yaml
   environment:
     - GEMINI_API_KEY=your_api_key_here
   ```

3. **Start the services**
   ```bash
   docker-compose up --build -d
   ```

4. **Access the application**
   - Main API: http://localhost:8002
   - Ticket Classification Interface: http://localhost:8002/classify
   - RAG Query Interface: http://localhost:8002/respond
   - ChromaDB Stats: http://localhost:8002/chromadb/stats

## API Endpoints

### Core Endpoints

- `GET /` - Welcome message
- `GET /classify` - HTML interface for ticket classification
- `POST /classify` - API endpoint for ticket classification
- `GET /respond` - HTML interface for RAG queries
- `POST /respond` - API endpoint for RAG queries
- `GET /chromadb` - HTML view of ChromaDB contents
- `GET /chromadb/stats` - ChromaDB collection statistics

### Ticket Classification

**POST /classify**
```json
{
  "ticket_id": 123,
  "subject": "VPN connection issues",
  "description": "Users cannot connect to corporate VPN",
  "priority": "High"
}
```

**Response:**
```json
{
  "message": "Successfully Classified and inserted metadata of ticket 123 into the database",
  "classification": {
    "category": "Zero Trust Network Access (ZTNA)",
    "priority": "High",
    "ticket_id": 123
  }
}
```

### RAG Query System

**POST /respond**
```json
{
  "question": "How do I configure VPN access?"
}
```

**Response:**
```json
{
  "response": "Based on the documentation...",
  "documents": ["relevant_document_1", "relevant_document_2"]
}
```

## Product Categories

The system classifies tickets into the following categories:
- CASB
- ZTNA
- SASE
- SSE
- Converged Gateway
- Unified Data Security
- Next Gen Secure Web Gateway (SWG)
- Cloud Inline Security
- Zero Trust Network Access (ZTNA)
- Cloud Firewall
- Enterprise Browser
- Remote Browser Isolation
- GenAI Security
- Threat Protection
- Data Security Posture Management (DSPM)
- Security for AI
- Firewall as a Service
- Advanced Analytics
- Digital Experience Management

## Priority Levels

- Low
- Medium
- High

## Database Schema

### TICKET_METADATA Table
- `ticket_id` (VARCHAR): Unique ticket identifier
- `category` (VARCHAR): Classified product category
- `priority` (VARCHAR): Classified priority level
- `query_time` (TIMESTAMP): Classification timestamp

## Document Ingestion

The system automatically ingests documentation from `docs.netskope.com` on first startup if ChromaDB is empty. The ingestion process:

1. Parses the sitemap to discover documentation pages
2. Scrapes content from each page
3. Stores documents in ChromaDB with embeddings for semantic search
4. Provides 2912+ documents for RAG queries

## Docker Services

### Listener Service (Port 8002)
- FastAPI application
- Handles all API endpoints and web interfaces
- Connects to PostgreSQL and ChromaDB

### PostgreSQL Service (Port 5435)
- Database for ticket metadata storage
- Persistent volume for data retention

### ChromaDB
- Vector database for document storage
- Persistent volume for document retention

## Environment Variables

- `GEMINI_API_KEY`: Google Gemini API key for AI operations
- `POSTGRES_DB`: Database name (default: ticket_triage)
- `POSTGRES_USER`: Database user (default: postgres)
- `POSTGRES_PASSWORD`: Database password (default: password)

## Development

### Project Structure
```
Ticket-Triage-Service/
├── api/
│   └── server.py              # FastAPI application entry point
├── endpoints/
│   ├── ticket_classifier.py   # Ticket classification endpoints
│   ├── listener.py            # RAG query endpoints
│   └── chroma_db.py           # ChromaDB management endpoints
├── ingestion/
│   ├── document_ingestion.py  # Document ingestion logic
│   └── sitemap_parser.py      # Sitemap parsing utilities
├── configuration/
│   └── classify.py            # Classification categories and priorities
├── database/
│   └── database.py            # PostgreSQL connection and operations
├── templates/
│   ├── classify.html          # Ticket classification interface
│   └── respond.html           # RAG query interface
├── chroma_db/                 # ChromaDB data directory
├── docker/
│   └── requirements.txt       # Python dependencies
├── docker-compose.yml         # Service orchestration
└── Dockerfile                 # Container definition
```

### Adding New Features

1. **New Endpoints**: Add to appropriate file in `endpoints/`
2. **New Templates**: Add HTML files to `templates/`
3. **Database Changes**: Update `database/database.py` and `TABLE_COLUMNS`
4. **Dependencies**: Add to `docker/requirements.txt`

## Troubleshooting

### Common Issues

1. **Port Conflicts**: Ensure ports 8002 and 5435 are available
2. **API Key Issues**: Verify Google Gemini API key is valid and has sufficient quota
3. **Database Connection**: Check PostgreSQL service is running and accessible
4. **Document Ingestion**: Clear ChromaDB volume to trigger re-ingestion

### Logs
```bash
# View application logs
docker-compose logs listener

# View database logs
docker-compose logs postgres
```

### Reset Data
```bash
# Remove all data and start fresh
docker-compose down --volumes
docker-compose up --build -d
```

## Performance

- **Document Ingestion**: ~2912 documents ingested on first startup
- **Classification Response Time**: ~2-5 seconds per ticket
- **RAG Query Response Time**: ~3-7 seconds per query
- **Database Operations**: Sub-second response times

## Security Considerations

- API keys are stored as environment variables
- Database credentials are configured via environment variables
- No sensitive data is logged
- All external API calls use HTTPS

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs
3. Create an issue in the repository
