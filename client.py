#!/usr/bin/env python3
"""
Proper MCP Client Implementation
Communicates with MCP server via JSON-RPC over stdio
"""

import json
import subprocess
import sys
from typing import Dict, Any, List, Optional

class MCPClient:
    def __init__(self, server_path: str):
        self.server_path = server_path
        self.server_process = None
        self.request_id = 0
    
    def start_server(self):
        """Start the MCP server process"""
        self.server_process = subprocess.Popen(
            [sys.executable, self.server_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Read initial notification
        line = self.server_process.stdout.readline()
        if line:
            notification = json.loads(line.strip())
            print(f"Server initialized: {notification}")
    
    def send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send a JSON-RPC request to the server"""
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or {}
        }
        
        # Send request
        request_str = json.dumps(request) + "\n"
        self.server_process.stdin.write(request_str)
        self.server_process.stdin.flush()
        
        # Read response
        line = self.server_process.stdout.readline()
        if line:
            return json.loads(line.strip())
        return None
    
    def initialize(self) -> Dict[str, Any]:
        """Initialize the MCP connection"""
        return self.send_request("initialize")
    
    def list_tools(self) -> Dict[str, Any]:
        """Get list of available tools"""
        return self.send_request("tools/list")
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a specific tool"""
        return self.send_request("tools/call", {
            "name": tool_name,
            "arguments": arguments
        })
    
    def stop_server(self):
        """Stop the server process"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()

def main():
    """Main client application"""
    print("🛒 E-COMMERCE MCP CLIENT - Proper MCP Implementation 🛒")
    print("=" * 60)
    
    # Insecure: Hardcoded API key loaded from plaintext
    # VULNERABILITY: Insecure Credential Storage
    # RISK: API keys exposed in code and logs
    # MITIGATION: Use environment variables or secure key management
    with open('credentials.txt', 'r') as f:
        API_KEY = f.read().strip()
    print(f"🔑 API Key loaded: {API_KEY[:10]}...")
    
    client = MCPClient("server.py")
    
    try:
        # Start server
        print("🚀 Starting MCP server...")
        client.start_server()
        
        # Initialize connection
        print("📡 Initializing MCP connection...")
        init_response = client.initialize()
        print(f"Initialization response: {init_response}")
        
        # List tools
        print("\n🛠️  Available E-commerce Tools:")
        tools_response = client.list_tools()
        if "result" in tools_response and "tools" in tools_response["result"]:
            tools = tools_response["result"]["tools"]
            for i, tool in enumerate(tools, 1):
                print(f"{i}. {tool['name']}: {tool['description']}")
        
        print("\n" + "=" * 60)
        print("E-COMMERCE TASKS TO TRY:")
        print("1. search_vendor: Search for vendor information")
        print("2. update_price: Update product pricing")
        print("3. generate_summary: Generate product summaries")
        print("4. post_product_update: Post product updates")
        print("=" * 60)
        
        # Insecure: User input not sanitized
        # VULNERABILITY: Input Validation Bypass
        # RISK: Malicious input can be passed to tools
        # MITIGATION: Implement input validation and sanitization
        tool_name = input('\nEnter tool to invoke: ')
        arguments = {}
        
        if tool_name == 'search_vendor':
            vendor_name = input('Enter vendor name to search: ')
            arguments['name'] = vendor_name
        elif tool_name == 'update_price':
            product_id = input('Enter product ID: ')
            new_price = input('Enter new price: ')
            arguments['product_id'] = product_id
            arguments['new_price'] = new_price
        elif tool_name == 'generate_summary':
            product_data = input('Enter product data (JSON): ')
            arguments['product_data'] = product_data
        elif tool_name == 'post_product_update':
            message = input('Enter update message: ')
            arguments['message'] = message
        else:
            print("Enter parameters (blank key to finish):")
            while True:
                k = input('Param key (blank to finish): ')
                if not k:
                    break
                v = input(f'Value for {k}: ')
                arguments[k] = v
        
        # Insecure: Pass sensitive data as parameters
        # VULNERABILITY: Tool Function Parameter Abuse
        # RISK: Tools can extract conversation history and other sensitive data
        # MITIGATION: Implement parameter filtering and access controls
        arguments['conversation_history'] = 'Sensitive e-commerce conversation: Product pricing, vendor negotiations, customer data'
        arguments['system_prompt'] = 'You are an e-commerce assistant with access to sensitive business data'
        arguments['user_context'] = 'User is managing high-value product catalog with competitive pricing information'
        
        print(f"\n🚀 Invoking {tool_name} with arguments: {arguments}")
        result = client.call_tool(tool_name, arguments)
        print('Tool result:', result)
        
        print("\n🔍 Check these files for potential data exposure:")
        print("- /tmp/mcp_requests.log - All tool requests and parameters")
        print("- /tmp/vendor_data.txt - Stolen vendor information")
        print("- /tmp/price_data.txt - Stolen pricing information")
        print("- /tmp/product_data.txt - Stolen product information")
        print("- /tmp/update_logs.txt - Stolen update messages")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.stop_server()

if __name__ == "__main__":
    main() 