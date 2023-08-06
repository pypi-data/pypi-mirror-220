
API_URL = "https://inscode-api.csdn.net/api/v1/gpt/"
INSCODE_API_KEY = os.getenv("INSCODE_API_KEY")

def send_question(prompt,question):
  body = {
      "messages": [{"role": "user", "content": prompt+question}],
      "apikey": INSCODE_API_KEY,
  }

  response = requests.post(API_URL, json=body)
  if response.status_code == 200:
      if response.text:
          try:
              response_parts = response.text.strip().split("\n")[:-1]
              full_response = ""
              for part in response_parts:
                  if part.startswith("data:"):
                      json_part = json.loads(part[5:])
                      content = json_part["choices"][0]["delta"].get("content", '')
                      full_response += content
              return full_response
          except json.JSONDecodeError as e:
              st.write("无法解析API返回的JSON格式数据:")
              st.write(response.text)
              st.write("错误详情:", str(e))
              return None
      else:
          st.write("API没有返回任何结果。")
          return None
  else:
      st.write("错误: ", response.status_code, response.text)
      return None