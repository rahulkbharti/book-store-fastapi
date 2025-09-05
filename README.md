# BookStore

A simple Book Store API with otp verification login

# Getting Started

1. **Clone the repository:**

   ```bash
   git clone https://github.com/rahulkbharti/book-store-fastapi.git
   cd book-store-fastapi
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Make Sure You have .env in root folder and replace with your own database config
   DATABASE_URL=postgresql+asyncpg://<username>:<password>@<host>:<port>/<database_name>
   SECRET_KEY=<your_secret_key> # for jwt

   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Start the FastAPI application:**

   ```bash
   py run.py
   ```

5. **Open in browser:**
   ```
   http://localhost:8000
   ```

- API docs available at: `http://localhost:8000/docs`
- API collection and environment variable setup can be found in the Postman folder.

