---
title:  "AWS rekognition hello world"
date:   "2019-01-30T15:03:00.000Z"
description: This is a custom description for SEO and Open Graph purposes, rather than the default generated excerpt. Simply add a description field to the frontmatter.
---

This is a super simple snippet for checking if it's the same person in two
different photos using [AWS Rekognition](https://aws.amazon.com/rekognition/).
It could for example be used to link an image extracted from CCTV footage with
an ID photo or similar.

```python
import boto3

if __name__ == "__main__":

    fileName01='photo01.jpg'
    fileName02='photo02.jpg'
    bucket='my-rekognition-images'

    client=boto3.client('rekognition', region_name='us-east-1')
    response = client.compare_faces(
        SourceImage={
            'S3Object': {
                'Bucket': bucket,
                'Name': fileName01
            }
        },
        TargetImage={
            'S3Object': {
                'Bucket': bucket,
                'Name': fileName02
            }
        },
    )
```
