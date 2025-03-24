import asyncio 
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from autogen_agentchat.agents import AssistantAgent 
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create an OpenAI model Client
model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini", 
    api_key=os.getenv('OPENAI_API_KEY')
)

# Create a Flask app
app = Flask(__name__)

# Configure CORS for Firebase hosting
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://ai-debate-arena-31f3e.web.app",
            "https://ai-debate-arena-31f3e.firebaseapp.com",
            "http://localhost:5000",
            "http://localhost:3000"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

@app.route('/')
def index():
    return jsonify({
        "status": "healthy",
        "message": "Welcome to the AI Debate Arena API"
    })

@app.route('/start-debate', methods=['POST'])
def start_debate():
    try:
        data = request.json
        if not data or 'topic' not in data or 'candiate1Name' not in data or 'candiate2Name' not in data:
            return jsonify({
                "error": "Missing required fields: topic, candiate1Name, candiate2Name"
            }), 400

        topic = data['topic']
        candiate1Name = data['candiate1Name']
        candiate2Name = data['candiate2Name']

        # Create Primary Agent
        primary_agent = AssistantAgent(
            candiate1Name,
            model_client=model_client,
            system_message = """You are a skilled debater participating in a structured debate. 
            Your role is to present well-reasoned arguments and respond thoughtfully to your opponent's points.
            Focus on the topic at hand and maintain a professional tone.
            Use markdown formatting for better presentation:
            - Use headers (##) for main points
            - Use bullet points for lists
            - Use **bold** for emphasis
            - Use > for quotes
            - Use code blocks for technical content
            Respond with 'FINALIZE' when you've made your concluding argument."""
        )

        # Create Critic Agent
        critic_agent = AssistantAgent(
            candiate2Name,
            model_client=model_client,
            system_message = """You are a skilled debate opponent.
            Your role is to present counter-arguments and engage critically with the other debater's points.
            Maintain a professional tone and focus on the topic.
            Use markdown formatting for better presentation:
            - Use headers (##) for main points
            - Use bullet points for lists
            - Use **bold** for emphasis
            - Use > for quotes
            - Use code blocks for technical content
            Respond with 'FINALIZE' when you've made your concluding argument."""
        )

        # Define termination condition
        text_termination = TextMentionTermination(text="FINALIZE")

        # Create team
        team = RoundRobinGroupChat([primary_agent, critic_agent], termination_condition=text_termination)

        # Run the debate
        result = asyncio.run(team.run(task=topic))

        # Process results
        candiate1Response = ""
        candiate2Response = ""
        token_count = 0

        for message in result.messages:
            if message.source == candiate1Name:
                candiate1Response += message.content + "\n\n"
            elif message.source == candiate2Name:
                candiate2Response += message.content + "\n\n"
                token_count += (
                    message.models_usage.prompt_tokens + 
                    message.models_usage.completion_tokens
                )

        return jsonify({
            "candiate1Response": candiate1Response.strip(),
            "candiate2Response": candiate2Response.strip(),
            "token_count": token_count
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "An error occurred during the debate"
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

