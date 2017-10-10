# coding: utf-8
import logging
logger = logging.getLogger(__name__)

def generate_rights(user_properties):
    """Generate rights for users coming from an external SSO system onto our own user format
    with rules. Rules are actually the code of this function.

    Args:
        user_properties(dict): A dict that contains user information from auth provider.
        Of the form::

            {
                'attributes': {
                    'name': 'John Smith',
                    'email': 'john@smith.example',
                    ...
                },
                'roles': [  # Set as USER by default
                    'USER' or 'ADMIN' or 'SUPER_ADMIN'
                ],
                'provider': '<ID (name) of the provider>'
            }

    Returns:
        A dict of the same form as the input dict, with added or
        substracted (mostly roles and privileges) informations.
    """
    try:
        rayons = user_properties['attributes']['rayons'][0]
        rayons = rayons.split(',')
        user_properties['groups'] = rayons
        logger.info('User groups {}, from {}'.format(rayons, user_properties['attributes']))
    except:
        pass

    return user_properties
