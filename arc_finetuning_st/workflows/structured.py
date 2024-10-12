import litellm
from litellm import completion,Router
import instructor
from pydantic import BaseModel
from typing import Any
import json
import os
import openai
from llama_index.core.prompts import PromptTemplate

def astruct_predict(
        output_cls: BaseModel,
        prompt: PromptTemplate,
        **prompt_args: Any,
    ) -> BaseModel:
        """Async Structured predict.

        Args:
            output_cls (BaseModel):
                Output class to use for structured prediction.
            prompt (PromptTemplate):
                Prompt template to use for structured prediction.
            prompt_args (Any):
                Additional arguments to format the prompt with.

        Returns:
            BaseModel: The structured prediction output.

        Examples:
            ```python
            from pydantic import BaseModel

            class Test(BaseModel):
                \"\"\"My test class.\"\"\"
                name: str

            from llama_index.core.prompts import PromptTemplate

            prompt = PromptTemplate("Please predict a Test with a random name related to {topic}.")
            output = await llm.astructured_predict(Test, prompt, topic="cats")
            print(output.name)
            ```
        """
        models = openai.OpenAI().models.list()
        for model in models.data:
            print(f"Model ID: {model.id}")
            print(f"Owned by: {model.owned_by}")
            # Access other properties like 'permission' if needed
            print("-" * 20) 
        #client = instructor.from_litellm(completion,  mode=instructor.Mode.JSON)
        client = instructor.patch(
            Router(
                model_list=[
                    {
                        "model_name": "gpt-4o", 
                        "litellm_params": {  # params for litellm completion/embedding call - e.g.: https://github.com/BerriAI/litellm/blob/62a591f90c99120e1a51a8445f5c3752586868ea/litellm/router.py#L111
                            "model": "sambanova/Meta-Llama-3.1-405B-Instruct",
                            "api_key": os.getenv("SAMBANOVA_API_KEY"),
                            "api_base": os.getenv("OPENAI_BASE_URL"),
                        },
                    }
                ]
            )
        )
        litellm.set_verbose = True
        #print(f"promt: {prompt}")
        prediction = client.chat.completions.create(
            model="gpt-4o",
            response_model=output_cls,
            messages=[
                {"role": "user", "content": prompt.template},
            ]
        )
            
        

        assert isinstance(prediction, output_cls)
        return prediction