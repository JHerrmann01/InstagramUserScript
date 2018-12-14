#Unfollowing all the people the account is currently following
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

    
    try:
        #Getting the list of followers for the specified ID
        following = api.getTotalFollowings(api.username_id)
        print("Number of following: " + str(len(following)) + "\n")
        
        #Traversing and following each of the users in the followers list
        count = 0
        for user in following:
            #Printing out the current person's information
            print(str(user['full_name']).translate(non_bmp_map) + "\n\t" + (str(user['pk'])))
            
            #Following the current person by their UserID
            api.unfollow(user['pk'])

            #Incrementing the current count
            count += 1

            #Generating a time to sleep for between 8 - 12 seconds
            randomTime = random.randint(800, 1200) / 100

            #Sleeping for that time
            time.sleep(randomTime)

            #Every 10 follows, we will wait 20 seconds to not seem too suspicious
            if(count % 10 == 0):
                print("Taking a break...")
                time.sleep(20)
    except Exception as e:
        print(str(e))
        time.sleep(60*15)
    print("Completely Done!")
