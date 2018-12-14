#Getting a list of account followers!
from InstagramAPI import InstagramAPI
import random
import time
import sys

def getTotalFollowers(api, user_id):
    """
    Returns the list of followers of the user.
    It should be equivalent of calling api.getTotalFollowers from InstagramAPI
    """

    followers = []
    next_max_id = True
    while next_max_id:
        # first iteration hack
        if next_max_id is True:
            next_max_id = ''

        _ = api.getUserFollowers(user_id, maxid=next_max_id)
        followers.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')
    return followers


if __name__ == "__main__":
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

    #Logining in
    api = InstagramAPI("", "")
    api.login()

    usedList = [5783083247, 200770901, 6223763144, 708885350, 1190318950, 4262637901, 1816863358, 6067232924, 40393730, 7071712831, 1751097425, 7203236488, 4926947083, 4640697970, 7301520547, 14819244, 551414615]
    userList = [7203236488]
    userList = [839915492]
    for user in userList:
        try:
            #Printing out the current user id
            print("User ID: " + str(user))
            
            #Getting the list of followers for the specified ID
            followers = api.getTotalFollowers(int(user))
            print("Number of followers: " + str(len(followers)) + "\n")

            #Traversing and following each of the users in the followers list
            count = 0
            for follower in followers:
                #Printing out the current person's information
                print(str(follower['full_name']).translate(non_bmp_map) + "\n\t" + (str(follower['pk'])) + "\n\t" + str(count))
                
                #Following the current person by their UserID
                api.follow(follower['pk'])

                #Incrementing the current count
                count += 1

                #Generating a time to sleep for between 8 - 12 seconds
                randomTime = random.randint(1500, 2000) / 100

                #Sleeping for that time
                time.sleep(randomTime)

                #Every 10 follows, we will wait 20 seconds to not seem too suspicious
                if(count % 10 == 0):
                    print("Taking a break...")
                    time.sleep(20)
                if(count >= 300):
                    break
            print("\nDone with User ID: " + str(userID) + "\n")
        except Exception as e:
            print("User ID: " + str(user) + " caused an error")
            print(str(e))
            time.sleep(60*15)
    print("Completely Done!")
