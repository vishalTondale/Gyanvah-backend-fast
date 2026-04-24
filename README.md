# GyanVah FastAPI Backend
# सिद्धिर्भवति कर्मजा (Success comes from action)

Educational platform backend API built with FastAPI and Snowflake.

## Features
- RESTful API for courses, books, projects, notes, videos
- Python course videos with episode management
- Contact form handling
- Learning paths with course relationships
- Statistics and analytics
- CORS enabled for frontend integration

## Tech Stack
- **FastAPI** - Modern Python web framework
- **Snowflake** - Cloud data warehouse
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## Local Development

1. Clone the repository
2. Create virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file with your Snowflake credentials:
   ```
   SNOWFLAKE_ACCOUNT=your_account
   SNOWFLAKE_USER=your_user
   SNOWFLAKE_PASSWORD=your_password
   SNOWFLAKE_WAREHOUSE=your_warehouse
   SNOWFLAKE_DATABASE=GYANVAH
   SNOWFLAKE_SCHEMA=PUBLIC
   ```

5. Run the application:
   ```bash
   uvicorn fastapi_app:app --reload
   ```

6. Visit `http://localhost:8000/docs` for API documentation

## Deployment

### Render (Recommended - Free)
1. Fork/clone this repository to GitHub
2. Go to [render.com](https://render.com) and sign up
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure the service:
   - **Runtime**: Python 3.13
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn fastapi_app:app --host 0.0.0.0 --port $PORT`
6. Add environment variables in Render dashboard
7. Deploy!

> Note: This repo also includes `render.yaml` in `fastapi_backend/` to pin the Render runtime to Python 3.13 and avoid build errors with `pydantic-core` on newer Python versions.

### Railway
1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Add environment variables
4. Deploy automatically

### Fly.io
1. Install Fly CLI
2. Run `fly launch` in your project directory
3. Configure environment variables
4. Deploy with `fly deploy`

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SNOWFLAKE_ACCOUNT` | Your Snowflake account URL | Yes |
| `SNOWFLAKE_USER` | Snowflake username | Yes |
| `SNOWFLAKE_PASSWORD` | Snowflake password | Yes |
| `SNOWFLAKE_WAREHOUSE` | Snowflake warehouse name | Yes |
| `SNOWFLAKE_DATABASE` | Database name (GYANVAH) | Yes |
| `SNOWFLAKE_SCHEMA` | Schema name (PUBLIC) | Yes |

## API Endpoints

- `GET /` - API information
- `GET /docs` - Interactive API documentation
- `GET /stats` - Platform statistics
- `GET /courses` - List courses
- `GET /books` - List books
- `GET /projects` - List projects
- `GET /notes` - List notes
- `GET /videos` - List videos
- `GET /python-course` - Python course episodes
- `POST /contact` - Submit contact form

## License

This project is part of the GyanVah educational platform.</content>
<parameter name="filePath">d:\gyanvah-firstcopy\fastapi_backend\README.md