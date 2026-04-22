"""
Instagram Follower Bot (instagrapi)
⚠️  АНХААРУУЛГА: Аккаунт блоклогдох эрсдэлтэй.
"""

import sys
import time
import random
import json
import os
from instagrapi import Client
from instagrapi.exceptions import (
    LoginRequired,
    ChallengeRequired,
    TwoFactorRequired,
)

from config import (
    USERNAME,
    PASSWORD,
    TARGET_ACCOUNTS,
    MAX_FOLLOWS_PER_DAY,
    FOLLOW_DELAY,
)

SESSION_FILE = "session.json"
BOT_FOLLOWED_FILE = "followed_by_bot.json"


def load_bot_followed():
    """Бот дагасан хүмүүсийн жагсаалт уншина"""
    if os.path.exists(BOT_FOLLOWED_FILE):
        with open(BOT_FOLLOWED_FILE, "r") as f:
            return json.load(f)
    return []


def save_bot_followed(followed_list):
    """Бот дагасан хүмүүсийн жагсаалт хадгална"""
    with open(BOT_FOLLOWED_FILE, "w") as f:
        json.dump(followed_list, f)


def add_to_bot_followed(user_id):
    """Нэг хүнийг жагсаалтад нэмнэ"""
    followed = load_bot_followed()
    uid_str = str(user_id)
    if uid_str not in followed:
        followed.append(uid_str)
        save_bot_followed(followed)


def login(cl):
    """Нэвтрэх — session хадгалж дахин ашиглана"""

    if os.path.exists(SESSION_FILE):
        try:
            cl.load_settings(SESSION_FILE)
            cl.login(USERNAME, PASSWORD)
            cl.get_timeline_feed()  # session ажиллаж байгаа эсэхийг шалгана
            print("✅ Хадгалсан session-ээр нэвтэрлээ!")
            return
        except Exception:
            print("⚠️  Хуучин session дууссан, шинээр нэвтэрч байна...")

    try:
        cl.login(USERNAME, PASSWORD)
        cl.dump_settings(SESSION_FILE)
        print("✅ Амжилттай нэвтэрлээ!")
    except TwoFactorRequired:
        code = input("📱 2FA код оруулна уу: ").strip()
        cl.login(USERNAME, PASSWORD, verification_code=code)
        cl.dump_settings(SESSION_FILE)
        print("✅ 2FA-тай нэвтэрлээ!")
    except ChallengeRequired:
        print("\n⚠️  Instagram баталгаажуулалт шаардаж байна...")
        try:
            # Challenge эхлүүлэх
            cl.challenge_resolve_auto()
            print("   📧 Email эсвэл SMS рүү код илгээлээ.")
            code = input("   📱 Кодоо оруулна уу: ").strip()
            cl.challenge_send_security_code(code)
            cl.login(USERNAME, PASSWORD)
            cl.dump_settings(SESSION_FILE)
            print("✅ Баталгаажуулалт амжилттай!")
        except Exception as e:
            print(f"   ❌ Баталгаажуулалт амжилтгүй: {e}")
            print("   Instagram app дээрээ нэвтэрч баталгаажуулаад дахин оролдоно уу.")
            sys.exit(1)


def get_my_stats(cl):
    """Аккаунтын статистик"""
    try:
        info = cl.account_info()
        print(f"\n📊 {USERNAME}: {info.dict().get('follower_count', '?')} дагагч | {info.dict().get('following_count', '?')} дагаж буй")
    except Exception:
        print(f"\n📊 {USERNAME}: Статистик одоогоор татагдахгүй байна.")
    return 0, 0


def follow_target_followers(cl):
    """Зорилтот аккаунтуудын дагагчдыг дагана"""
    total_followed = 0
    per_account = MAX_FOLLOWS_PER_DAY // len(TARGET_ACCOUNTS)

    for account in TARGET_ACCOUNTS:
        print(f"\n📌 '{account}' аккаунтын дагагчдыг татаж байна...")
        try:
            user_id = cl.user_id_from_username(account)
            followers = cl.user_followers(user_id, amount=per_account)
        except Exception as e:
            print(f"   ❌ '{account}' - алдаа: {e}")
            print("   ⏳ Хэдэн минут хүлээгээд дахин оролдоно уу.")
            continue

        if not followers:
            print(f"   ❌ Дагагч олдсонгүй.")
            continue

        follower_ids = list(followers.keys())
        print(f"   ✅ {len(follower_ids)} дагагч олдлоо. Дагаж эхэлж байна...")

        for i, fid in enumerate(follower_ids, 1):
            try:
                cl.user_follow(fid)
                add_to_bot_followed(fid)
                total_followed += 1
                print(f"   [{i}/{len(follower_ids)}] ✅ дагалаа (нийт: {total_followed})")
            except Exception as e:
                print(f"   [{i}/{len(follower_ids)}] ❌ алдаа: {e}")


    print(f"\n🎉 Нийт {total_followed} хүнийг дагалаа!")


def unfollow_non_followers(cl):
    """Буцааж дагаагүй хүмүүсийг unfollow"""
    print("\n🔍 Дагагчид болон дагаж буй хүмүүсийг шалгаж байна...")
    my_id = cl.user_id
    try:
        followers = set(cl.user_followers(my_id).keys())
        following = set(cl.user_following(my_id).keys())
    except Exception as e:
        print(f"   ❌ Жагсаалт татаж чадсангүй: {e}")
        print("   ⏳ Хэдэн минут хүлээгээд дахин оролдоно уу.")
        return

    non_followers = following - followers
    if not non_followers:
        print("   Бүгд таныг буцааж дагасан байна! 🎉")
        return

    print(f"   {len(non_followers)} хүн таныг буцааж дагаагүй.")
    confirm = input("   Unfollow хийх үү? (y/n): ").strip().lower()
    if confirm != "y":
        print("   Цуцаллаа.")
        return

    for i, uid in enumerate(non_followers, 1):
        try:
            cl.user_unfollow(uid)
            print(f"   [{i}/{len(non_followers)}] unfollow ✅")
        except Exception as e:
            print(f"   [{i}/{len(non_followers)}] ❌ {e}")

    print(f"✅ Unfollow дууслаа.")


def unfollow_bot_followed(cl):
    """Зөвхөн бот дагасан хүмүүсийг unfollow хийнэ"""
    followed = load_bot_followed()

    if not followed:
        print("\n❌ Бот дагасан хүн бүртгэлд байхгүй байна.")
        return

    total = len(followed)
    print(f"\n🔄 Бот нийт {total} хүнийг дагасан бүртгэлтэй байна.")
    confirm = input(f"   Бүгдийг нь unfollow хийх үү? (y/n): ").strip().lower()
    if confirm != "y":
        print("   Цуцаллаа.")
        return

    unfollowed = 0
    remaining = list(followed)
    for i, uid_str in enumerate(followed, 1):
        try:
            cl.user_unfollow(int(uid_str))
            unfollowed += 1
            remaining.remove(uid_str)
            save_bot_followed(remaining)
            print(f"   [{i}/{total}] unfollow ✅")
        except Exception as e:
            print(f"   [{i}/{total}] ❌ {e}")

    print(f"\n✅ Нийт {unfollowed}/{total} хүнийг unfollow хийлээ!")


def show_my_following(cl):
    """Миний дагаж буй бүх хүмүүсийг сүүлийнхээс нь эхлэн харуулна"""
    print("\n🔍 Дагаж буй хүмүүсийг татаж байна...")
    my_id = cl.user_id
    try:
        following = cl.user_following(my_id)
    except Exception as e:
        print(f"   ❌ Жагсаалт татаж чадсангүй: {e}")
        return

    if not following:
        print("   ❌ Дагаж буй хүн байхгүй байна.")
        return

    # Instagram API сүүлд дагаснаас нь эхлэн буцаадаг
    users = list(following.values())
    total = len(users)
    print(f"\n📋 Нийт {total} хүнийг дагаж байна (сүүлийнхээс нь):")
    print("-" * 55)

    for i, user in enumerate(users, 1):
        username = user.username
        full_name = user.full_name or "-"
        is_private = "🔒" if user.is_private else "🌐"
        print(f"  {i}. {is_private} @{username} | {full_name}")

    print("-" * 55)
    print(f"Нийт: {total} хүн\n")


def show_menu():
    print("\n" + "=" * 45)
    print("     🤖 INSTAGRAM FOLLOWER BOT")
    print("=" * 45)
    print("  1. Дагагч нэмэх (follow target followers)")
    print("  2. Буцааж дагаагүй хүмүүсийг unfollow")
    print("  3. Статистик харах")
    print("  4. Ботоор дагасан хүмүүсийг unfollow")
    print("  5. Миний дагаж буй хүмүүс (сүүлийнхээс)")
    print("  0. Гарах")
    print("=" * 45)


def main():
    print("🔐 Instagram-руу нэвтэрч байна...")
    cl = Client()
    cl.delay_range = [1, 3]
    login(cl)
    get_my_stats(cl)

    while True:
        show_menu()
        choice = input("\n👉 Сонголт (0-5): ").strip()

        if choice == "1":
            follow_target_followers(cl)
        elif choice == "2":
            unfollow_non_followers(cl)
        elif choice == "3":
            get_my_stats(cl)
        elif choice == "4":
            unfollow_bot_followed(cl)
        elif choice == "5":
            show_my_following(cl)
        elif choice == "0":
            print("\n👋 Баяртай!")
            sys.exit(0)
        else:
            print("❌ Буруу сонголт.")


if __name__ == "__main__":
    main()
