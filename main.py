from reditt_api_functions.api_call.downlaod_api_data import RedittApi
from reditt_api_functions.file_systems.convert_file import ConvertFile



if __name__ == "__main__":
    ConvertFile().delete_tmp_dir()
    ConvertFile().create_tmp_dir()
    RedittApi().get_api_data()

    ConvertFile().add_audit_fields_upload_to_s3()





