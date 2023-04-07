import json
import re
from call_ai_function import call_ai_function
from config import Config
cfg = Config()

def extract_json(text):
    try:
        json_start = text.index('{')
        json_end = text.rindex('}') + 1
        return text[json_start:json_end]
    except ValueError:
        return None

def fix_and_parse_json(json_str: str, try_to_fix_with_gpt: bool = True):
    json_schema = """
    {
    "command": {
        "name": "command name",
        "args":{
            "arg name": "value"
        }
    },
    "thoughts":
    {
        "text": "thought",
        "reasoning": "reasoning",
        "plan": "- short bulleted\n- list that conveys\n- long-term plan",
        "criticism": "constructive self-criticism",
        "speak": "thoughts summary to say to user"
    }
    }
    """

    try:
        json_str = json_str.replace('\t', '')
        return json.loads(json_str)
    except Exception as e:
        json_str = extract_json(json_str)
        if json_str is not None:
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
                return None
        else:
            print("No JSON found in the input string.")
            return None

# You can keep the fix_json function as it is.

def fix_json(json_str: str, schema: str, debug=False) -> str:
    # Try to fix the JSON using gpt:
    function_string = "def fix_json(json_str: str, schema:str=None) -> str:"
    args = [f"'''{json_str}'''", f"'''{schema}'''"]
    description_string = """Fixes the provided JSON string to make it parseable and fully complient with the provided schema.\n If an object or field specifed in the schema isn't contained within the correct JSON, it is ommited.\n This function is brilliant at guessing when the format is incorrect."""

    # If it doesn't already start with a "`", add one:
    if not json_str.startswith("`"):
      json_str = "```json\n" + json_str + "\n```"
    result_string = call_ai_function(
        function_string, args, description_string, model=cfg.fast_llm_model
    )
    if debug:
        print("------------ JSON FIX ATTEMPT ---------------")
        print(f"Original JSON: {json_str}")
        print("-----------")
        print(f"Fixed JSON: {result_string}")
        print("----------- END OF FIX ATTEMPT ----------------")
    try:
        json.loads(result_string) # just check the validity
        return result_string
    except:
        # Get the call stack:
        # import traceback
        # call_stack = traceback.format_exc()
        # print(f"Failed to fix JSON: '{json_str}' "+call_stack)
        return "failed"

