import asyncio
import json
from google.genai import types
from google.adk.runners import InMemoryRunner
from app.agent import app

async def main():
    with open("tests/eval/datasets/industry_eval.json", "r") as f:
        dataset = json.load(f)
    
    for case in dataset["eval_cases"]:
        print(f"\n{'='*50}\nEvaluating Case: {case['eval_case_id']}")
        prompt_text = case["prompt"]["parts"][0]["text"]
        print(f"Prompt: {prompt_text}\n")
        
        runner = InMemoryRunner(app=app)
        session = await runner.session_service.create_session(app_name="app", user_id="test_user")
        
        async for partial in runner.run_async(
            user_id="test_user",
            session_id=session.id, 
            new_message=types.Content(role="user", parts=[types.Part.from_text(text=prompt_text)])
        ):
            if partial.content:
                print("Agent Response:")
                print(partial.content.parts[0].text)
            if partial.actions and partial.actions.requested_tool_confirmations:
                 # In case it asks for input
                 pass

if __name__ == "__main__":
    asyncio.run(main())
