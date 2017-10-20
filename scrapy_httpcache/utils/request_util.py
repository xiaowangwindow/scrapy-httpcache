from scrapy.utils import request


def fingerprint(r):
    return request.request_fingerprint(r)


def convert_header(header):
    if isinstance(header, dict):
        return {convert_header(k): convert_header(v) for k, v in header.items()}
    elif isinstance(header, list):
        return [convert_header(v) for v in header]
    elif isinstance(header, bytes):
        return header.decode('utf8')
    else:
        return header


if __name__ == '__main__':
    pass
