def encode_str(data: str) -> str:
    return data.encode('utf-8').decode('iso-8859-1')


def decode_str(data: str) -> str:
    try:
        return data.encode('iso-8859-1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError, AttributeError):
        return data


def decode_dict(data: dict) -> dict:
    keys_to_decode = [
        'title', 'description', 'name', 'source',
        'tag', 'category'
    ]

    for key, value in data.items():
        if key in keys_to_decode:
            try:
                data[key] = decode_str(value)
            except (UnicodeEncodeError, UnicodeDecodeError):
                continue

    return data
