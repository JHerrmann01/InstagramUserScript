from InstagramAPI import InstagramAPI
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random

class InstagramBot():
    def __init__(self, email, password):
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_argument("--incognito")
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.browser = webdriver.Chrome('/home/jeremy/Desktop/chromedriver', chrome_options=self.browserProfile)
        self.email = email
        self.password = password

    def signIn(self):
        self.browser.get('https://www.instagram.com/accounts/login/')
        time.sleep(10)
        emailInput = self.browser.find_elements_by_css_selector('form input')[0]
        passwordInput = self.browser.find_elements_by_css_selector('form input')[1]
        
        emailInput.send_keys(self.email)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(10)
        self.browser.find_elements_by_xpath("//*[contains(text(), 'Not Now')]")[0].click()
        time.sleep(10)
        
    def followWithUsername(self, username):
        self.browser.get('https://www.instagram.com/' + username + '/')
        time.sleep(2)
        followButton = self.browser.find_element_by_css_selector('button')
        if (followButton.text != 'Following'):
            followButton.click()
            time.sleep(2)
        else:
            print("You are already following this user")
    
    def unfollowWithUsername(self, username):
        self.browser.get('https://www.instagram.com/' + username + '/')
        time.sleep(2)
        followButton = self.browser.find_element_by_css_selector('button')
        if (followButton.text == 'Following'):
            followButton.click()
            time.sleep(2)
            confirmButton = self.browser.find_element_by_xpath('//button[text() = "Unfollow"]')
            confirmButton.click()
        else:
            print("You are not following this user")
    
    def getUserFollowers(self, username, max):
        self.browser.get('https://www.instagram.com/' + username)
        followersLink = self.browser.find_element_by_css_selector('ul li a')
        followersLink.click()
        time.sleep(2)
        followersList = self.browser.find_element_by_css_selector('div[role=\'dialog\'] ul')
        numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
    
        followersList.click()
        actionChain = webdriver.ActionChains(self.browser)
        while (numberOfFollowersInList < max):
            actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
            print(numberOfFollowersInList)
        
        followers = []
        for user in followersList.find_elements_by_css_selector('li'):
            userLink = user.find_element_by_css_selector('a').get_attribute('href')
            print(userLink)
            followers.append(userLink)
            if (len(followers) == max):
                break
        return followers

    def followAction(self, user_id, quantity):
        print("Getting followers")
        followers = getFollowers(user_id)

        #Traversing and following each of the users in the followers list
        count = 0
        for follower in followers:
            #Printing out the current person's information
            print(str(follower['username']) + "\n\t" + (str(follower['pk'])) + "\n\t" + str(count))
            
            #Following the current person by their UserID
            #api.follow(follower['pk'])
            self.followWithUsername(follower['username'])

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
            if(count >= quantity):
                break
            
    def unfollowAction(self, quantity):
        print("Getting people following me")
        followers = getFollowing()

        #Traversing and following each of the users in the followers list
        count = 0
        for follower in followers:
            #Printing out the current person's information
            print(str(follower['username']) + "\n\t" + (str(follower['pk'])) + "\n\t" + str(count))
            
            #Following the current person by their UserID
            #api.follow(follower['pk'])
            self.unfollowWithUsername(follower['username'])

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
            if(count >= quantity):
                break

    def closeBrowser(self):
        self.browser.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.closeBrowser()


def getFollowers(user_id):
    api = InstagramAPI("satisfyingsunsets", "laralamp")
    api.login()
    followers = api.getTotalFollowers(user_id)
    print("Number of followers: " + str(len(followers)))
    api.logout()
    return followers

def getFollowing():
    api = InstagramAPI("satisfyingsunsets", "laralamp")
    api.login()
    followers = api.getTotalFollowings(api.username_id)
    print("Number of followers: " + str(len(followers)))
    api.logout()
    return followers

if __name__ == "__main__":
    bot = InstagramBot("satisfyingsunsets@gmail.com", "Laralamp")
    bot.signIn()

    #bot.followAction("4262637901", 10)
    bot.unfollowAction(10)
    bot.closeBrowser()
    
    





        
