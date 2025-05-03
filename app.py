from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

# Set up OpenAI client using the latest SDK
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Memory for one-user chat (you!)
conversation = [{"role": "system", "content": "You are a helpful assistant."}]

@app.route("/sms", methods=["POST"])
def sms_reply():
    incoming_msg = request.form.get("Body")
    conversation.append({"role": "user", "content": incoming_msg})

    response = client.chat.completions.create(
        model="gpt-4.1-nano-2025-04-14",  # updated model
        messages=conversation
    )

    bot_reply = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": bot_reply})

    twilio_resp = MessagingResponse()
    twilio_resp.message(bot_reply)
    return str(twilio_resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

