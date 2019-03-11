import pprint
import json
import sys

import boto3


class VideoDetect:
    jobId = ''
    rek = boto3.client('rekognition', region_name='us-east-1')
    queueUrl = 'https://sqs.us-east-1.amazonaws.com/my-sqs-url'
    roleArn = 'arn:aws:iam::my-role-arn'
    topicArn = 'arn:aws:sns:us-east-1:my-topic-arn'
    bucket = 'my-bucket'
    video = '1096256848221663232.mp4'

    def main(self):

        jobFound = False
        sqs = boto3.client('sqs')

        response = self.rek.start_label_detection(Video={'S3Object': {'Bucket': self.bucket, 'Name': self.video}},
                                         NotificationChannel={'RoleArn': self.roleArn, 'SNSTopicArn': self.topicArn})
        while jobFound == False:
            sqsResponse = sqs.receive_message(QueueUrl=self.queueUrl, MessageAttributeNames=['ALL'],
                                          MaxNumberOfMessages=10)

            if sqsResponse:
                
                if 'Messages' not in sqsResponse:
                    continue

                for message in sqsResponse['Messages']:
                    notification = json.loads(message['Body'])
                    rekMessage = json.loads(notification['Message'])
                    if str(rekMessage['JobId']) == response['JobId']:
                        jobFound = True
                        #=============================================
                        self.GetResultsLabels(rekMessage['JobId'])
                        #=============================================

                        sqs.delete_message(QueueUrl=self.queueUrl,
                                       ReceiptHandle=message['ReceiptHandle'])
                    # Delete the unknown message. Consider sending to dead letter queue
                    sqs.delete_message(QueueUrl=self.queueUrl,
                                   ReceiptHandle=message['ReceiptHandle'])



    def GetResultsLabels(self, jobId):
        maxResults = 10
        paginationToken = ''
        finished = False
        pp = pprint.PrettyPrinter(indent=4)

        while finished == False:
            response = self.rek.get_label_detection(JobId=jobId,
                                            MaxResults=maxResults,
                                            NextToken=paginationToken,
                                            SortBy='TIMESTAMP')

            for labelDetection in response['Labels']:
                label=labelDetection['Label']

                if label['Name'] == 'Water' or label['Name'] == 'Sea' or label['Name'] == 'Ocean':
                    pp.pprint(labelDetection)

                if 'NextToken' in response:
                    paginationToken = response['NextToken']
                else:
                    finished = True


if __name__ == "__main__":

    analyzer=VideoDetect()
    analyzer.main()
