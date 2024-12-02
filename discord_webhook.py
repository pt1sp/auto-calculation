import requests

class DiscordWH:
    def __init__(self, url):
        self.api = url

    def send_message(self, message, username="default_user", avatar='https://static-00.iconduck.com/assets.00/discord-icon-2048x2048-wooh9l0j.png'):
        request_body = {
            'content': message,
            'username': username,
            'avatar_url': avatar,
        }
        res = requests.post(self.api, data=request_body)
        print(f"ステータスコード{res.status_code}")

# 関数を追加
def send_to_discord(message):
    url = 'https://discord.com/api/webhooks/1313076808987709481/P17fxvFSnL92sZlTYESHk3aUr-iYE5aSaFGgV-ofCZfEbz6gyOpCZHUZPA_vfF7Y3FLo'
    username = 'mk8dx自動集計bot'
    avatar = 'https://cdn.discordapp.com/attachments/1313077033013608479/1313078332845330482/92.png?ex=674ed2fe&is=674d817e&hm=8c95bfb9ccefb2580f3734b771dcbf62b68be9e16e6719253ce314c192ae273a&'

    # DiscordWH のインスタンス化と送信
    hook = DiscordWH(url)
    hook.send_message(message=message, username=username, avatar=avatar)
