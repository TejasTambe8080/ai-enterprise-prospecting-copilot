# FlytBase Inbound BDR System

AI-assisted inbound-lead qualification and AE handoff using FastAPI, MongoDB, Gemini, React, Tailwind, and Material UI.

## Local development

1. Copy `backend/.env.example` to `backend/.env` and provide MongoDB, Gemini, and secret values.
2. Copy `frontend/.env.example` to `frontend/.env` if the defaults need changing.
3. Start the API: `cd backend; .\\venv\\Scripts\\python.exe -m uvicorn app.main:app --reload`.
4. Start the UI: `cd frontend; npm run dev`.

## Deployment

- Render uses `backend/render.yaml`. Set `MONGODB_URI` and `GEMINI_API_KEY` as secret environment variables in Render.
- Vercel deploys `frontend` with `vercel.json`. Set `VITE_API_URL` and `VITE_WS_URL` in the Vercel project if using a different backend URL.
- After Vercel assigns the final URL, add it to Render's `ALLOWED_ORIGINS` as comma-separated origins.

## Verification

`GET /health` confirms API availability. Run `npm run build` from `frontend` before deployment.
