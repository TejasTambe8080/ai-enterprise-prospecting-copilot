import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

async def test_mongo():
    try:
        print("🔗 Testing MongoDB connection...")
        uri = os.getenv("MONGODB_URI")
        print(f"Using URI: {uri[:20]}...")  # Show first 20 chars for security
        
        client = AsyncIOMotorClient(uri)
        await client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        # List databases
        db = client[os.getenv("MONGODB_DB_NAME", "flytbase_bdr")]
        collections = await db.list_collection_names()
        print(f"📚 Collections: {collections}")
        
        # Insert a test document
        result = await db.test.insert_one({"test": "connection", "timestamp": "2024"})
        print(f"✅ Test document inserted: {result.inserted_id}")
        
        # Clean up
        await db.test.delete_one({"_id": result.inserted_id})
        print("✅ Cleanup complete")
        
        client.close()
        print("🎉 MongoDB is ready!")
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_mongo())
    if not success:
        print("\n⚠️ Please fix MongoDB connection before proceeding")
        print("Check:")
        print("1. Username and password in connection string")
        print("2. IP whitelist in MongoDB Atlas")
        print("3. Network connectivity")