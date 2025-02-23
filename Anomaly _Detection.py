def detect_anomalies(text):
    """Uses LLaMA 3 to analyze and flag risks in legal/financial documents"""
    prompt = f"Analyze the following text and detect financial or legal risks. Flag anomalies:\n\n{text}\n\nOutput in JSON format."
    output = llm(prompt)
    return json.loads(output["choices"][0]["text"])
