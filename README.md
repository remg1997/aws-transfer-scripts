# aws-transfer-scripts
Repository meant for storing scripts used to transfer objects between different AWS accounts and services


1. S3 file transfer between accounts:
    1. Setup the source account. This means:
        1. Sign into the source account in AWS. 
        2. Attach the policy included in [account_transfer_bucket_policy.py](https://github.com/remg1997/aws-transfer-scripts/blob/main/account_transfer_bucket_policy.py) to the bucket you want to synchronize in the destination account. As you can see, that script automatically attaches the policy for any bucket you specify. 

    2. Setup the destination account. This means:
        1. Sign into the destination account in AWS.
        2. Create an IAM user that includes the policy included in the same script as 1.1. 
        3. Open AWS CLI and run the following command replacing the related variables: 
        `aws s3 sync s3://SOURCE-BUCKET-NAME s3://DESTINATION-BUCKET-NAME --source-region SOURCE-REGION-NAME --region DESTINATION-REGION-NAME`


2. ECR image transfer between accounts:
    1. Open a terminal and go to .aws directory. (`cd ~/.aws` should do the trick in macOS ).
    2. Run your preferred text editor to open the credentials file. We will be creating two AWS profiles, one for the source account and one for the destination account. Specific instructions can be found [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html#:~:text=Using%20named%20profiles-,Creating%20named%20profiles,-You%20can%20configure). For example, create a profile named Source and a profile named Destination. 
    3. Head to the directory where the [ecr_transfer.py](https://github.com/remg1997/aws-transfer-scripts/blob/main/ecr_transfer.py) script is stored.
    4. Run the following command: `python ecr_transfer.py --source_profile >Source< --destination_profile >Destination< --destination_account_id >Destination_Account_ID<` replacing the source profile name, the destination profile name and the destination account ID. 
