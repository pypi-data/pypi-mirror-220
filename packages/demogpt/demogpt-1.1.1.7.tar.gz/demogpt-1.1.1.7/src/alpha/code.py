import os
import re
from pprint import pprint
import json
os.environ["OPENAI_API_KEY"]="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"

from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
def getRes(system_template="", human_template="", **kwargs):
    prompts = []
    if system_template:
        prompts.append(SystemMessagePromptTemplate.from_template(system_template))
    if human_template:
        prompts.append(HumanMessagePromptTemplate.from_template(human_template))
    chat_prompt = ChatPromptTemplate.from_messages(prompts)
    return LLMChain(llm=llm, prompt=chat_prompt).run(**kwargs)

examples = """
=========================================
Instruction:Generate blog post from title.
Args: {{
"system_template":"You are a helpful assistant that generates a blog post from the title: {{title}}. Please provide some content.",
"template":"{{title}}",
"variety":"True"
}}
##########################################
Instruction:Implement language translation app
Args: {{
"system_template":"You are a helpful assistant that translates {{input_language}} to {{output_language}}.",
"template":"{{text}}",
"variety":"False"
}}
##########################################
Instruction:Generate animal name from animal
Args: {{
"system_template":"You are a helpful assistant that generates a name for an animal. You generate short answer.",
"template":"What is a good name for a {{animal}}?",
"variety":"True"
}}
##########################################
Instruction:Create programming related humor machine
Args: {{
"system_template":"You are a helpful assistant that generates a humor related to programming.",
"template":"",
"variety":"True"
}}
##########################################
Instruction:Create a math teacher.
Args: {{
"system_template":"You are a helpful assistant that solve any math problem",
"template":"Here is the math problem: {{math_problem}}",
"variety":"False"
}}
##########################################
Instruction:{instruction}
Args:
"""

stremalit_system_template = """
Transfer the python code to the interactive streamlit code to do the instruction.
Make the output fancy.
Rewrite the python code to generate full streamlit code
"""
stremalit_human_template="""
Instruction:{instruction}
Python Code:{code}
Streamlit Code:
"""

def getCode(
instruction = "Create an app that predicts the gender from country and name inforation"
):
    res = getRes(human_template=examples,instruction=instruction)
    templates = json.loads(res)

    variables = [var[1:-1] for var in re.findall("{\S+}", res)]
    args = ", ".join(variables)
    run_call = '{}'
    if len(variables) > 0:
        run_call = ", ".join([f"{var}={var}" for var in variables])
    
    temperature = 0 if templates.get("variety","False") == "False" else 0.7

    code =f"""
    from langchain import LLMChain
    from langchain.chat_models import ChatOpenAI
    from langchain.prompts.chat import (ChatPromptTemplate,
                                        HumanMessagePromptTemplate,
                                        SystemMessagePromptTemplate)

    def generate({args}):
        chat = ChatOpenAI(
            temperature={temperature}
        )
        system_template = {templates['system_template']}
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_template = {templates['template']}
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        chain = LLMChain(llm=chat, prompt=chat_prompt)
        result = chain.run({run_call})
        return result                                 
    """

    streamlit_code = getRes(system_template = stremalit_system_template,
                            human_template=stremalit_human_template,
                            instruction=instruction,
                            code=code)
    return streamlit_code

__all__ = ['getCode']