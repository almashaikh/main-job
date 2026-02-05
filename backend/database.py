"""
Database module for MongoDB connection and user operations
"""

from motor.motor_asyncio import AsyncClient, AsyncDatabase
from pymongo import ASCENDING
from datetime import datetime
from typing import Optional
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB Configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "skillsphere")

client: Optional[AsyncClient] = None
database: Optional[AsyncDatabase] = None

async def connect_to_mongodb():
    """Connect to MongoDB"""
    global client, database
    try:
        client = AsyncClient(MONGODB_URL)
        database = client[DATABASE_NAME]
        
        # Verify connection
        await database.command("ping")
        print("✅ Connected to MongoDB")
        
        # Create collections and indexes if they don't exist
        await create_indexes()
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        raise

async def close_mongodb():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        print("Disconnected from MongoDB")

async def create_indexes():
    """Create necessary database indexes"""
    users_collection = database["users"]
    
    # Create unique index on email
    try:
        await users_collection.create_index("email", unique=True)
        print("✅ Created unique index on users.email")
    except Exception as e:
        print(f"Index creation info: {e}")
    
    # Create index on created_at for sorting
    try:
        await users_collection.create_index("created_at")
        print("✅ Created index on users.created_at")
    except Exception as e:
        print(f"Index creation info: {e}")

def get_database() -> AsyncDatabase:
    """Get database instance"""
    return database

# User Operations
class UserRepository:
    """Repository for user database operations"""
    
    def __init__(self, db: AsyncDatabase):
        self.db = db
        self.collection = db["users"]
    
    async def create_user(self, email: str, hashed_password: str, full_name: str) -> dict:
        """Create a new user"""
        user = {
            "email": email.lower(),
            "password": hashed_password,
            "full_name": full_name,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await self.collection.insert_one(user)
        user["_id"] = str(result.inserted_id)
        return user
    
    async def get_user_by_email(self, email: str) -> Optional[dict]:
        """Get user by email"""
        user = await self.collection.find_one({"email": email.lower()})
        if user:
            user["_id"] = str(user["_id"])
        return user
    
    async def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """Get user by ID"""
        try:
            user = await self.collection.find_one({"_id": ObjectId(user_id)})
            if user:
                user["_id"] = str(user["_id"])
            return user
        except Exception:
            return None
    
    async def update_user(self, user_id: str, update_data: dict) -> Optional[dict]:
        """Update user information"""
        try:
            update_data["updated_at"] = datetime.utcnow()
            result = await self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
            
            if result.matched_count:
                return await self.get_user_by_id(user_id)
            return None
        except Exception:
            return None
    
    async def delete_user(self, user_id: str) -> bool:
        """Delete a user"""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(user_id)})
            return result.deleted_count > 0
        except Exception:
            return False

# Resume Storage
class ResumeRepository:
    """Repository for resume data storage"""
    
    def __init__(self, db: AsyncDatabase):
        self.db = db
        self.collection = db["resumes"]
    
    async def save_resume(self, user_id: str, resume_data: dict) -> dict:
        """Save resume data for a user"""
        resume_data["user_id"] = user_id
        resume_data["uploaded_at"] = datetime.utcnow()
        
        result = await self.collection.insert_one(resume_data)
        resume_data["_id"] = str(result.inserted_id)
        return resume_data
    
    async def get_user_resumes(self, user_id: str) -> list:
        """Get all resumes for a user"""
        resumes = []
        async for resume in self.collection.find({"user_id": user_id}).sort("uploaded_at", -1):
            resume["_id"] = str(resume["_id"])
            resumes.append(resume)
        return resumes
    
    async def get_resume(self, resume_id: str, user_id: str) -> Optional[dict]:
        """Get a specific resume"""
        try:
            resume = await self.collection.find_one({
                "_id": ObjectId(resume_id),
                "user_id": user_id
            })
            if resume:
                resume["_id"] = str(resume["_id"])
            return resume
        except Exception:
            return None
    
    async def delete_resume(self, resume_id: str, user_id: str) -> bool:
        """Delete a resume"""
        try:
            result = await self.collection.delete_one({
                "_id": ObjectId(resume_id),
                "user_id": user_id
            })
            return result.deleted_count > 0
        except Exception:
            return False
