# Learning Adventure
AI-based assistants to generate personalized exercises, provide feedback on solutions, and adapt to individual learning preferences. 
# An openAI-api-key is required, you can get your own at platform.openai.com
# Create a .env file in the backend folder and replace all three [] with your actual keys.
```
DATABASE_URL=sqlite:///./database.db
API_PREFIX=/api
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
MODEL = []
OPENAI_API_KEY= []
OPENAI_API_BASE= []
```
# Inside backend
```
# Navigate into the frontend directory
cd backend
# Install dependencies and start the api server
uv sync
uv run main.py
```

# Start frontend
```
# Navigate into the frontend directory
cd frontend
# Install dependencies and start the development server
npm install
npm run dev
```

# Visit ```http://localhost:5173/``` and use the login button on the bottom left
```
matriculation_number="9999999",
password= "Ganyu.01Emilie.02Fehler.03"
```
# Only admin can create new profile/course. For more details, check backend/services/InitServices.py
# Host machine can visit ```http://0.0.0.0:8000/docs``` to see how the API is used
