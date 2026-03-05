# name: Brandon Valadez
# date: March 5
# description: Implementation of CRUD operations with DynamoDB — CS178 Lab 10
# proposed score: 0 (out of 5) -- 4.999999... I believe my interface hits all of the critical points and it clever enough to use for songs :D

import boto3
from boto3.dynamodb.conditions import Attr

# boto3 uses the credentials configured via `aws configure` on EC2
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def get_table():
    """Return a reference to the DynamoDB Songs table."""
    return dynamodb.Table('Songs')

def create_song():
    try:
        title = input("Enter song title: ").strip()
        if not title:
            print("Title cannot be empty.")
            return

        artist = input("Enter artist name: ").strip()
        if not artist:
            print("Artist cannot be empty.")
            return

        table = get_table()

        # Check if a song with this title already exists
        response = table.scan(
            FilterExpression=Attr("Title").eq(title)
        )
        if response.get("Items"):
            print(f"\nA song titled '{title}' already exists.")
            return

        item = {
            "Title":   title,
            "Artist":  artist,
            "Ratings": []
        }
        table.put_item(Item=item)
        print(f"\nSong '{title}' by {artist} successfully added!\n")
        print_song(item)

    except:
        print("error in creating song")
def print_song(song):
    title   = song.get("Title",   "Unknown Title")
    artist  = song.get("Artist",  "Unknown Artist")
    ratings = song.get("Ratings", [])
    print(f"  Title  : {title}")
    print(f"  Artist : {artist}")
    print(f"  Ratings: {ratings if ratings else 'No ratings yet'}")
    print()

def print_all_songs():
    try:
        table = get_table()
        response = table.scan()
        items = response.get("Items", [])

        if not items:
            print("No songs found. Make sure your DynamoDB table has data.")
            return

        print(f"\nFound {len(items)} song(s):\n")
        for song in items:
            print_song(song)

    except:
        print("error in reading songs")

def update_rating():
    try:
        title  = input("Enter song title to rate: ").strip()
        rating = int(input("Enter your rating (1-10): "))

        if not 1 <= rating <= 10:
            print("Rating must be between 1 and 10.")
            return

        table = get_table()


        response = table.scan(
            FilterExpression=Attr("Title").eq(title)
        )
        if not response.get("Items"):
            print(f"\nSong '{title}' not found in the table.")
            return

        table.update_item(
            Key={"Title": title},
            UpdateExpression="SET Ratings = list_append(Ratings, :r)",
            ExpressionAttributeValues={':r': [rating]}
        )
        print(f"\nRating of {rating} successfully added to '{title}'!\n")

    except:
        print("error in updating song rating")

def delete_song():
    try:
        title = input("Enter song title to delete: ").strip()
        if not title:
            print("Title cannot be empty.")
            return

        table = get_table()

        response = table.scan(
            FilterExpression=Attr("Title").eq(title)
        )
        if not response.get("Items"):
            print(f"\nSong '{title}' not found in the table.")
            return

        table.delete_item(
            Key={"Title": title}
        )
        print(f"\nSong '{title}' successfully deleted.\n")

    except:
        print("error in deleting song")

def query_song():
    try:
        title = input("Enter song title to query: ").strip()
        if not title:
            print("Title cannot be empty.")
            return

        table = get_table()

        response = table.get_item(
            Key={"Title": title}
        )
        song = response.get("Item")

        if not song:
            print("song not found")
            return

        ratings_list = song.get("Ratings", [])

        if not ratings_list:
            print("song has no ratings")
            return

        average = sum(ratings_list) / len(ratings_list)
        print(f"\n  Title  : {song.get('Title')}")
        print(f"  Artist : {song.get('Artist', 'Unknown Artist')}")
        print(f"  Ratings: {ratings_list}")
        print(f"  Average: {average:.1f}\n")

    except:
        print("error in querying song")

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new song")
    print("Press R: to READ all songs")
    print("Press U: to UPDATE a song (add a rating)")
    print("Press D: to DELETE a song")
    print("Press Q: to QUERY a song's average rating")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_song()
        elif input_char.upper() == "R":
            print_all_songs()
        elif input_char.upper() == "U":
            update_rating()
        elif input_char.upper() == "D":
            delete_song()
        elif input_char.upper() == "Q":
            query_song()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()
