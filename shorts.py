from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import pandas as pd
import re
import html


def cleanurl(raw_url):
  cleanr = re.compile('(http|ftp|https)://(?:[-\w.]|(?:\da-fA-F]{2}))+')
  cleantext = re.sub(cleanr, '', raw_url)
  return cleantext
'''
##########################################################################################################################
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def rmEmoji(inputData):
    return inputData.encode('utf-8', 'ignore').decode('utf-8')

def rmEmoji_ascii(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

##########################################################################################################################
#유튜브를 불러오는 빌더를 불러온다.
DEVELOPER_KEY = "AIzaSyBRGZRZJbbBnCNdmEFFFyZmu3yGDQ8KrSw"
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
##########################################################################################################################
#채널의 업로드된 동영상 리스트 아이디를 가져온다.
youtube = build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
response = youtube.search().list(q="#Shorts", order = 'viewCount',part = "snippet,id",type = 'video',maxResults=100).execute()


#동영상을 가져오고 데이터 프레임으로 정리하고 엑셀로 저장
videos = list()
while response:
        for item in response['items']:
            video = item['snippet']
            videos.append([video['title'], video['publishedAt'], item['id']['videoId']])
 
        if 'nextPageToken' in response:
            response = youtube.search().list(part='snippet,id',q="#Shorts", order = 'viewCount',type = 'video', pageToken=response['nextPageToken'], maxResults=100).execute()
        else:
            break
    
listvd_df = pd.DataFrame(videos)
listvd_df.columns = ['title', 'publishedAt', 'ID']
#listvd_df.to_excel('listvd.xlsx', index=False)
#listvd_df = pd.read_excel('listvd.xlsx')
#########################################################################################################################
#코멘트수를 추가
comments = list()
cnt = 0
for ids in listvd_df['ID'][:20]:
    print(cnt)
    cnt = cnt + 1
    response = youtube.commentThreads().list(part='snippet,replies', videoId=ids, maxResults=100).execute()
    
    while response:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append([comment['textDisplay'], comment['authorDisplayName'], comment['publishedAt'], comment['likeCount']])
 
            if item['snippet']['totalReplyCount'] > 0:
                for reply_item in item['replies']['comments']:
                    reply = reply_item['snippet']
                    comments.append([reply['textDisplay'], reply['authorDisplayName'], reply['publishedAt'], reply['likeCount']])
 
        if 'nextPageToken' in response:
            response = youtube.commentThreads().list(part='snippet,replies', videoId=ids, pageToken=response['nextPageToken'], maxResults=100).execute()
        else:
            break

comment_df = pd.DataFrame(comments)
comment_df.columns = ['comment', 'author', 'date', 'num_likes']

##############################################################################################################################

comment_list = list()
for comment in comment_df['comment']:
    de_comments = html.unescape(str(comment))
    de_comments = rmEmoji(de_comments)
    de_comments = rmEmoji_ascii(de_comments)
    de_comments = cleanhtml(de_comments)
    comment_list.append(de_comments)

comment_1 = pd.DataFrame(comment_list)
comment_1.columns = ['comment']

rm = comment_df.drop("comment",axis=1)
dataset = pd.concat([comment_1,rm],axis=1)

##############################################################################################################################

index_list =list()
for i in range(50):
    if i == 0:
        space = ' '
    else:
        space = space + ' '
    cnt = 0
    for com in comment_df['comment']:
        if re.fullmatch(space,com):
            index_list.append(cnt)
        cnt += 1
no_space = comment_df.drop(index_list)

###############################################################################################################################

id_list = dataset.drop_duplicates(["author"])
docu = list()
log = list()
cnt = 0
for com in dataset['comment']:
    if re.search('@',com):
        log.append(cnt)
    cnt += 1
    
re_com = dataset.iloc[log]
re_com.reset_index(drop=True, inplace=True)
re_com2= re_com.copy()

for ids in id_list["author"]:
    nick = '@'+str(ids)
    cnt = 0
    for com in re_com['comment']:
        if nick in com:
            nake = com.replace(nick,'')
            re_com2['comment'][cnt] = nake
        cnt += 1
        
temp_df = dataset.drop(log)
dataset2 = pd.concat([temp_df,re_com2],ignore_index=True)
###############################################################################################################################
'''
dataset2 = pd.read_csv('before.csv')
comment_list2 = list()
for comment in dataset2['comment']:
    de_comments = cleanurl(str(comment))
    comment_list2.append(de_comments)

comment_2 = pd.DataFrame(comment_list2)
comment_2.columns = ['comment']
rm = dataset2.drop("comment",axis=1)
dataset3 = pd.concat([comment_2,rm],axis=1)
