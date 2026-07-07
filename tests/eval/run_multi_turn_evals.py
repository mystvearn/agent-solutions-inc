import asyncio
import base64
import os
from google.genai import types
from google.adk.runners import InMemoryRunner
from app.agent import app

scenarios = [
    {
        "name": "Scenario 1: Uploading wrong document (Manufacturing)",
        "turns": [
            "I am a manufacturing company. I want to optimize our quality control process.",
            "Here is our quality control process document: 1. Post a job opening on LinkedIn. 2. Review candidate resumes. 3. Conduct HR screening interview. 4. Send offer letter. (Wait, this is an HR process!)"
        ]
    },
    {
        "name": "Scenario 2: Doesn't know how to structure (Logistics)",
        "turns": [
            "I have a logistics company. I want to optimize warehouse inventory checking.",
            "I don't know how to structure the procedure or what details you need. Can you help?"
        ]
    },
    {
        "name": "Scenario 3: New company without baseline (E-commerce)",
        "turns": [
            "I just started a new e-commerce startup. I have no existing processes or baseline. We need an AI agent for customer order returns.",
            "Yes, our main goal is just to automate returns so we don't have to hire a support team yet. We use Shopify."
        ]
    }
]

async def run_scenarios():
    for scenario in scenarios:
        print(f"\n{'='*60}\n{scenario['name']}\n{'='*60}")
        runner = InMemoryRunner(app=app)
        session = await runner.session_service.create_session(app_name="app", user_id="eval_user")
        
        for turn_idx, user_input in enumerate(scenario["turns"]):
            print(f"\n--- Turn {turn_idx + 1} ---")
            
            parts = []
            if isinstance(user_input, str):
                parts.append(types.Part.from_text(text=user_input))
                print(f"User: {user_input}")
            else:
                parts.append(types.Part.from_text(text=user_input["text"]))
                print(f"User: {user_input['text']} (Attached file: {user_input['file']})")
                
                # Load the file
                file_path = os.path.join("/Users/anhduynguyen/dev/5day-intensive-agent-course/capstone-project", user_input["file"])
                with open(file_path, "rb") as f:
                    file_data = f.read()
                parts.append(types.Part.from_bytes(data=file_data, mime_type=user_input["mime_type"]))
            
            content = types.Content(role="user", parts=parts)
            
            # Send to agent
            async for event in runner.run_async(
                user_id="eval_user",
                session_id=session.id,
                new_message=content
            ):
                if event.content and event.content.parts:
                    agent_text = event.content.parts[0].text
                    print(f"\nAgent: {agent_text}")
                elif event.output and isinstance(event.output, dict) and event.output.get("status") == "wait":
                    pass

if __name__ == "__main__":
    asyncio.run(run_scenarios())
