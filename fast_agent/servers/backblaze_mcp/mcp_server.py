from mcp.server.fastmcp import FastMCP
from backblaze_operations import *
from typing import List
import argparse
import sys

from datetime import datetime

input_args = {
    "key_id": None,
    "key": None,
    "debug_level": "console"
}

def print_to_file(message):
    timestamp = datetime.now().isoformat()
    log_output = f"{timestamp} - {message}"
    if input_args["debug_level"] == "file":
        with open("logs/mcp_server.log", "a") as file:
            file.write(f"{log_output}\n")

    print(f"{log_output}")

def clear_log_file():
    with open("logs/mcp_server.log", "w") as file:
        file.truncate(0)

clear_log_file()
print_to_file("Cleared log file")
print_to_file("Loading MCP server...")

def parse_args():
    parser = argparse.ArgumentParser(description='Backblaze MCP Server')
    parser.add_argument('--key-id', help='Backblaze B2 Application Key ID')
    parser.add_argument('--key', help='Backblaze B2 Application Key')
    return parser.parse_args()

mcp = FastMCP("Backblaze MCP")


print_to_file("Defining tool: list_all_available_buckets")
@mcp.tool()
def list_all_available_buckets() -> List[str]:
    """List all buckets"""
    print_to_file("Executing tool: list_all_available_buckets")
    return list_buckets(credentials=input_args)

print_to_file("Defining tool: list_public_bucket_files")
@mcp.tool()
def list_public_bucket_files(bucket_name: str) -> List[str]:
    """List all files in a public Backblaze B2 bucket"""
    print_to_file(f"Executing tool: list_public_bucket_files with bucket_name: {bucket_name}")
    return list_files_in_bucket(bucket_name, credentials=input_args)

print_to_file("Defining tool: upload_local_file")
@mcp.tool()
def upload_local_file_to_bucket(local_file_path: str, bucket_name: str, b2_file_name: str) -> dict:
    """Upload a local file to a specific Backblaze B2 bucket.

    Args:
        local_file_path: The path to the local file to upload.
        bucket_name: The name of the target B2 bucket.
        b2_file_name: The desired name for the file within the B2 bucket.
    """
    print_to_file(f"Executing tool: upload_local_file with local_file_path: '{local_file_path}', bucket_name: '{bucket_name}', b2_file_name: '{b2_file_name}'")
    return upload_file_to_bucket(local_file_path, bucket_name, b2_file_name, credentials=input_args)

if __name__ == "__main__":
    print_to_file("Starting MCP server...")
    parsed_args = parse_args()
    input_args["key_id"] = parsed_args.key_id
    input_args["key"] = parsed_args.key

    print_to_file(f"Input args: {input_args}")

    mcp.run()