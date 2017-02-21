import requests

headers = {
}

files = {
    'Host': 'antenna.stage.mozaws.net',
    'Content-Type': 'multipart/form-data',
    'ProductName': 'Firefox',
    'Version': '1',
    'upload_file_minidump': open('small.dmp', 'rb')
}


resp = requests.post('https://antenna-loadtest.stage.mozaws.net/submit', headers=headers, files=files)
print(resp.status_code)
print(resp.text)
