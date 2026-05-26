# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv

from google.adk.agents.llm_agent import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.auth.auth_credential import AuthCredential, AuthCredentialTypes, OAuth2Auth
from google.adk.auth.auth_tool import AuthConfig
from google.adk.tools.authenticated_function_tool import AuthenticatedFunctionTool
from fastapi.openapi.models import OAuth2, OAuthFlows, OAuthFlowAuthorizationCode

from .tools import list_gmail_messages, get_message_content

# Load environment variables
load_dotenv()

OAUTH_CLIENT_ID = os.getenv("OAUTH_CLIENT_ID")
OAUTH_CLIENT_SECRET = os.getenv("OAUTH_CLIENT_SECRET")

# Check if environment variables are set
if not OAUTH_CLIENT_ID or not OAUTH_CLIENT_SECRET:
    logging.error("OAUTH_CLIENT_ID or OAUTH_CLIENT_SECRET is missing from environment variables.")
    # In a real app, you might want to exit or handle this more gracefully
    # sys.exit(1)

# Define Gmail Authentication Configuration
gmail_auth_config = AuthConfig(
    auth_scheme=OAuth2(
        flows=OAuthFlows(
            authorizationCode=OAuthFlowAuthorizationCode(
                authorizationUrl="https://accounts.google.com/o/oauth2/auth",
                tokenUrl="https://oauth2.googleapis.com/token",
                scopes={
                    "https://www.googleapis.com/auth/gmail.readonly": "Read your emails and metadata",
                },
            )
        )
    ),
    raw_auth_credential=AuthCredential(
        auth_type=AuthCredentialTypes.OAUTH2,
        oauth2=OAuth2Auth(
            client_id=OAUTH_CLIENT_ID,
            client_secret=OAUTH_CLIENT_SECRET,
        ),
    ),
    credential_key="gmail_api_auth" # Essential for ADK Web UI to track authentication state
)

def update_time(callback_context: CallbackContext):
    """Callback to provide current timestamp to the agent."""
    now = datetime.now()
    callback_context.state["current_time"] = now.strftime("%Y-%m-%d %H:%M:%S")

# Read instruction from file
instruction_path = os.path.join(os.path.dirname(__file__), "instruction.txt")
with open(instruction_path, "r") as f:
    instruction_text = f.read()

root_agent = Agent(
    model="gemini-2.0-flash",
    name="gmail_bot",
    description="安全的中文 Gmail 助手，可获取、筛选和总结邮件。",
    instruction=instruction_text,
    tools=[
        AuthenticatedFunctionTool(
            func=list_gmail_messages,
            auth_config=gmail_auth_config
        ),
        AuthenticatedFunctionTool(
            func=get_message_content,
            auth_config=gmail_auth_config
        ),
    ],
    before_agent_callback=update_time,
)
