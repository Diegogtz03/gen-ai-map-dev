import asyncio
import time
import openai
from config import OPENAI_MODEL_NAME, MAX_TOKENS, TEMPERATURE, INDEX_K, MAIN_COLUMN
import src.prompt_repo as prompt_repo
import os


async def run_prompt(vectorstore, prompt, key):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    docs = await vectorstore.asimilarity_search(prompt, k=INDEX_K)
    context = "".join(doc.page_content for doc in docs)

    full_prompt = prompt_repo.rag.format(context=context, question=prompt)
    client = openai.AsyncClient()
    try:
        response = await client.chat.completions.create(
            model=OPENAI_MODEL_NAME,
            temperature=TEMPERATURE,
            messages=[
                {"role": "system", "content": "You're a very helpful assistant"},
                {"role": "user", "content": full_prompt},
            ],
        )
        return key, response.choices[0].message.content.replace("\n", "")
    except Exception as e:
        print(f"Error in OpenAI API call: {e}")
        return key, "Error"


async def run_chain_on(tool, vectorstore):
    start = time.perf_counter()

    prompts = prompt_repo.get_prompts(tool)

    try:
        tasks = [run_prompt(vectorstore, prompt, key) for key, prompt in prompts]
        responses = await asyncio.gather(*tasks)

        result = {MAIN_COLUMN: tool}
        for key, value in responses:
            result[key] = value

        print("LLM a-calls took: %s seconds", time.perf_counter() - start)
        return result
    except Exception as e:
        print("Error in run_chain_on: %s", e)
        return {MAIN_COLUMN: tool, "Error": str(e)}
