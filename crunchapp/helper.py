import re  
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
from django.conf import settings
from django.core.mail import send_mail


#s = 'Hello from shubhamg199630@gmail.com to priya@yahoo.com about the meeting @2PM'
# \S matches any non-whitespace character 
# @ for as in the Email 
# + for Repeats a character one or more times 
# lst = re.findall('\S+@\S+', s)
# # print(lst)
#['shubhamg199630@gmail.com', 'priya@yahoo.com']





def getFilterEmailData(descript):
    if descript != "":
        emails = [i for i in re.findall('\S+@\S+', descript)]
        # emails = re.findall('\S+@\S+', s)
        if len(emails) != 0:
            return emails[0]
    # if len(emails) == 0:
    #     emails = '-'

def filterSpecialChar(text):
    if text[-1] != '.':
        return text[:-1]
    if text[-1] != ',':
        return text[:-1]


def getInstagramData(descript):
    if descript != "":
        # # print(descript)
        insta = [t for t in descript.split() if t.startswith('@') ]
        if len(insta) != 0:
            insta = insta[0].replace('@','')
            # insta = filterSpecialChar(insta)
            # print(insta)
            # insta = insta[-1].replace('.','')
            # insta = insta[-1].replace('[','')
            # insta = insta[-1].replace(']','')
            # insta = insta[-1].replace('#','')
            # insta = insta[-1].replace('@','')
            # insta = insta[-1].replace('$','')
            # insta = insta[-1].replace('&','')
            # insta = insta[-1].replace('(','')
            # insta = insta[-1].replace(')','')
            return "https://www.instagram.com/" + insta
    # instagram = ''
    # for link in BeautifulSoup(descript, parse_only=SoupStrainer('a')):
    #     if link.has_attr('href'):
    #         if link.text == "Instagram" or link.text == "Insta":
    #             instagram = link['href']
    # else:
    #     instagram = " ".join(filter(lambda x:x[0] =='@', descript.split()))
    #     instagram = instagram.replace("@","")
    # if len(instagram) == 0:
    #     instagram = ""
    # return instagram
    



def serachPlayList(request,offsetNO,searcString,sp,checked_value):
    dataCollectDict = {}
    dataCollectList = []
    try:
        for iOffset in offsetNO:
            results = sp.search(q=searcString,limit=50,type='playlist', offset=iOffset)
            if len(results['playlists']['items']) != 0:
                for dataGet in results['playlists']['items']:
                    if checked_value == "Email" and getFilterEmailData(dataGet['description']):
                        dataCollectDict['display_url'] = "https://open.spotify.com/playlist/" + dataGet['id']
                        dataCollectDict['followers'] = sp.playlist(dataGet['id'])['followers']['total']
                        dataCollectDict['desciption'] = dataGet['description']
                        dataCollectDict['author_name'] = dataGet['name']
                        dataCollectDict['tracks'] = dataGet['tracks']['total']
                        dataCollectDict['ownerName'] = dataGet['owner']['display_name']
                        dataCollectDict['email'] = getFilterEmailData(dataGet['description'])
                        dataCollectDict['instagram'] = None
                        dataCollectList.append(dataCollectDict)
                        dataCollectDict = {}
                    if checked_value == "Instagram" and getInstagramData(dataGet['description']):
                        dataCollectDict['display_url'] = "https://open.spotify.com/playlist/" + dataGet['id']
                        dataCollectDict['followers'] = sp.playlist(dataGet['id'])['followers']['total']
                        dataCollectDict['desciption'] = dataGet['description']
                        dataCollectDict['author_name'] = dataGet['name']
                        dataCollectDict['tracks'] = dataGet['tracks']['total']
                        dataCollectDict['ownerName'] = dataGet['owner']['display_name']
                        dataCollectDict['email'] = None
                        dataCollectDict['instagram'] = getInstagramData(dataGet['description'])
                        dataCollectList.append(dataCollectDict)
                        dataCollectDict = {}
                    if checked_value == "All" and (getFilterEmailData(dataGet['description']) or getInstagramData(dataGet['description'])):
                        # print("all")
                        dataCollectDict['display_url'] = "https://open.spotify.com/playlist/" + dataGet['id']
                        dataCollectDict['followers'] = sp.playlist(dataGet['id'])['followers']['total']
                        dataCollectDict['desciption'] = dataGet['description']
                        dataCollectDict['author_name'] = dataGet['name']
                        dataCollectDict['tracks'] = dataGet['tracks']['total']
                        dataCollectDict['ownerName'] = dataGet['owner']['display_name']
                        dataCollectDict['email'] = getFilterEmailData(dataGet['description'])
                        dataCollectDict['instagram'] = getInstagramData(dataGet['description'])
                        dataCollectList.append(dataCollectDict)
                        dataCollectDict = {}
        if len(dataCollectList) != 0:
            # print(dataCollectList)
            return dataCollectList
        return dataCollectList
                
    # exit()
    #     if len(results['playlists']['items']) != 0:
    #         for dataGet in results['playlists']['items']:
    #             if checked_value == "mail" and len(getFilterEmailData(dataGet['description'])) != 0:
    #                 dataCollect = frameData(sp,dataCollectDict,dataGet,checked_value)
    #                 dataCollectList.append(dataCollect)
    #                 dataCollectDict = {}
    #             if checked_value == "insta" and  len(getInstagramData(dataGet['description'])) != 0:
    #                 dataCollect = frameData(sp,dataCollectDict,dataGet,checked_value)
    #                 dataCollectList.append(dataCollect)
    #                 dataCollectDict = {}
    #             if checked_value == "all" and  len(getInstagramData(dataGet['description'])) != 0 or len(getFilterEmailData(dataGet['description'])) != 0:
    #                 dataCollect = frameData(sp,dataCollectDict,dataGet,checked_value)
    #                 dataCollectList.append(dataCollect)
    #                 dataCollectDict = {}

    except:
        return dataCollectList




def sendEmail(sendEmailID,baseURL,token,typeCHeck):
    subject = 'Playlist Crunch| Reset Password'
    if typeCHeck == "FORGOTPASSWORD":
        url_link =  baseURL + "verify_user_to_reset_password/token=" + token + "/email=" + sendEmailID 
        message = f'Hi Playlist Crunch User, your reset password, link is {url_link}'
    if typeCHeck == "VERIFYEMAIL":
        url_link =  baseURL + "verify_account/token=" + token + "/email=" + sendEmailID
        message = f'Hi Playlist Crunch User, please verify your email {url_link}'
    # message = f'Hi {user.username}, thank you for registering in geeksforgeeks.'
    email_from = settings.EMAIL_HOST_USER
    # email_from = "info@playlistcrunch.com"
    recipient_list = [sendEmailID,]
    send_mail( subject, message, email_from, recipient_list )






    
    
   