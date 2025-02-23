import google.generativeai as genai

genai.configure(api_key="AIzaSyAZw_IQd8zSxkxjQ2ni-dVZnHFQ48qUi2o")

model = genai.GenerativeModel("gemini-pro")
response = model.generate_content("Tell me about threat zone detection in disaster-prone areas.")

print(response.text)
