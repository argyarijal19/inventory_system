from fastapi.responses import JSONResponse
from fastapi import status


def success_get_data(data):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': status.HTTP_200_OK,
            'success': True,
            'message': "success get data",
            'data': data
        }
    )


def success_post_data(data, message):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': status.HTTP_200_OK,
            'success': True,
            'message': message,
            'data':  data
        }
    )


def get_data_null(message):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            'code': status.HTTP_404_NOT_FOUND,
            'success': False,
            'message': message,
            'data': None
        }
    )


def post_data_fail(message):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'code': status.HTTP_400_BAD_REQUEST,
            'success': False,
            'message': message,
            'data':  None
        }
    )
