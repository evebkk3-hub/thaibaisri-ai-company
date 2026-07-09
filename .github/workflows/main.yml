import os
import json
import smtplib
from datetime import datetime, timezone, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import random

BKK = timezone(timedelta(hours=7))
TODAY = datetime.now(BKK).strftime("%d %B %Y")
TODAY_ISO = datetime.now(BKK).strftime("%Y-%m-%d")

CHANNEL_NAME = os.getenv("CHANNEL_NAME", "Thai Baisri")
CURRENT_SUBSCRIBERS = int(os.getenv("CURRENT_SUBSCRIBERS", "72200"))
TARGET_SUBSCRIBERS = int(os.getenv("TARGET_SUBSCRIBERS", "100000"))
MAIL_TO = os.getenv("MAIL_TO", "eveth99@hotmail.com")

TOPIC_POOL = [
    {
        "topic": "พานไหว้ครูบายศรีแบบง่าย ใช้ได้จริง สำหรับนักเรียน นักศึกษา และมือใหม่",
        "keywords": ["พานไหว้ครู", "บายศรี", "วิธีทำพาน", "ไหว้ครู", "งานฝีมือไทย"],
        "reason": "ตรงฤดูกาลเปิดเทอม/ไหว้ครู และตรงจุดแข็งของช่องด้านบายศรีและงานฝีมือไทย",
        "score": 97,
    },
    {
        "topic": "บายศรีสู่ขวัญแบบประหยัด ทำเองได้ งบไม่สูง แต่ดูสวย",
        "keywords": ["บายศรีสู่ขวัญ", "บายศรีประหยัด", "ทำบายศรี", "พิธีไทย"],
        "reason": "เหมาะกับคนจัดงานเองและค้นหาวิธีลดงบ แต่ยังต้องการความสวยงาม",
        "score": 94,
    },
    {
        "topic": "5 จุดที่มือใหม่ทำบายศรีพลาดบ่อย และวิธีแก้ให้สวยขึ้นทันที",
        "keywords": ["ทำบายศรี", "มือใหม่", "งานใบตอง", "แก้ปัญหา"],
        "reason": "คอนเทนต์แก้ปัญหามีโอกาส retention สูง เพราะผู้ชมอยากดูวิธีแก้จนจบ",
        "score": 93,
    },
    {
        "topic": "ASMR พับใบตอง ทำบายศรี เสียงธรรมชาติ ผ่อนคลาย",
        "keywords": ["ASMR", "พับใบตอง", "บายศรี", "ผ่อนคลาย", "งานฝีมือ"],
        "reason": "เป็นมุมใหม่ที่ต่างจากคลิปสอนทั่วไป และเหมาะสำหรับ Shorts/Reels",
        "score": 89,
    },
    {
        "topic": "ทำพานบายศรีให้ดูแพง ด้วยเทคนิคจัดชั้นและเลือกสี",
        "keywords": ["พานบายศรี", "เทคนิค", "จัดพาน", "งานพิธี"],
        "reason": "คำว่า 'ดูแพง' ช่วยเพิ่มแรงจูงใจในการคลิก และให้คุณค่าเชิงเทคนิค",
        "score": 91,
    },
]

THUMBNAIL_FORMATS = [
    'ก่อน-หลัง: ซ้ายเป็นวัสดุธรรมดา ขวาเป็นพานสำเร็จ ข้อความ "มือใหม่ก็ทำได้"',
    'ภาพพานสำเร็จเต็มจอ ข้อความใหญ่ "พานไหว้ครู" + "ทำเองได้"',
    'ภาพมือกำลังจัดบายศรี ข้อความ "3 เทคนิคให้สวยขึ้น"',
    'ภาพพานสวย + ป้ายราคา ข้อความ "งบประหยัด แต่ดูแพง"',
]

def load_history():
    path = Path("data/history.json")
    if not path.exists():
        return {"used_topics": []}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"used_topics": []}

def save_history(history):
    path = Path("data/history.json")
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")

def choose_topic(history):
    used = set(history.get("used_topics", []))
    candidates = [t for t in TOPIC_POOL if t["topic"] not in used]
    if not candidates:
        candidates = TOPIC_POOL
        history["used_topics"] = []
    candidates.sort(key=lambda x: x["score"], reverse=True)
    return candidates[0]

def build_report():
    history = load_history()
    topic = choose_topic(history)
    remaining = TARGET_SUBSCRIBERS - CURRENT_SUBSCRIBERS
    progress = CURRENT_SUBSCRIBERS / TARGET_SUBSCRIBERS * 100
    daily_target_90 = max(1, round(remaining / 90))
    thumbnail = THUMBNAIL_FORMATS[hash(TODAY_ISO) % len(THUMBNAIL_FORMATS)]

    titles = [
        f"{topic['topic']} | สอนละเอียดทีละขั้นตอน",
        f"มือใหม่ต้องดู! {topic['topic']}",
        f"ทำเองได้จริง: {topic['topic']}",
        f"{topic['topic']} แบบง่าย สวย และประหยัด",
        f"เทคนิคจาก Thai Baisri: {topic['topic']}",
    ]

    hooks = [
        f"ถ้าคุณกำลังหาแนวทางทำ {topic['keywords'][0]} คลิปนี้จะพาทำแบบเข้าใจง่าย ตั้งแต่เริ่มจนเสร็จ",
        f"หลายคนคิดว่า {topic['keywords'][0]} ทำยาก แต่วันนี้เราจะทำให้ดูว่าเริ่มต้นได้ไม่ยากเลย",
        f"วันนี้ Thai Baisri จะพาทำงานฝีมือไทยแบบง่าย ใช้ได้จริง และเหมาะกับมือใหม่",
    ]

    report = f"""
Thai Baisri AI Company V1
CEO Daily Growth Report
วันที่: {TODAY}
เป้าหมายหลัก: 100,000 Subscribers

==============================
1) CEO SUMMARY
==============================

สถานะเป้าหมาย:
- Current Subscribers Estimate: {CURRENT_SUBSCRIBERS:,}
- Target Subscribers: {TARGET_SUBSCRIBERS:,}
- Remaining: {remaining:,}
- Progress: {progress:.2f}%
- Daily Growth Target เฉลี่ยใน 90 วัน: {daily_target_90:,} subscribers/day

CEO Decision:
วันนี้ทุกคอนเทนต์ต้องเน้น 3 อย่าง:
1. คนค้นหาได้จริง
2. มือใหม่ดูแล้วทำตามได้
3. กระตุ้นให้กดติดตามเพื่อดูตอนต่อไป

==============================
2) RESEARCH DEPARTMENT
==============================

หัวข้อที่มีศักยภาพสูงวันนี้:
"{topic['topic']}"

Reason:
{topic['reason']}

Opportunity Score:
{topic['score']}/100

==============================
3) SEO DEPARTMENT
==============================

Keyword ที่ควรใช้:
{", ".join(topic["keywords"])}

Hashtag:
#ThaiBaisri #บายศรี #งานฝีมือไทย #DIYThaiCraft #{topic['keywords'][0].replace(" ", "")}

==============================
4) TITLE TEAM
==============================

Title Options:
1. {titles[0]}
2. {titles[1]}
3. {titles[2]}
4. {titles[3]}
5. {titles[4]}

CEO Recommended Title:
{titles[3]}

==============================
5) THUMBNAIL TEAM
==============================

Thumbnail Concept:
{thumbnail}

Text on Thumbnail:
- "ทำเองได้"
- "มือใหม่ก็สวย"
- "{topic['keywords'][0]}"

==============================
6) SCRIPT TEAM
==============================

Hook 15 วินาทีแรก:
"{hooks[hash(topic['topic']) % len(hooks)]}"

Video Outline:
1. เปิดด้วยภาพผลงานสำเร็จ 5-7 วินาที
2. บอกปัญหาของผู้ชม เช่น ทำไม่เป็น / กลัวไม่สวย / งบจำกัด
3. แนะนำวัสดุทั้งหมด
4. สอนขั้นตอนหลักทีละขั้น
5. แทรกเทคนิคที่ทำให้งานดูสวยขึ้น
6. สรุปผลงานก่อน-หลัง
7. Call to Action: ให้ผู้ชมคอมเมนต์ว่าอยากให้สอนแบบไหนต่อ

==============================
7) SHORTS DEPARTMENT
==============================

Shorts ที่ควรตัดวันนี้:
1. Before/After จากวัสดุธรรมดาเป็นงานสำเร็จ
2. 3 เทคนิคที่ทำให้งานดูสวยขึ้นทันที
3. ข้อผิดพลาดที่มือใหม่ทำบ่อย
4. คลิปเร็ว 30 วินาที สรุปขั้นตอนทั้งหมด

==============================
8) MARKETING DEPARTMENT
==============================

Post Facebook/Community:
"ใครกำลังเตรียมงานไหว้ครู/งานพิธี วันนี้ Thai Baisri มีไอเดียทำบายศรีแบบง่าย ใช้ได้จริง มือใหม่ก็ทำตามได้ ฝากติดตามคลิปใหม่วันนี้ค่ะ"

==============================
9) HR & PRODUCTIVITY REVIEW
==============================

Agent Performance:
- Research Agent: PASS
- SEO Agent: PASS
- Creative Agent: PASS
- Thumbnail Agent: NEEDS A/B TEST
- Growth Agent: PASS

CEO Order:
Thumbnail Team ต้องเสนออย่างน้อย 2 แบบก่อนเผยแพร่
ถ้า CTR ต่ำกว่า 5% หลังมีข้อมูลเพียงพอ ให้เปลี่ยน Thumbnail

==============================
10) DAILY ACTION PLAN
==============================

งานที่ต้องทำวันนี้:
1. ผลิตคลิปยาว 8-12 นาที จำนวน 1 คลิป
2. ตัด Shorts อย่างน้อย 3 คลิป
3. โพสต์ Community 1 ครั้ง
4. ปักคอมเมนต์ถามผู้ชมว่าอยากให้สอนอะไรต่อ
5. บันทึกผล CTR / View / Subscriber เพิ่ม เพื่อใช้ในรายงานวันถัดไป

==============================
CEO FINAL NOTE
==============================

เป้าหมาย 100,000 subscribers ต้องไม่พึ่งคลิปไวรัลอย่างเดียว
กลยุทธ์หลักคือทำคอนเทนต์ที่ค้นหาได้ยาวนาน + ตัด Shorts เพื่อดึงผู้ชมใหม่ + ทำซีรีส์ให้คนกดติดตามเพื่อรอดูตอนต่อไป
"""
    history.setdefault("used_topics", []).append(topic["topic"])
    save_history(history)
    return report

def send_email(subject, body):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    mail_from = os.getenv("MAIL_FROM", smtp_user)
    mail_to = os.getenv("MAIL_TO", MAIL_TO)

    missing = [k for k, v in {
        "SMTP_HOST": smtp_host,
        "SMTP_USER": smtp_user,
        "SMTP_PASSWORD": smtp_password,
        "MAIL_FROM": mail_from,
        "MAIL_TO": mail_to
    }.items() if not v]
    if missing:
        print("Missing email config:", ", ".join(missing))
        print("Report generated but not sent:")
        print(body)
        return False

    msg = MIMEMultipart()
    msg["From"] = mail_from
    msg["To"] = mail_to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)

    print(f"Email sent to {mail_to}")
    return True

def main():
    report = build_report()
    subject = f"Thai Baisri CEO Daily Growth Report - {TODAY_ISO}"
    sent = send_email(subject, report)
    Path("latest_report.txt").write_text(report, encoding="utf-8")
    print("Done. Sent:", sent)

if __name__ == "__main__":
    main()
