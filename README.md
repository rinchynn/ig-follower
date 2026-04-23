# Instagram Follower Bot

Terminal дээр ажилладаг меню-тэй Instagram follower bot. `instagrapi` ашиглан target account-уудын follower-оос follow хийх, non-follower хүмүүсийг unfollow хийх, мөн follow/unfollow холбоотой үндсэн үйлдлүүдийг CLI орчноос ажиллуулна.

## Features

| Меню | Үйлдэл |
|------|--------|
| **1** | Зорилтот account-уудын follower-уудыг автоматаар follow хийх |
| **2** | Таныг буцааж follow хийгээгүй хүмүүсийг unfollow хийх |
| **3** | Account-ийн follower / following тоо харах |
| **4** | Зөвхөн bot-аар follow хийсэн хүмүүсийг unfollow хийх |
| **5** | Following жагсаалтаа харах |

Bot-аар follow хийсэн хүмүүсийн ID-г `followed_by_bot.json` файлд хадгалдаг тул дараа нь зөвхөн bot follow хийсэн хэрэглэгчдийг сонгомлоор unfollow хийх боломжтой.

## Clone хийх

GitHub-оос төслийг татах:

```bash
git clone https://github.com/rinchynn/ig-follower.git
cd ig-follower
```

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

`config.example.py` файлыг `config.py` болгож хуулна:

```bash
cp config.example.py config.py
```

Дараа нь `config.py` файлаа засна:

```python
USERNAME = "таны_instagram_нэр"
PASSWORD = "таны_нууц_үг"
TARGET_ACCOUNTS = ["target_account1", "target_account2"]
MAX_FOLLOWS_PER_DAY = 50
FOLLOW_DELAY = [30, 60]
```

### Config тайлбар

- **`USERNAME`** — Таны Instagram username
- **`PASSWORD`** — Таны Instagram password
- **`TARGET_ACCOUNTS`** — Эдгээр account-уудын follower-оос bot follow хийнэ
- **`MAX_FOLLOWS_PER_DAY`** — Өдөрт follow хийх дээд тоо
- **`FOLLOW_DELAY`** — Follow бүрийн хооронд хүлээх хугацаа `[min, max]` секундээр

## Run

```bash
python bot.py
```

Script ажилласны дараа menu гарч ирнэ. Та хүссэн үйлдлээ дугаараар нь сонгож ажиллуулна.

## Login / Session

- Session автоматаар `session.json` файлд хадгалагдана
- Дараагийн удаа ажиллуулахад дахин login хийх шаардлагагүй байж болно
- **2FA** дэмждэг — баталгаажуулах код terminal дээр асууна
- **Challenge** (email/SMS verification) гарвал мөн terminal дээр үргэлжлүүлэн шийдэж болно

## Project structure

```bash
ig-follower/
├── bot.py              # Үндсэн скрипт
├── config.py           # Таны тохиргоо (gitignored)
├── config.example.py   # Тохиргооны жишээ файл
├── requirements.txt    # Төслийн dependency-үүд
└── .gitignore
```

## Notes

- `config.py` болон `session.json`-г GitHub руу push хийж болохгүй
- Instagram rate limit, challenge, temporary restriction гарах эрсдэлтэй
- Хэт хурдан follow/unfollow хийх нь account-д эрсдэл үүсгэж болно

## Warning

Энэ төсөл нь Instagram-ийн official бус API ашигладаг. Иймээс account дээр challenge, rate limit, temporary block зэрэг эрсдэл үүсэж болзошгүй. Өөрийн эрсдэл дээр ашиглана.
