from InstagramAPI import InstagramAPI
import base64
import sys


'''
def shortcode_to_id(shortcode):
    code = ('A' * (12-len(shortcode)))+shortcode
    return int.from_bytes(base64.b64decode(code.encode(), b'-_'), 'big')
'''


if(__name__ == "__main__"):
    IGApi = InstagramAPI("username", "password")
    IGApi.login()
    try:

        target = "6223763144"

        IGApi.getUserFeed(target)
        
        media = IGApi.LastJson['items']


        for post in media:
            post_id = str(post['id']).split("_")[0]
            print(post_id)
            IGApi.getMediaLikers(post_id)
            info = IGApi.LastJson
            likers = info['users']
            print(str(len(likers)))
            for liker in likers:
                likerUsername = str(liker['username'])
                likerUserID = str(liker['pk'])
                print("Username: " + likerUsername)
                print("\tUser ID: " + likerUserID)
    except Exception as e:
        print(str(e))
    IGApi.logout()
