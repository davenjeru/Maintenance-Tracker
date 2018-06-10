import datetime

from flask import url_for, request
from flask_restplus import Resource
from werkzeug.exceptions import BadRequest

from MaintenanceTrackerAPI.api.v1.exceptions import PayloadExtractionError, \
    RequestTransactionError
from MaintenanceTrackerAPI.api.v1.models.request_model import Request


def get_validated_payload(resource: Resource):
    """
    Checks whether the request data is in JSON raising an error if not
    Evaluates the request data to a dict literal if it is a string or bytes
    object
    :param resource:
    :return: validated payload
    :rtype: dict
    """
    # check whether the request body is in JSON format
    if request.content_type != 'application/json':
        raise PayloadExtractionError('request data should be in json format',
                                     415)
    try:
        # in the tests, request body is sent as string so we have to eval the
        #  body to dict
        payload = eval(resource.api.payload) if type(resource.api.payload) == \
                                                str else resource.api.payload
    except BadRequest:
        # if an error is caught as a bad request, try and get the data from
        # request.data if its there
        try:
            payload = eval(request.data) if bool(request.data) else None
        except Exception as e:
            raise PayloadExtractionError('Something is wrong'
                                         ' with data you have provided')
    except Exception as e:
        raise PayloadExtractionError('Something is wrong'
                                     ' with the data you have provided')

    # All the above checks have not given a payload so the only explanation
    # is that there is none hence return a 400
    if payload is None:
        raise PayloadExtractionError('no data was found in the request', 400)
    return payload


def extract_from_payload(payload: dict, list_of_contexts: list):
    """
    Extracts items from the given dictionary raising an error
    if the item could not be found
    :param payload:
    :param list_of_contexts:
    :return: tuple of the items that were extracted
    :rtype: dict
    """
    return_list = []
    for name in list_of_contexts:
        if payload.get(name) is None \
                and (name != 'role' and name != 'request_type'):
            raise PayloadExtractionError(
                'missing \'{}\' parameter'.format(name), 400)
        return_list.append(payload.get(name, None))

    return tuple(return_list)


def generate_auth_output(resource, user: dict):
    """
    Generates output specific to the auth namespace
    :param resource: The resource that called this function
    :param user: The user whose output should be generated
    :return: The output dictionary specific to the resource
    that called this function
    :rtype: dict
    """
    api = resource.api
    output_dict = dict(user=safe_user_output(resource, user))

    if api.url_for(resource) == url_for(api.endpoint('auth_register')):
        output_dict['message'] = 'user registered successfully'
    elif api.url_for(resource) == url_for(api.endpoint('auth_login')):
        output_dict['message'] = 'user logged in successfully'
    elif api.url_for(resource) == url_for(api.endpoint('auth_logout')):
        output_dict['message'] = 'user logged out successfully'

    return output_dict


def safe_user_output(resource: Resource, user: dict):
    """
    Creates a dictionary of a User's details
    :param resource:
    :param user:
    :return: dict
    """
    api = resource.api
    output = dict(email=user['email'], role=user['role'])
    return output


def safe_request_output(resource: Resource, the_request: dict):
    """
    Creates a dictionary of Request details
    :param resource:
    :param the_request:
    :return: dict
    """
    api = resource.api
    request_dict = dict(
        requested_by=the_request['requested_by'],
        request_type=the_request['request_type'],
        title=the_request['title'],
        description=the_request['description'],
        date_requested=str(the_request['date_requested']),
        status=the_request['status'],
        last_modified=str(the_request['last_modified'])
    )
    return request_dict


def generate_request_output(resource: Resource, the_request: dict,
                            method: str):
    """
    Generates output specific to the users namespace
    :param resource: The resource that called this function
    :param the_request: The request whose output should be generated
    :param method: The HTTP method
    :return: The output dictionary specific to the resource that called
     this function
    :rtype: dict
    """
    output_dict = dict(request=safe_request_output(resource, the_request))
    if 'single_user_all_requests' in resource.endpoint:
        if method == 'post':
            output_dict['message'] = 'request created successfully'
    elif 'users_single_user_single_request' in resource.endpoint:
        if method == 'patch':
            output_dict['message'] = 'request modified successfully'
    return output_dict


def edit_request(a_request: dict, details: dict):
    """
    Method to edit a request
    :param a_request: The request to be edited
    :param details: A dictionary containing the details to be changed
    :return: edited request
    """
    # make a copy of the dictionary
    the_request = a_request.copy()

    # check the request status
    if the_request['status'] != 'Pending Approval':
        raise RequestTransactionError('cannot edit a request which'
                                      ' is {}'.format(the_request['status']),
                                      409)

    # retrieve the title and description from the details dictionary
    title = details.get('title', None)
    description = details.get('description', None)

    # validate the details given
    try:
        if title is not None:
            Request._Request__validate_request_details('title', title)
        if description is not None:
            Request._Request__validate_request_details('description',
                                                       description)
    except AssertionError as e:
        raise RequestTransactionError(e.args[0])

    # raise error if no title and description was given
    if not title and not description:
        raise RequestTransactionError('could not edit request, please '
                                      'insert title or description')

    # check if the title or description given is the same
    if title is not None:
        if the_request['title'] == title:
            name = 'title'
            raise RequestTransactionError('{0} given matches'
                                          ' the previous {0}'.format(name))
    if description is not None:
        if the_request['description'] == description:
            name = 'description'
            raise RequestTransactionError('{0} given matches the'
                                          ' previous {0}'.format(name))

    # change the details if they are not None
    the_request['title'] = title if title is not None else the_request['title']
    the_request['description'] = description if description is not None \
        else the_request['description']

    # change the 'last_modified' timestamp and return
    the_request['last_modified'] = datetime.datetime.now()
    return the_request
