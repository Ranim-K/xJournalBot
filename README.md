# 📓 xJournal Bot

A minimalist Telegram journaling bot that helps you reflect and write daily entries — stored privately in your own group or channel.

---

## 🏗️ Create Your Private Journal Channel

To store journals securely:

1. **Create a Telegram Group** or a **Channel with discussion enabled**.
2. **Add your bot** as an **admin** with permission to send messages.
3. **Send a message in a thread** to create a topic (e.g., "Journals").
4. Right-click (desktop) or long-press (mobile) on the topic → **Copy Topic ID**.  
   If your client doesn’t show it, you can also extract it via the Telegram API.
5. Paste the `GROUP_CHAT_ID` and `JOURNAL_TOPIC_ID` into your bot's code:
    ```python
    BOT_TOKEN = "YOUR_BOT_TOKEN"
    YOUR_USER_ID = "YOUR_USER_ID"
    GROUP_CHAT_ID = "YOUR_GROUP_CHAT_ID"
    JOURNAL_TOPIC_ID = 2  # or whatever topic ID you copied
    ```
6. ✅ That’s it! Journals will now be posted automatically to that thread.

🛑 **Only you and the bot** should have access to this group for maximum privacy.

---

## 📋 Bot Commands

| Command | Description         |
|---------|---------------------|
| /start  | Start or reset the bot |
| /help   | Show help information  |

---

## 🛡️ Privacy

**xJournal** is designed with **privacy in mind**.  
No data is sent to external servers — everything stays in your **own private Telegram group**.

---

## 🤝 Contributing

Have an idea or improvement?

1. Fork this repo.
2. Make your changes.
3. Submit a pull request.

✨ Bug fixes, new features, and even README improvements are welcome!

---

## 📄 License

Licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.

---

> Made with 💙 by [Ranim-K](https://github.com/Ranim-K) — because journaling is power.
