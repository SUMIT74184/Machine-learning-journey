#chain of thoughts prompting

import json
from openai import OpenAI

client = OpenAI(
    api_key="",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
SYSTEM_PROMPT = """
You are an expert AI assistant that solves user queries using step-by-step reasoning.

Workflow Rules:
- You must follow this sequence strictly:
  Start → PLAN (can repeat) → OUTPUT
- Only ONE step per response.
- Do NOT skip steps.
- Do NOT merge steps.

JSON Rules:
- Output MUST be valid JSON.
- Use ONLY the keys: step, content
- step must be one of: Start, PLAN, OUTPUT

Reasoning Rules:
- PLAN steps are internal reasoning.
- OUTPUT is the final user-visible answer.
- Do not add explanations outside JSON.

Output JSON Format:
{"step":"Start|PLAN|OUTPUT","content":"string"}

Refusal Rule:
- If the question is invalid, explain only in OUTPUT step.
"""


response = client.chat.completions.create(
    model="gemini-2.5-flash",
    response_format={"type": "json_object"},
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "34 + (2 * 4 - 93) / 3.5"
        },
        {
            "role": "assistant",
            "content": json.dumps({
                "step": "Start",
                "content": "Solve the given mathematical expression."
            })
        },
        {
            "role": "assistant",
            "content": json.dumps({
                "step": "PLAN",
                "content": "Apply order of operations (PEMDAS/BODMAS)."
            })
        },

         {
            "role": "assistant",
            "content": json.dumps({
                "step": "PLAN",
                "content":"First, evaluate the expression inside the parentheses: (2 * 4 - 93)."
            })
        },


        {
            "role": "assistant",
            "content": json.dumps({
             "step": "PLAN",
             "content": "1. Multiply 2 * 4.\\n2. Subtract 93 from the result.\\n3. Divide the result by 3.5.\\n4. Add 34 to the final result."

            })
        }



    ]
)

'{"step": "PLAN", '


print(response.choices[0].message)


# print(response.choices[0].message)


#alpaca style prompting

# import json
# from openai import OpenAI

# client = OpenAI(
#     api_key="AIzaSyCQnOAqe5BPnSXyrlGGzu36X8_P-ql3p60",
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# ALPACA_PROMPT = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

# ### Instruction:
# You are an expert AI assistant that solves user queries using step-by-step reasoning.

# Follow this workflow strictly:
# - Start → PLAN (can repeat) → OUTPUT
# - Only ONE step per response
# - Do NOT skip or merge steps

# Output valid JSON with keys: step, content
# - step must be: Start, PLAN, or OUTPUT
# - PLAN steps are internal reasoning
# - OUTPUT is the final answer

# Format: {"step":"Start|PLAN|OUTPUT","content":"string"}

# If the question is invalid, explain only in OUTPUT step.

# ### Input:
# 34 + (2 * 4 - 93) / 3.5

# ### Response:
# """

# response = client.chat.completions.create(
#     model="gemini-2.5-flash",
#     response_format={"type": "json_object"},
#     messages=[
#         {
#             "role": "user",
#             "content": ALPACA_PROMPT
#         }
#     ]
# )

# print(response.choices[0].message)