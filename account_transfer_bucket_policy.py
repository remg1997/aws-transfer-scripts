import boto3


DESTINATION_BUCKET_ACCOUNT_NUMBER=0
DESTINATION_BUCKET_NAME = ''
SOURCE_REGION = ''
DESTINATION_REGION = ''
s3 = boto3.client('s3')

bucket_list =  s3.list_buckets()['Buckets']
bucket_names = [bucket['Name'] for bucket in bucket_list]
SOURCE_BUCKET_NAME = bucket_names[0] #Define bucket

bucket_policy =  {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "DelegateS3Access",
            "Effect": "Allow",
            "Principal": {
                "AWS": f"arn:aws:iam::f{DESTINATION_BUCKET_ACCOUNT_NUMBER}:root"
            },
            "Action": [
                "s3:ListBucket",
                "s3:GetObject"
            ],
            "Resource": [
                f"arn:aws:s3:::{SOURCE_BUCKET_NAME}/*",
                f"arn:aws:s3:::{SOURCE_BUCKET_NAME}"
            ]
        }
    ]
}


s3.put_bucket_policy(Bucket= SOURCE_BUCKET_NAME, Policy=bucket_policy) 


IAM_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::SOURCE_BUCKET_NAME",
                "arn:aws:s3:::SOURCE_BUCKET_NAME/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:PutObject",
                "s3:PutObjectAcl"
            ],
            "Resource": [
                "arn:aws:s3:::DESTINATION_BUCKET_NAME",
                "arn:aws:s3:::DESTINATION_BUCKET_NAME/*"
            ]
        }
    ]
}
#Once the bucket policy is set, the final step requires running the following command in the AWS CLI:

'aws s3 sync s3://SOURCE-BUCKET-NAME s3://DESTINATION-BUCKET-NAME --source-region SOURCE-REGION-NAME --region DESTINATION-REGION-NAME'
