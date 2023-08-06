import requests

def testLicense(public_key: str, license: str):
    try:
        response = requests.get("https://api.mercury.candor.slz.lol")
        json_response = response.json()
        isLicenseValid = json_response.get('is_license_valid', False)
        return isLicenseValid
    except requests.exceptions.RequestException:
        print("Error: Unable to fetch license information.")
        return False