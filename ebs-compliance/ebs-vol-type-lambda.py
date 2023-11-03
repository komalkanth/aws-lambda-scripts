import boto3

def volumeid_from_arn(vol_arn):
    # split arn to get the end part related to volume-id
    arn_split = (vol_arn.split(':')[-1])

    # split last part 'volume/vol-xxxxxxxxxxxxx' to get just the volume-id
    volumeid_arn = arn_split.split('/')[-1]
    return volumeid_arn


def get_volume_type (volume_id):
    myec2_client = boto3.client('ec2')

    descr_vol_response = myec2_client.describe_volumes(
        VolumeIds=[
            volume_id
        ]
    )
    vol_type = descr_vol_response['Volumes'][0]['VolumeType']
    return(vol_type)


def lambda_handler(event, context):
    parsed_volumeid = volumeid_from_arn(event['resources'][0])
    print(f"Volume id is {parsed_volumeid}")

    volume_type = get_volume_type(parsed_volumeid)
    print(f"Volume type is {volume_type}")
    if volume_type == "gp2":
        myec2_client = boto3.client('ec2')
        modifyrequest = myec2_client.modify_volume(
            VolumeId = parsed_volumeid,
            VolumeType = 'gp3'
        )
        modified_vol_type = get_volume_type(parsed_volumeid)
        print(f"Volume {modified_vol_type} has been modified to type 'gp3'")
    elif volume_type == "gp3":
        print(f"Volume {volume_type} is already of type 'gp3'")
    else:
        print(f"Volume is not 'gp2' or 'gp3', it is of {volume_type} type")
