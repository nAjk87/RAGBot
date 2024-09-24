import json
from openai import AsyncOpenAI, AsyncAssistantEventHandler
from typing_extensions import override
from get_recommendations import get_question_embedding, get_recommendations
import pprint


client = AsyncOpenAI()


class RagBotEventHandler(AsyncAssistantEventHandler):

    def handle_requires_action(self, data, run_id):
        tool_outputs = []

        for tool in data.required_action.submit_tool_outputs.tool_calls:
            if tool.function.name == "get_recommendations":

                question = json.loads(tool.function.arguments)["question"]

                question_embedding = get_question_embedding(question)
                answers = get_recommendations(question_embedding)
                answers_str = pprint.pformat(answers)
                tool_outputs.append({"tool_call_id": tool.id, "output": answers_str})

        # Submit all tool_outputs at the same time
        return self.submit_tool_outputs(tool_outputs, run_id)

    def submit_tool_outputs(self, tool_outputs, run_id):
        # Use the submit_tool_outputs_stream helper
        return client.beta.threads.runs.submit_tool_outputs_stream(
            thread_id=self.current_run.thread_id,
            run_id=run_id,
            tool_outputs=tool_outputs,
            event_handler=AsyncAssistantEventHandler(),
        )
