import requests
import urllib
import os

def OptmizeImage(input_file_path, output_file_path=None):
    file_extension = os.path.splitext(input_file_path)[1].lower()
    if file_extension == '.png':
        mime = 'image/png'
    elif file_extension == '.jpg':
        mime = 'image/jpeg'
    elif file_extension == '.jpeg':
        mime = 'image/jpeg'

    if not os.path.isfile(input_file_path):
        print(f"Unsupported Format")
    name = input_file_path.split('/')[-1]

    files = {'files': (name, open(input_file_path, 'rb'), mime)}

    url = f'http://api.resmush.it/?qlty=80'

    try:
        response = requests.post(url, files=files, timeout=5)
        result = response.json()

        dest_url = result['dest']

        if not output_file_path:
            output_file_path = os.path.join(os.getcwd(), f"{os.urandom(8).hex()}.jpg")
        urllib.request.urlretrieve(dest_url, output_file_path)
        print(True)
    except FileNotFoundError:
        print("File/Folder not found.")
    except Exception as e:
        print(f"Error: {e}")


def DynamicCompress(input_file_path, output_file_path=None,qlty=None):
    file_extension = os.path.splitext(input_file_path)[1].lower()
    if file_extension == '.png':
        mime = 'image/png'
    elif file_extension == '.jpg':
        mime = 'image/jpeg'
    elif file_extension == '.jpeg':
        mime = 'image/jpeg'

    if not os.path.isfile(input_file_path):
        print(f"Unsupported Format")
    name = input_file_path.split('/')[-1]

    files = {'files': (name, open(input_file_path, 'rb'), mime)}
    if qlty == '':
        qlty=80

    url = f'http://api.resmush.it/?qlty={qlty}'

    try:
        response = requests.post(url, files=files, timeout=5)
        result = response.json()

        dest_url = result['dest']

        if not output_file_path:
            output_file_path = os.path.join(os.getcwd(), f"{os.urandom(8).hex()}.jpg")
        urllib.request.urlretrieve(dest_url, output_file_path)
        print(f"Image downloaded successfully as {output_file_path}")
    except FileNotFoundError:
        print("File/Folder not found.")
    except Exception as e:
        print(f"Error: {e}")
