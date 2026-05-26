# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from typing import Any, Dict, List, Optional
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.adk.auth.auth_credential import AuthCredential

def list_gmail_messages(
    credential: Optional[AuthCredential] = None,
    days: int = 1,
    sender: str = None,
    keyword: str = None,
    max_results: int = 10
) -> List[Dict[str, Any]]:
    """
    Fetches a list of emails from Gmail based on criteria.

    Args:
        credential: The OAuth2 credential provided by ADK (automatically injected by AuthenticatedFunctionTool).
        days: Number of days back to search (default 1).
        sender: Filter by sender email (optional).
        keyword: Search keyword in subject or body (optional).
        max_results: Maximum number of emails to return (default 10).

    Returns:
        A list of dictionaries containing email metadata (id, subject, from, date, snippet).
    """
    if not credential or not credential.oauth2:
        return [{"error": "Authorization Required. Please click the Authorize button to proceed."}]
        
    creds = Credentials(
        token=credential.oauth2.access_token,
        refresh_token=credential.oauth2.refresh_token,
    )
    
    service = build('gmail', 'v1', credentials=creds)
    
    # Build the query string
    query_parts = []
    if days:
        date_threshold = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime('%Y/%m/%d')
        query_parts.append(f"after:{date_threshold}")
    if sender:
        query_parts.append(f"from:{sender}")
    if keyword:
        query_parts.append(keyword)
        
    query = " ".join(query_parts)

    # Fetch list of message IDs
    results = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
    messages = results.get('messages', [])
    
    email_list = []
    for msg in messages:
        # Get details for each message
        m = service.users().messages().get(userId='me', id=msg['id'], format='metadata', 
                                          metadataHeaders=['Subject', 'From', 'Date']).execute()
        headers = m.get('payload', {}).get('headers', [])
        
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")
        from_email = next((h['value'] for h in headers if h['name'] == 'From'), "Unknown")
        date_sent = next((h['value'] for h in headers if h['name'] == 'Date'), "Unknown")
        snippet = m.get('snippet', '')
        
        email_list.append({
            "id": msg['id'],
            "subject": subject,
            "from": from_email,
            "date": date_sent,
            "snippet": snippet
        })
    
    return email_list

def get_message_content(message_id: str, credential: Optional[AuthCredential] = None) -> str:
    """
    Fetches the full body of a specific email message.

    Args:
        message_id: The unique ID of the Gmail message.
        credential: The OAuth2 credential provided by ADK (automatically injected by AuthenticatedFunctionTool).

    Returns:
        The text content of the email.
    """
    if not credential or not credential.oauth2:
        return "Authorization Required. Please click the Authorize button to proceed."
        
    creds = Credentials(
        token=credential.oauth2.access_token,
        refresh_token=credential.oauth2.refresh_token,
    )
    service = build('gmail', 'v1', credentials=creds)
    message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
    
    parts = message.get('payload', {}).get('parts', [])
    body = ""
    
    # Simple extraction of plain text body
    if not parts:
        body = message.get('snippet', '')
    else:
        for part in parts:
            if part['mimeType'] == 'text/plain':
                import base64
                data = part.get('body', {}).get('data', '')
                if data:
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
                    break
    
    if not body:
        body = message.get('snippet', '(No body content found)')
        
    return body
