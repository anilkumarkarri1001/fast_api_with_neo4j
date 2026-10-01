import json
from encryption import decrypt_value 

def decrypt_response_data(encrypted_response: str):
    try:
        # 1. Decrypt the encrypted Base64 value
        decrypted_json = decrypt_value(encrypted_response)

        # 2. Convert JSON string back into Python object
        data = json.loads(decrypted_json)

        print("✅ Decryption successful")
        print("✅ Valid JSON")
        print(json.dumps(data, indent=4, ensure_ascii=False))

        return data

    except Exception as e:
        print("❌ Decryption/JSON parsing failed")
        print("Error:", str(e))
        return None
res = decrypt_response_data("3fjy/nHtjolQIPiEYufiY9dNkTyowh0k+PXH5CKS6b5Z44c3zzZ4SgIbohL5450aALjsJ+2dXmPozcTqPYyH53zMJWvCbe0n2DqWx55pxr5Ya8KZhm/GWP73mH+y0W2pnvmKgb64fSc+I6huR2Tk9e14nYegq32lHs3l3LVzYcYjd/Uqfz7f+Xkkyh751KqMBKAF1rVdCX+ysTcScfacBmZp95jl++MOKemvAQMXXWD141VAEFeVI3TmwgIavHxPI2td9AepJ4YOoal6sQJLf0h9LPpXaFILyFEOL23ku9xKmUJhbdh0mCcIYhZ51h/A1qnJ2f5I8LBPVV2vAcuS4686MhlOWJhJ6kvhO+sv3sTDj47k85coTWo0p6rstnHpqaABI+Bq4CVF7phJomsDsYYcIx6bwBWsSs1BNH666xbu1chHXUxNShvbN3yEr6WYmOAzBhXglo0kP3DFuOtbgpFVf+0qQgNK2vSEYfmw6Xe41WizRimZi4nbuKqYr+f7m899ccA=")
print(res)    