# Slackbot for GPT Chat

SlackBot Chat GPT is a language model app integrated into the Zircon's Slack workspace to enhance the team's communication and productivity. This SlackBot is designed to generate responses and engage in natural language conversations with users in the Slack channels, providing real-time assistance and automating tasks to streamline your workflow.

The bot is only configured to work properly in public and private channels but not in DMs or multi-person chats. It becomes easier when you want to post a question to a common group interest. Nonetheless, if you'd like to keep questions private, you can eventually create a private channel for yourself and ask there.

To trigger the bot, simply send `@Gpt Z` + *your question* in any private or public channel. The bot will take a few seconds and give you the answer you are looking for (hopefully) 😎

## Features

- Responds to user messages with GPT-3.5-turbo generated text
- Generates images with DALL-E based on user descriptions

## Prerequisites

- Python 3.6 or later
- OpenAI Python package
- Slack Bolt and Slack SDK Python packages
- Python-dotenv package
- Requests package

You can install the required Python packages using the following command:

<pre>
pip install openai slack-bolt slack-sdk python-dotenv requests
</pre>

## Slack App Setup
- Create a new Slack app at https://api.slack.com/apps.
- Set up bot scopes under "OAuth & Permissions":
<pre>
app_mentions:read
channels:history
chat:write
chat:write.public
files:write
groups:history
im:history
im:write
mpim:history
mpim:write
users:read
users:read.email
</pre>
Install the app to your Slack workspace and obtain the bot token and app token.
Add the bot to a channel or use it in a direct message.
## Configuration
Create a .env file in the project directory with the following variables:

<pre>
OPENAI_API_KEY=<your_openai_api_key>
SLACK_BOT_APP_TOKEN=<your_slack_app_token>
SLACK_API_KEY=<your_slack_bot_token>
</pre>
Replace <your_openai_api_key>, <your_slack_app_token>, and <your_slack_bot_token> with your corresponding API keys and tokens.

## Running the Bot
Execute the Python script to start the bot:

<pre>
python <your_script_name>.py
</pre>
Replace <your_script_name> with the name of the Python script containing the bot's code.

## Usage
To interact with the bot, mention the bot in a message within a channel it is added to or in a direct message.
To generate an image with DALL-E, send a message in the following format: 
<pre>
image: description
</pre>
## License
This project is licensed under the MIT License. See the LICENSE file for details.

