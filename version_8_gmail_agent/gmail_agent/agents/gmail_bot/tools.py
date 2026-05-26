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
    # 步骤 1：ADK 会在授权完成后自动注入 credential；没有授权就返回提示。
    if not credential or not credential.oauth2:
        return [{"error": "Authorization Required. Please click the Authorize button to proceed."}]

    # 步骤 2：把 ADK OAuth credential 转换成 Google API Client 可用的 Credentials。
    creds = Credentials(
        token=credential.oauth2.access_token,
        refresh_token=credential.oauth2.refresh_token,
    )

    # 步骤 3：创建 Gmail API service，后续所有 Gmail 请求都通过它发出。
    service = build('gmail', 'v1', credentials=creds)

    # 步骤 4：根据天数、发件人、关键词拼接 Gmail 搜索 query。
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

    # 步骤 5：先查询匹配邮件的 ID 列表，再逐封读取元数据。
    # Fetch list of message IDs
    results = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
    messages = results.get('messages', [])
    
    email_list = []
    for msg in messages:
        # 步骤 6：这里只读取 metadata 和 snippet，避免一次性暴露完整正文。
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
    # 步骤 1：读取正文同样需要 OAuth 授权，没有授权就让用户先授权。
    if not credential or not credential.oauth2:
        return "Authorization Required. Please click the Authorize button to proceed."

    # 步骤 2：构造 Gmail API client，并按 message_id 拉取完整邮件内容。
    creds = Credentials(
        token=credential.oauth2.access_token,
        refresh_token=credential.oauth2.refresh_token,
    )
    service = build('gmail', 'v1', credentials=creds)
    message = service.users().messages().get(userId='me', id=message_id, format='full').execute()

    # 步骤 3：优先提取 text/plain 正文；如果邮件结构简单或没有正文，则回退到 snippet。
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
