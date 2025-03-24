# AI Debate Arena

An interactive debating platform where two AI agents can engage in structured debates on various topics.

## Project Structure

```
debate-arena/
├── public/              # Static files for frontend
│   ├── index.html      # Main HTML file
│   └── screens/        # Screen assets
├── autogen-multi-agent.py  # Backend Python script
├── firebase.json       # Firebase configuration
├── .firebaserc         # Firebase project settings
└── README.md          # Project documentation
```

## Deployment Instructions

### Prerequisites

1. Install Firebase CLI:
```bash
npm install -g firebase-tools
```

2. Login to Firebase:
```bash
firebase login
```

### Deploy to Firebase

1. Initialize Firebase project (first time only):
```bash
firebase init
```
- Select "Hosting"
- Choose your project
- Use "public" as your public directory
- Configure as a single-page app: Yes
- Don't overwrite index.html: No

2. Deploy to Firebase:
```bash
firebase deploy
```

### Backend Deployment

The backend needs to be deployed separately as a Cloud Function or to a server of your choice:

1. Set up your backend server (e.g., on Google Cloud Run, Heroku, etc.)
2. Update the API endpoint in `public/index.html` to point to your deployed backend

## Local Development

1. Start the backend server:
```bash
python autogen-multi-agent.py
```

2. Serve the frontend locally:
```bash
firebase serve
```

## Environment Variables

Make sure to set up the following environment variables in your backend deployment:
- OpenAI API Key
- Other necessary configuration variables

## Notes

- The frontend is deployed on Firebase Hosting
- The backend needs to be deployed separately
- CORS needs to be configured properly in the backend
- Make sure to secure your API endpoints and add proper authentication 