import boto3
import docker
import base64

def extract_ecr_configuration(ecr_client) -> dict:
    ecr_credentials = (ecr_client.get_authorization_token()['authorizationData'][0])
    ecr_username = 'AWS'
    ecr_password = (base64.b64decode(
                    ecr_credentials['authorizationToken']).replace(
                    b'AWS:', b'').decode('utf-8'))
    ecr_url = ecr_credentials['proxyEndpoint']

    return {'ecr_username':ecr_username,
            'ecr_password': ecr_password,
            'ecr_url': ecr_url}


def ecr_transfer(source_profile: str,
                 destination_profile: str,
                 destination_account_id: str,
                 region: str = 'eu-west-3'):

    """Transfer ecr repo from one AWS account to another

    Args:
        source_profile (str): AWS config profile for source account
        destination_profile (str): AWS config profile for destination account
        destination_account_id (str): AWS destination account ID
        region (str, optional): Region where to create buckets. Defaults to 'eu-west-3'.
    """

    source_session = boto3.Session(profile_name=source_profile, region_name=region)
    destination_session = boto3.Session(profile_name=destination_profile, region_name=region)

    ecr_source_client= source_session.client('ecr')
    ecr_destination_client = destination_session.client('ecr')

    ecr_source_config = extract_ecr_configuration(ecr_source_client)
    ecr_destination_config = extract_ecr_configuration(ecr_destination_client)

    docker_client = docker.from_env()
    docker_client.login(username=ecr_source_config['ecr_username'],
                        password=ecr_source_config['ecr_password'],
                        registry=ecr_source_config['ecr_url'])

    docker_dest_client = docker.from_env()
    docker_dest_client.login(username=ecr_destination_config['ecr_username'],
                             password=ecr_destination_config['ecr_password'],
                             registry=ecr_destination_config['ecr_url'])

    repo_list = ecr_source_client.describe_repositories()

    for i in repo_list['repositories']:
        print("Creating new destination repository")
        response = ecr_destination_client.create_repository(registryId = str(destination_account_id),
                                                            repositoryName =i['repositoryName'])

        print(response)
        print(f"Pulling image {i['repositoryName']} from meta account")

        image = docker_client.images.pull(repository=i['repositoryUri'])
        print("Image pulled")

        image.tag(repository=response['repository']['repositoryUri'], tag = 'latest')
        print("Image tagged")

        push_image = docker_dest_client.images.push(repository = response['repository']['repositoryUri'],
                                                    tag = 'latest')
        print("Image pushed to destination repository")

if __name__ == '__main__':
    import fire
    fire.Fire(ecr_transfer)



