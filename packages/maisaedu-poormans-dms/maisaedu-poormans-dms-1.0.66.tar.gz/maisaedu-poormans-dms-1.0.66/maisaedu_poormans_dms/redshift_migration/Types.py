LOCAL = "local"
DEV = "dev"
PROD = "prod"

FULL = "full"
INCREMENTAL = "incremental"

PREFECT_DMS = "prefect-dms"
PREFECT = "prefect"

SAVED_S3 = "saved-s3"
SAVED_REDSHIFT = "saved-redshift"

IAM_ROLE = "arn:aws:iam::977647303146:role/service-role/AmazonRedshift-CommandsAccessRole-20220714T104138"


def check_if_env_is_valid(env):
    if env not in [LOCAL, DEV, PROD]:
        raise ValueError("env must be 'local', 'dev' or 'prod'")


def check_if_option_is_valid(option):
    if option not in [FULL, INCREMENTAL, None]:
        raise ValueError("option must be 'full' or 'incremental'")
