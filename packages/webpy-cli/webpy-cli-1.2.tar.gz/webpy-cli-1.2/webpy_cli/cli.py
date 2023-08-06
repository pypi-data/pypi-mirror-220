import argparse
import os
import requests
import zipfile

def get_latest_release(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        release_data = response.json()
        tag_name = release_data["tag_name"]
        assets = release_data["assets"]
        return tag_name, assets
    else:
        response.raise_for_status()

def create_project(name):
    owner = "tj-likes-coding"
    repo = "webpy"
    
    access_token = "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"
    
    headers = {}
    headers["Authorization"] = f"token {access_token}"
    
    try:
        latest_tag, assets = get_latest_release(owner, repo)
        print(f"Latest release: {latest_tag}")
        print("Assets:")
        for asset in assets:
            if asset['name'] == "cli.zip":
                # download and unzip the asset and add the files to the "name" directory
                
                if not os.path.exists(name):
                    os.makedirs(name)
                
                asset_url = asset["browser_download_url"]
                download_path = os.path.join(name, "cli.zip")
                
                # Download the asset
                response = requests.get(asset_url)
                response.raise_for_status()
                
                # Save the asset to the download path
                with open(download_path, "wb") as f:
                    f.write(response.content)
                
                # Unzip the asset
                with zipfile.ZipFile(download_path, "r") as zip_ref:
                    zip_ref.extractall(name)
                
                # Remove the downloaded zip file
                os.remove(download_path)
                
                break
            else:
                continue
            
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='CLI tool for the python WebPy Framework')
    subparsers = parser.add_subparsers(dest='command')
    
    create_parser = subparsers.add_parser('create', help='Create a new project')
    create_parser.add_argument('name', metavar='name', type=str, help='name of the project')
    
    args = parser.parse_args()

    if args.command == 'create':
        create_project(args.name)
    else:
        print('Invalid command. Use "pyweb create <project name>" to create a new project.')

if __name__ == '__main__':
    main()
