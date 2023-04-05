from rest_framework.response import Response

class ResponseWrapper(Response):

    def __init__(self, data=None, error_code=None, template_name=None, headers=None, exception=False, content_type=None,
                 error_msg=None, msg=None, response_success=True, status=None, data_type=None):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.

        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        status_by_default_for_gz = 200
        if error_code is None and status is not None:
            if status > 299 or status < 200:
                error_code = status
                response_success = False
            else:
                status_by_default_for_gz = status
        if error_code is not None:
            status_by_default_for_gz = error_code
            response_success = False

        # manipulate dynamic msg
        if msg is not None and not msg == "":
            if msg.lower() == "list":
                msg = "List retrieved successfully!" if response_success else "Failed to retrieve the list!"
            elif msg.lower() == "create":
                msg = "Created successfully!" if response_success else "Failed to create!"
            elif msg.lower() == "update":
                msg = "Updated successfully!" if response_success else "Failed to update!"
            elif msg.lower() == "delete":
                msg = "Deleted successfully!" if response_success else "Failed to delete!"
            elif msg.lower() == "retrieve":
                msg = "Object retrieved successfully!" if response_success else "Failed to retrieve the object!"
            else:
                pass

        output_data = {
            "error": {"code": error_code, "error_details": error_msg},
            "data": data,
            "status": response_success,
            "status_code": error_code if not error_code == "" and not error_code == None else status_by_default_for_gz,
            "message": msg if msg else str(error_msg) if error_msg else "Success" if response_success else "Failed",
        }
        if data_type is not None:
            output_data["type"] = data_type

        super().__init__(data=output_data, status=status_by_default_for_gz,
                         template_name=template_name, headers=headers,
                         exception=exception, content_type=content_type)