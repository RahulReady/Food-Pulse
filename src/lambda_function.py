from review_scraper import GoogleReviewScraper
import time
import boto3
import json
client = boto3.client('lambda') 
def lambda_handler(event, context):
  url = event["params"]["querystring"]["url"]
  #url = 'https://www.google.com/search?sxsrf=ALeKk00eGwQ9r0qW4pRfPShRnayVy_9Qwg:1608741576150&ei=q3LjX9z2NdC0tQbrnaGQDA&q=restaurants%20springfield&tbs=lrf:!1m4!1u5!3m2!5m1!1sgcid_3american_1restaurant!1m4!1u3!2m2!3m1!1e1!1m4!1u5!2m2!5m1!1sgcid_3italian_1restaurant!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!1m4!1u22!2m2!21m1!1e1!2m1!1e2!2m1!1e1!2m1!1e3!2m1!1e5!3sIAEqAlVT,lf:1,lf_ui:9&tbm=lcl&rflfq=1&num=10&rldimm=10387104384240500369&lqi=ChdyZXN0YXVyYW50cyBzcHJpbmdmaWVsZEi9nuel8qyAgAhaOgoXcmVzdGF1cmFudHMgc3ByaW5nZmllbGQQABABGAAYASIXcmVzdGF1cmFudHMgc3ByaW5nZmllbGSaASNDaFpEU1VoTk1HOW5TMFZKUTBGblNVUnpjM1pEUTFwM0VBRQ&phdesc=zna5f1-QV7I&ved=2ahUKEwjj1LmxxeTtAhXdAp0JHdrKCpYQvS4wAnoECAIQWg&rlst=f&rlfi=hd:;si:#lrd=0x887547d645565aa7:0x7c97b16249ca0690,1,,,&rlfi=hd:;si:8977839417889261200,l,ChdyZXN0YXVyYW50cyBzcHJpbmdmaWVsZFo4ChRhbWVyaWNhbiByZXN0YXVyYW50cyIgYW1lcmljYW4gcmVzdGF1cmFudHMgc3ByaW5nZmllbGQ;mv:[[39.821890599999996,-89.5977458],[39.7091394,-89.73139990000001]]'
  local = False
  reviews = GoogleReviewScraper(local).get_reviews(url)
  # return reviews
  response = client.invoke(FunctionName='ARN_for_sentiment', InvocationType='RequestResponse', Payload=reviews)
  responseJson = json.load(response['Payload'])
  return responseJson