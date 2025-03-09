reddit_login = {
    "client_id" : "***************",
    "secret_key" : "***************",,
    "login_data" : {
        "username":"***************",,
        "password": "***************",,
        "grant_type": "password"
    },
    "headers" : {'User-Agent': 'MyAPI/0.0.1'},
    "auth" : "https://www.reddit.com/api/v1/access_token",
    "url" : "https://oauth.reddit.com/r/SBU/"
}

api_call = ["hot", "new", "top", "controversial"]

s3_credentials = {
    "aws_access_key_id" : "***************",
    "aws_secret_access_key" : "***************",,
    "s3_url": "s3://prasad-reditt-test/bronze/"
}
