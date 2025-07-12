# Adapta Hackathon Agent Backend

AI-powered solution recommendation system built with FastAPI, LangChain, and pgvector.

## 🚀 Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **LangChain**: Framework for developing applications with language models
- **pgvector**: PostgreSQL extension for vector similarity search
- **OpenAI**: Embeddings and language models
- **SQLAlchemy**: SQL toolkit and ORM
- **Alembic**: Database migrations
- **Pydantic**: Data validation using Python type annotations

## 📋 Features

- **AI-Powered Recommendations**: Vector similarity search using OpenAI embeddings
- **Solution Owner Management**: CRUD operations for solution providers
- **Product Catalog**: Product management with advanced search capabilities
- **Chat Interface**: Conversational AI for product recommendations
- **Context Management**: Enhanced user context for personalized recommendations
- **Background Tasks**: Asynchronous embedding generation
- **Health Monitoring**: Built-in health checks and metrics

## 🏗️ Project Structure

```
adapta-hackathon-agent-backend/
├── app/
│   ├── api/v1/               # API routes
│   ├── core/                 # Core functionality
│   │   ├── config.py         # Configuration management
│   │   ├── database.py       # Database setup
│   │   └── embeddings.py     # Embedding service
│   ├── models/               # Database models
│   │   ├── base.py           # Base model classes
│   │   ├── owner.py          # Solution owner model
│   │   ├── product.py        # Product model
│   │   └── chat.py           # Chat and context models
│   ├── schemas/              # Pydantic schemas
│   │   ├── common.py         # Common schemas
│   │   ├── owner.py          # Owner schemas
│   │   ├── product.py        # Product schemas
│   │   └── chat.py           # Chat schemas
│   ├── services/             # Business logic
│   ├── migrations/           # Database migrations
│   └── main.py               # FastAPI application
├── tests/                    # Test files
├── scripts/                  # Utility scripts
├── docs/                     # Documentation
├── .env.example              # Environment variables template
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🛠️ Setup

### Prerequisites

- Python 3.12+
- PostgreSQL 15+ with pgvector extension
- OpenAI API key

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd adapta-hackathon-agent-backend
```

2. **Create virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Setup database:**
```bash
# Make sure PostgreSQL is running with pgvector extension
# Run migrations (when implemented)
alembic upgrade head
```

## 🔧 Configuration

Key environment variables in `.env`:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/adapta_hackathon
DATABASE_URL_SYNC=postgresql://user:password@localhost:5432/adapta_hackathon

# OpenAI
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_EMBEDDING_MODEL=text-embedding-3-large
OPENAI_EMBEDDING_DIMENSIONS=1536

# FastAPI
DEBUG=True
SECRET_KEY=your-secret-key-here
API_V1_STR=/api/v1
```

## 🚀 Running the Application

### Development

```bash
# With auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python directly
python app/main.py
```

### Production

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📚 API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_embeddings.py
```

## 🔍 API Endpoints

### Core Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/v1/owners/` - List solution owners
- `POST /api/v1/owners/` - Create solution owner
- `GET /api/v1/products/` - List products
- `POST /api/v1/products/` - Create product
- `POST /api/v1/messages/` - Send chat message
- `GET /api/v1/recommendations/products` - Get product recommendations

## 🎯 Key Features

### Vector Similarity Search

The system uses OpenAI embeddings and pgvector for intelligent similarity search:

```python
# Example: Finding similar products
similar_products = await recommend_products(
    user_id="user123",
    query="CRM software for small business",
    k=5
)
```

### Embedding Service

Automatic embedding generation with caching:

```python
# Generate embeddings for text
embedding = await embedding_service.embed_text("Your text here")

# Batch processing
embeddings = await embedding_service.embed_texts(["text1", "text2"])
```

### Context Management

Enhanced user context for personalized recommendations:

```python
# Create user context
context = await create_enhanced_context(
    user_id="user123",
    context_type="onboarding",
    preferences={"industry": "healthcare", "size": "small"}
)
```

## 📊 Database Schema

### Main Tables

- `solutions_owner` - Solution providers
- `products` - Product catalog
- `users_chat_history` - Chat messages
- `users_enhanced_context` - User context data

All tables include `embeddings` columns (vector(1536)) for similarity search.

## 🔐 Security

- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy
- Environment variable management
- CORS configuration
- Request logging and monitoring

## 🚢 Deployment

### Docker

```bash
# Build image
docker build -t adapta-backend .

# Run container
docker run -p 8000:8000 --env-file .env adapta-backend
```

### Environment Variables

Ensure all required environment variables are set in production:

- Database connection strings
- OpenAI API key
- Security keys
- Monitoring configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:

1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed information

## 🏆 Acknowledgments

- OpenAI for embeddings and language models
- pgvector for vector similarity search
- FastAPI for the excellent web framework
- LangChain for LLM integration tools 
