import aiohttp
import asyncio
import random
import string
import base64
from colorama import  Fore
import time
#⚠️Warning
# EN/ I am not responsible if you use this for illegal purposes
# VI/ Tôi không chịu trách nhiệm nếu  bạn sử dụng vào mục đích phi pháp!

print(Fore.RED + "Tôi không chịu trách nhiệm nếu bạn sử dụng vào mục đích phi pháp" + Fore.RESET)

username = str(input("NGL UserName -> "))
multi_username = []
sl = int(input("Số lần spam ( nên < 50 ) -> "))
question = str(input("Câu hỏi -> "))
url = "https://ngl.link/api/submit"
requests_per_second = 5  # Số request tối đa mỗi giây
proxy_list = []  # Thêm proxy

base_delay = 0.5 / requests_per_second  # Độ trễ ban đầu (giây)
random_millis = 500  # Thời gian trễ ngẫu nhiên tối đa (mili giây)
max_delay = 30  # Giới hạn delay tối đa nếu bị 429 liên tục

error_429_count = 0
dynamic_rps = requests_per_second


def generate_device_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
def get_dynamic_delay():
    return base_delay + random.uniform(0, random_millis / 1000)
def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/115.0.1901.203",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (iPad; CPU OS 15_3 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/15.3 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.1.2 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Brave/119.0.0.0 Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Linux; U; Android 11; en-us; Moto G Power) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; U; Android 10; en-us; SM-G960U) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 9; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Version/13.1.2 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/116.0.1938.81",
        "Mozilla/5.0 (Linux; Android 10; SAMSUNG SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.98 Mobile Safari/537.36",
        "Mozilla/5.0 (iPad; CPU OS 16_1 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Brave/120.0.0.0 Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_5) AppleWebKit/537.36 (KHTML, like Gecko) Version/15.6 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.2 Mobile/15E148 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 8.1; Nexus 6P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Mobile Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Version/18.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Opera/101.0.0.0 Safari/537.36"
    ]
    return random.choice(user_agents)

print(get_random_user_agent())

def get_random_proxy():
    return random.choice(proxy_list) if proxy_list else None



def get_human_like_base64():
    def random_unicode():
        return random.choice([
            '🌟', '🔥', '💀', '🎃', '👽', '💡', '🎵', '✨', '🚀', '💎', '❤️', '🌀',
            '⚡', '🐍', '🤖', '👾', '💲', '🧩', '🔮', '💬', '📌', '🔑', '🎯', '🎲',
            '🔗', '🔓', '💥', '💰', '🚧', '💣', '📡', '🔍', '🕵️', '🔊', '🖥️',
            '📲', '📟', '🔠', '📀', '📂', '🗂️', '🧪', '🧬', '™', '©', '®', '§',
            '¶', '∑', '∆', '∞', '≈', '≠', '±', '√', 'µ', 'Ω', 'λ', 'φ', 'π', 'ψ',
            'á', 'à', 'ả', 'ã', 'ạ', 'ă', 'ắ', 'ằ', 'ẳ', 'ẵ', 'ặ', 'â', 'ấ', 'ầ', 'ẩ', 'ẫ', 'ậ',
            'é', 'è', 'ẻ', 'ẽ', 'ẹ', 'ê', 'ế', 'ề', 'ể', 'ễ', 'ệ',
            'ó', 'ò', 'ỏ', 'õ', 'ọ', 'ô', 'ố', 'ồ', 'ổ', 'ỗ', 'ộ', 'ơ', 'ớ', 'ờ', 'ở', 'ỡ', 'ợ',
            'ú', 'ù', 'ủ', 'ũ', 'ụ', 'ư', 'ứ', 'ừ', 'ử', 'ữ', 'ự',
            'í', 'ì', 'ỉ', 'ĩ', 'ị',
            'ý', 'ỳ', 'ỷ', 'ỹ', 'ỵ',
            'đ', 'Đ',
            'あ', 'い', 'う', 'え', 'お', 'か', 'き', 'く', 'け', 'こ',
            'さ', 'し', 'す', 'せ', 'そ', 'た', 'ち', 'つ', 'て', 'と',
            'な', 'に', 'ぬ', 'ね', 'の', 'は', 'ひ', 'ふ', 'へ', 'ほ',
            'ま', 'み', 'む', 'め', 'も', 'や', 'ゆ', 'よ', 'ら', 'り', 'る', 'れ', 'ろ',
            'わ', 'を', 'ん', 'ア', 'イ', 'ウ', 'エ', 'オ', 'カ', 'キ', 'ク', 'ケ', 'コ',
            'サ', 'シ', 'ス', 'セ', 'ソ', 'タ', 'チ', 'ツ', 'テ', 'ト',
            'ナ', 'ニ', 'ヌ', 'ネ', 'ノ', 'ハ', 'ヒ', 'フ', 'ヘ', 'ホ',
            'マ', 'ミ', 'ム', 'メ', 'モ', 'ヤ', 'ユ', 'ヨ', 'ラ', 'リ', 'ル', 'レ', 'ロ',
            'ワ', 'ヲ', 'ン',
            '你', '好', '我', '是', '中', '国', '人', '学', '习', '汉', '字', '爱', '吃', '饭', '喝', '水',
            '가', '나', '다', '라', '마', '바', '사', '아', '자', '차', '카', '타', '파', '하',
            '각', '낙', '닥', '락', '막', '박', '삭', '악', '작', '착', '칵', '탁', '팍', '학',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+',
            '{', '}', '[', ']', '|', '\\', ':', ';', '"', "'", '<', '>', ',', '.', '?', '/'
        ])

    def modify_b64(b64_str):
        if random.random() < 0.3:
            b64_str = b64_str[::-1]

        if random.random() < 0.5:
            b64_str = random_unicode() + b64_str + random.choice(["-", "_", " "])

        if "=" in b64_str:
            b64_str = b64_str.replace('=', random.choice(["", "-", "_", random_unicode()]))

        return b64_str

    raw_bytes = [bytes([random.randint(0, 255) for _ in range(3)]) for _ in range(3)]
    b64_1, b64_2, b64_3 = [base64.b64encode(rb).decode() for rb in raw_bytes]

    b64_1 = modify_b64(b64_1)
    b64_2 = modify_b64(b64_2)
    b64_3 = modify_b64(b64_3)

    return b64_1, b64_2, b64_3



def get_random_headers():
    b64_1, b64_2, b64_3 = get_human_like_base64()
    return {
        "accept": "*/*",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://ngl.link",
        "referer": f"https://ngl.link/{username}",
        "x-requested-with": "XMLHttpRequest",
        "User-Agent": get_random_user_agent(),
        "sec-fetch-site": random.choice(["same-origin", "cross-site"]),
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "X-Auth-Session": b64_1,
        "X-Verify-Token": b64_2,
        "X-Client-Signature": b64_3,
        "X-Forwarded-For": "",
        "Client-IP": "",
        "Via": "",
    }


request_times = []


async def send_question(session, i, use_proxy=True):
    global error_429_count, dynamic_rps, request_times

    device_id = generate_device_id()
    random_bytes = ''.join(random.choices(string.ascii_letters + string.digits, k=2))
    payload = f"username={username}&question={question}{random_bytes}&deviceId={device_id}&gameSlug=&referrer="
    headers = get_random_headers()
    proxy = get_random_proxy() if use_proxy else None 

    start_time = time.time()

    try:
        async with session.post(url, data=payload, headers=headers, proxy=proxy) as response:
            end_time = time.time()
            elapsed_time = end_time - start_time

            request_times.append(elapsed_time)
            if len(request_times) > 100:
                request_times.pop(0)

            if response.status == 200:
                data = await response.json()
                print(Fore.GREEN + f"✅ Sent {i + 1}: {data.get('questionId')} | {data.get('userRegion')} | {device_id} | ⏳ {elapsed_time:.2f}s" + Fore.RESET)
                error_429_count = 0
                dynamic_rps = min(dynamic_rps + 1, requests_per_second)
            elif response.status == 429:
                error_429_count += 1
                dynamic_rps = max(dynamic_rps / 2, 1)
                print(Fore.YELLOW + f"⚠️ 429 Too Many Requests! Giảm tốc độ xuống {dynamic_rps:.2f} RPS" + Fore.RESET)
                await asyncio.sleep(min(error_429_count * 5, max_delay))
            else:
                print(Fore.RED + f"❌ Server lỗi {response.status} - {await response.text()}" + Fore.RESET)

    except Exception as e:
        print(Fore.RED + f"❌ Lỗi khi gửi câu {i + 1}: {e}" + Fore.RESET)
        await asyncio.sleep(5)



async def check_server_status(session):
    global error_429_count
    device_id = generate_device_id()
    test_payload = f"username={username}&question=test_check&deviceId={device_id}&gameSlug=&referrer="
    headers = get_random_headers()
    proxy = get_random_proxy()
    async with session.post(url, data=test_payload, headers=headers, proxy=proxy) as response:
        if response.status == 200:
            print( Fore.GREEN +  "✅ Server ổn định, tiếp tục gửi!" + Fore.RESET)
            error_429_count = 0
            return True
        elif response.status == 429:
            print(Fore.RED + "⏳ Server vẫn bị 429, chờ thêm..." + Fore.RESET)
            return False
        return False




async def main():
    global dynamic_rps
    async with aiohttp.ClientSession() as session:
        for i in range(sl):
            await send_question(session, i)
            await asyncio.sleep(1 / dynamic_rps)
            if error_429_count >= 2:
                print(Fore.RED  + "tạm dừng 60s..." + Fore.RESET)
                await asyncio.sleep(60)
                await check_server_status(session)
        print(f"Bị chặn {error_429_count} lần")
asyncio.run(main())


#By @kenftr
