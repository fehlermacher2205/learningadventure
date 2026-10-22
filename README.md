# Learning Adventure
AI-based assistants to generate personalized exercises, provide feedback on solutions, and adapt to individual learning preferences. 
# To use this application you require an openAI-api-key, you can get your own at platform.openai.com
# You have to create an .env file in the backend, look at the src/backend/.env.example
```
You will have to set MODEL, OPENAI_API_KEY, OPENAI_API_BASE in the .env you just created
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

# Visit Frontend using default Address```http://localhost:5173/``` and use the button on the bottom left to login
```
matriculation_number="9999999",
password= "Ganyu.01Emilie.02Fehler.03"
```
# You will need an account with admin rights if you want to create profile/course using the frontend.

## Pleate note that the profile creation using frontend will not allow customized name.
## This account is created in backend/services/InitServices.py 

# You can visit ```http://0.0.0.0:8000/docs``` to know how the port (backend/main.py to) is created if you are the host machine
