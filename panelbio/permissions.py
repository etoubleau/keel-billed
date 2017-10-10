def generate_permissions(data):
    """
    Insert here code to generate group specific permissions
    """

    user_groups_permissions = []
    for entity in data:
        user_groups_permissions.append({
            'group': entity[u'nom_entite'],
            'reports': {
                'ENTITY_ID': entity[u'ENTITY_ID'],
                }
        })

    # print user_groups_permissions

    return user_groups_permissions
