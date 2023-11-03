import boto3
import pprint
import sys

print('''
- - - - - - - - - - - - - - - - - -
      CHECKING VOLUME TYPE
- - - - - - - - - - - - - - - - - -
      ''')

# vol_type = ""
try:
    myec2_client = boto3.client('ec2')
    descr_vol_response = myec2_client.describe_volumes(
        VolumeIds=[
            sys.argv[1]
        ]
    )
    vol_type = descr_vol_response['Volumes'][0]['VolumeType']
except Exception as errmsg:
    print(errmsg)
else:
    if vol_type == "gp2":
        modifyrequest = myec2_client.modify_volume(
            VolumeId = sys.argv[1],
            VolumeType = 'gp3'
        )
        print(f"Volume {sys.argv[1]} has been modified to type 'gp3'")
    elif vol_type == "gp3":
        print(f"Volume {sys.argv[1]} is already of type 'gp3'")
    else:
        print(f"Volume is not 'gp2' or 'gp3', it is of {vol_type} type")




