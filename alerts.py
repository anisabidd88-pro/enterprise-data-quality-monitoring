
import os
import smtplib
from email.message import EmailMessage
import requests

def send_slack(message, webhook_url):
    if not webhook_url:
        print('No Slack webhook provided; skipping Slack alert.')
        return False
    payload = {'text': message}
    try:
        r = requests.post(webhook_url, json=payload, timeout=5)
        return r.status_code == 200
    except Exception as e:
        print('Slack alert failed:', e)
        return False

def send_email(subject, body, cfg):
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = cfg.get('FROM')
        msg['To'] = cfg.get('TO')
        msg.set_content(body)
        with smtplib.SMTP(cfg.get('SMTP_SERVER'), int(cfg.get('SMTP_PORT',587))) as s:
            s.starttls()
            s.login(cfg.get('SMTP_USER'), cfg.get('SMTP_PASS'))
            s.send_message(msg)
        return True
    except Exception as e:
        print('Email failed:', e)
        return False

def maybe_alert(low_score_records):
    if not low_score_records:
        return
    webhook = os.getenv('SLACK_WEBHOOK')
    smtp_cfg = {
        "SMTP_SERVER": os.getenv('SMTP_SERVER'),
        "SMTP_PORT": os.getenv('SMTP_PORT'),
        "SMTP_USER": os.getenv('SMTP_USER'),
        "SMTP_PASS": os.getenv('SMTP_PASS'),
        "FROM": os.getenv('ALERT_EMAIL_FROM'),
        "TO": os.getenv('ALERT_EMAIL_TO')
    }
    text = "Data Quality Alert: low scores detected:\n" + "\n".join([f"{r['source']}: {r['score']}" for r in low_score_records])
    print("ALERT:", text)
    send_slack(text, webhook)
    if smtp_cfg.get('SMTP_SERVER'):
        send_email("Data Quality Alert", text, smtp_cfg)
