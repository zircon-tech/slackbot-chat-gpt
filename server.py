import os
import openai
import requests
from io import BytesIO
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from slack_bolt import App
from dotenv import load_dotenv

load_dotenv()


# NEEDED Environment Variables
openai_api_key = os.getenv('OPENAI_API_KEY')
slack_app_token = os.getenv('SLACK_BOT_APP_TOKEN')
slack_bot_token = os.getenv('SLACK_API_KEY')
# Optional Environment variables
openai_engine = 'gpt-3.5-turbo'
openai_max_tokens = int('1024')
openai_ack_msg = "Hey there! :robot_face: I'm on it!"
openai_reply_msg = "Here you go: \n"

# Event API & Web API
app = App(token=slack_bot_token)
client = WebClient(slack_bot_token)

def generate_image_url(prompt):
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "image-alpha-001",
        "prompt": prompt,
        "num_images": 1,
        "size":"256x256",
        "response_format": "url"
    }

    response = requests.post("https://api.openai.com/v1/images/generations", json=data, headers=headers)
    response.raise_for_status()

    return response.json()["data"][0]["url"]

# This gets activated when the bot is tagged in a channel
@app.event("app_mention")
def handle_message_events(body, logger):
    # Log message
    print(str(body["event"]["text"]).split(">")[1])

    # Create prompt for ChatGPT
    message_text = str(body["event"]["text"]).split(">")[1].strip()

    # Let thre user know that we are busy with the request 
    response = client.chat_postMessage(channel=body["event"]["channel"], 
                                       thread_ts=body["event"]["event_ts"],
                                       text=f"{openai_ack_msg}")

    # Check if the message starts with "image:"
    if message_text.startswith("image:"):
        print("Generating image ...")
        image_description = message_text[len("image:"):].strip()

        # Generate the image URL
        try:
            image_url = generate_image_url(image_description)
            openai_reply_msg = f"Here's an image based on your description:"

            # Download the image
            image_data = requests.get(image_url).content
            image_file = BytesIO(image_data)

            # Upload the image to Slack
            response = client.files_upload(
                channels=body["event"]["channel"],
                thread_ts=body["event"]["event_ts"],
                file=image_file,
                filename=f"{image_description}.png",
                title=f"{image_description}",
                initial_comment=openai_reply_msg,
            )
            return
        except Exception as e:
            openai_reply_msg = f"Sorry, an error occurred while generating the image: {str(e)}"

    else:
        print("Generating text response ...")
        # Check ChatGPT
        openai.api_key = openai_api_key

        if openai_engine.startswith('gpt-3.'):
            response = openai.ChatCompletion.create(
                model=openai_engine,
                max_tokens=openai_max_tokens,
                stop=None,
                temperature=0.5,
                messages=[
                    {"role": "user", "content": f"{message_text}"},
                ],
            ).choices[0].message.content

        else:
            response = openai.Completion.create(
                engine=openai_engine,
                prompt=message_text,
                max_tokens=openai_max_tokens,
                n=1,
                stop=None,
                temperature=0.5).choices[0].text
        
        openai_reply_msg = f"Here you go: \n{response}"

    print("Replying to the thread")

    # Reply to thread
    response_reply = client.chat_postMessage(
        channel=body["event"]["channel"],
        thread_ts=body["event"]["event_ts"],
        text=f"{openai_reply_msg}",
    )

    print("Done")

@app.event("message")
def handle_message_events(body, logger):
    print("General message received")
    print(body)


if __name__ == "__main__":
    handler = SocketModeHandler(app, slack_app_token)
    handler.start()
