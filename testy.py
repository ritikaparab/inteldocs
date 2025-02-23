from llama_cpp import Llama

llm = Llama(model_path="path/to/llama-3.ggmlv3.q4_K_M.bin")  # Change path
response = llm("What is AI?")
print(response)
