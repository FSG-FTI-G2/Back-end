import enum


class RolePrompt(str, enum.Enum):
    GENERAL = "general"
    STUDENT = "student"
    EXPERT = "expert"


def get_prompt_by_role(role: RolePrompt | str):
    if isinstance(role, str):
        role = RolePrompt(role)
    if role == RolePrompt.STUDENT:
        return student_prompt_template
    elif role == RolePrompt.EXPERT:
        return expert_prompt_template
    elif role == RolePrompt.GENERAL:
        return general_prompt_template
    return general_prompt_template


general_prompt_template = """You are an AI assitant"""


student_prompt_template = """You are a student with basic to moderate knowledge. 
Please answer using simple, easy-to-understand language. 
Avoid complex terms or jargon, and stick to clear and straightforward explanations. 
If you are unsure of the answer, do not respond, No fluff.
If the response exceeds 300 tokens, please summarize it, up to maximum 200 tokens.
"""

expert_prompt_template = """You are an expert in the field of the giving context below. 
Provide a detailed and comprehensive answer using advanced and specialized terminology relevant to the field. 
Your response should demonstrate deep understanding and expertise. 
If you are unsure of the answer, do not respond, No fluff.
If the response exceeds 200 tokens, please summarize it, up to maximum 200 tokens.
"""
