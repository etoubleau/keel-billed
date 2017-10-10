def generate_permissions(data):
    """
    Insert here code to generate group specific permissions
    """

    user_groups_permissions = []
    for entity in data:
        user_groups_permissions.append({
            'group': entity[u'ENTITY_ID'],
            'reports': {
                '$or': [
                    {'ENTITY_ID': entity[u'ENTITY_ID']}
                ,
                    {'ENTITY_ID': entity[u'ID_DEPARTEMENT']}
                ,
                    {'ENTITY_ID': entity[u'ID_UNIVERS']}
                ]
                }
        })

    # print user_groups_permissions

    return user_groups_permissions
