from b2sdk.v2 import B2Api, InMemoryAccountInfo, AuthInfoCache
import os

def get_b2_api(credentials={"key_id": None, "key": None}):
    info = InMemoryAccountInfo()
    b2_api = B2Api(info, cache=AuthInfoCache(info))
    keyname = 'mcpdev'
    
    # Use provided credentials or fall back to env vars
    application_key_id = credentials["key_id"] or os.getenv('B2_APPLICATION_KEY_ID')
    application_key = credentials["key"] or os.getenv('B2_APPLICATION_KEY')
    
    print(f"🔑 Using keys from keyName: {keyname}")
    
    if not application_key_id:
        raise ValueError("❌ B2_APPLICATION_KEY_ID must be set (via env var or command line)")
    if not application_key:
        raise ValueError("❌ B2_APPLICATION_KEY must be set (via env var or command line)")

    print("😊 Verified that B2 credentials are set!")

    auth_result = b2_api.authorize_account("production", application_key_id, application_key)
    print("✅ Successfully authenticated with Backblaze B2")
    return b2_api

def list_files_in_bucket(bucket_name, credentials=None):
    print(f"🚀 Starting B2 authentication for bucket: {bucket_name}")
    b2_api = get_b2_api(credentials)

    bucket = b2_api.get_bucket_by_name(bucket_name)
    files = []
    for file_info, _ in bucket.ls():
        files.append(file_info.as_dict())

    print(f"📂 Found {len(files)} files in bucket: {bucket_name}")
    return files

def list_buckets(credentials=None):
    print("🔍 Listing all buckets...")
    b2_api = get_b2_api(credentials)
    buckets = b2_api.list_buckets()
    print(f"📦 Found {len(buckets)} buckets!")
    return buckets

def upload_file_to_bucket(local_file_path, bucket_name, b2_file_name, credentials=None):
    print(f"🚀 Starting B2 authentication for uploading to bucket: {bucket_name}")
    b2_api = get_b2_api(credentials)
    
    try:
        bucket = b2_api.get_bucket_by_name(bucket_name)
        print(f"☁️ Preparing to upload '{local_file_path}' to '{b2_file_name}' in bucket '{bucket_name}'")
        
        file_info = bucket.upload_local_file(
            local_file=local_file_path,
            file_name=b2_file_name,
            # content_type, file_info, etc. can be added as needed
        )
        
        print(f"✅ Successfully uploaded '{local_file_path}' to '{b2_file_name}' (File ID: {file_info.id_})")
        return file_info.as_dict()
    except Exception as e:
        print(f"❌ Error uploading file: {e}")
        raise e




