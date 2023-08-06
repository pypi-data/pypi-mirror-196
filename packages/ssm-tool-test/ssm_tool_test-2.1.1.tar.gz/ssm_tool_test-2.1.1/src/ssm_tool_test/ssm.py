# Definitions of methods to get parameter store from aws
# Note: using aws credentials
import boto3


SSM_CLIENT = boto3.client('ssm')

class ParameterStore():
    """
    Structure class of SSM parameter store

    Method availables: get_parameter, describe_parameter
    """

    @staticmethod
    def get_parameter(name: str):
        try:
            ssm_parameter = SSM_CLIENT.get_parameter(
                Name=str(name),
                WithDecryption=True|False
            )
            return ssm_parameter['Parameter']
        except SSM_CLIENT.exceptions.ParameterNotFound as message:
            print(f"Error: {message}")
