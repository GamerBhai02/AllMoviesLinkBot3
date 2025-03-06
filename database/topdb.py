from info import DATABASE_URI
import motor.motor_asyncio
import uuid  # for generating unique IDs

class JsTopDB:
    def __init__(self, db_uri):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(db_uri)
        self.db = self.client["movie_series_db"]
        self.collection = self.db["movie_series"]

    async def set_movie_series_names(self, names, group_id):
        # Split the input string by comma to get individual names
        movie_series_list = names.split(",")
        # Store each name in the database for the group with a unique search_id
        for name in movie_series_list:
            search_id = str(uuid.uuid4())  # Generate unique search_id
            await self.collection.update_one(
                {"name": name.strip(), "group_id": group_id},
                {"$inc": {"search_count": 1}},
                upsert=True
            )

    async def get_movie_series_names(self, group_id):
        # Retrieve all movie and series names for the specified group from the database
        cursor = self.collection.find({"group_id": group_id})
        # Sort by search_count field in descending order
        cursor.sort("search_count", -1)
        names = [document["name"] async for document in cursor]
        return names

    async def clear_movie_series_names(self, group_id):
        # Remove all movie and series names for the specified group from the database
        await self.collection.delete_many({"group_id": group_id})

async def main():
    movie_series_db = JsTopDB(DATABASE_URI)
    while True:
        # Simulating a movie search
        search_input = input("𝖤𝗇𝗍𝖾𝗋 𝗍𝗁𝖾 𝗆𝗈𝗏𝗂𝖾/𝗌𝖾𝗋𝗂𝖾𝗌 𝗇𝖺𝗆𝖾: ")
        group_id = input("𝖤𝗇𝗍𝖾𝗋 𝗀𝗋𝗈𝗎𝗉 𝖨𝖣: ")
        
        # Automatically set the movie/series name after search
        await movie_series_db.set_movie_series_names(search_input, group_id)
        print("𝖬𝗈𝗏𝗂𝖾/𝖲𝖾𝗋𝗂𝖾𝗌 𝗇𝖺𝗆𝖾 𝖺𝖽𝖽𝖾𝖽 𝖺𝗎𝗍𝗈𝗆𝖺𝗍𝗂𝖼𝖺𝗅𝗅𝗒.")
        
        # Print the updated list of names after each search
        names = await movie_series_db.get_movie_series_names(group_id)
        print("𝖴𝗉𝖽𝖺𝗍𝖾𝖽 𝖬𝗈𝗏𝗂𝖾/𝖲𝖾𝗋𝗂𝖾𝗌 𝖭𝖺𝗆𝖾𝗌 (𝖲𝗈𝗋𝗍𝖾𝖽 𝖻𝗒 𝖲𝖾𝖺𝗋𝖼𝗁 𝖢𝗈𝗎𝗇𝗍):")
        for name in names:
            print(name)
        
        # Option to clear names (for testing purposes)
        clear_input = input("𝖣𝗈 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍 𝗍𝗈 𝖼𝗅𝖾𝖺𝗋 𝗇𝖺𝗆𝖾𝗌 𝖿𝗈𝗋 𝗍𝗁𝗂𝗌 𝗀𝗋𝗈𝗎𝗉? (𝗒𝖾𝗌/𝗇𝗈): ")
        if clear_input.lower() == "yes":
            await movie_series_db.clear_movie_series_names(group_id)
            print("𝖭𝖺𝗆𝖾𝗌 𝖼𝗅𝖾𝖺𝗋𝖾𝖽 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒.")
