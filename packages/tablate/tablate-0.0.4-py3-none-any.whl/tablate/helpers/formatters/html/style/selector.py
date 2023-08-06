def id_factory(element_id: str) -> str:
    return f'tablate-{element_id}'
def class_factory(element_type: str, element_id: str, uid: str) -> str:
    return f'tablate {element_type} {element_id} tablate-{uid}'
