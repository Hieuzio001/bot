import discord
from discord.ext import commands, tasks
from datetime import datetime, time, timedelta

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 🛠 CẤU HÌNH
channel_id = 1395784873708486656  # ID của channel cần giới hạn truy cập

# 📅 Lịch truy cập cho từng người
user_schedules = {
    994084789697134592: [  # <@994084789697134592>
        {"start": time(4, 0), "end": time(7, 0)},
        {"start": time(15, 0), "end": time(18, 0)}
    ],
    1284898656415125586: [  # <@1284898656415125586>
        {"start": time(11, 0), "end": time(15, 0)},
        {"start": time(21, 0), "end": time(23, 59, 59)}
    ],
    1134008850895343667: [  # <@1134008850895343667>
        {"start": time(0, 0), "end": time(4, 0)}
    ],
    960787999833079881: [  # <@960787999833079881>
        {"start": time(7, 0), "end": time(11, 0)},
        {"start": time(18, 0), "end": time(21, 0)}
    ]
}

# 👉 DÙNG GIỜ VIỆT NAM
def get_vietnam_time():
    return (datetime.utcnow() + timedelta(hours=7)).time()

@bot.event
async def on_ready():
    print(f"✅ Bot đang hoạt động: {bot.user}")
    update_permissions.start()

@tasks.loop(minutes=1)
async def update_permissions():
    now = get_vietnam_time()
    channel = bot.get_channel(channel_id)

    for user_id, intervals in user_schedules.items():
        member = channel.guild.get_member(user_id)
        if not member:
            continue

        # Kiểm tra có nằm trong bất kỳ khoảng thời gian nào không
        allowed = any(interval['start'] <= now <= interval['end'] for interval in intervals)

        if allowed:
            await channel.set_permissions(member, view_channel=True, send_messages=True)
        else:
            await channel.set_permissions(member, overwrite=None)

# 📘 Lệnh xem lịch của tất cả user
@bot.command()
async def xemlich(ctx):
    result = ""
    for uid, intervals in user_schedules.items():
        member = ctx.guild.get_member(uid)
        if member:
            lich = "\n".join([f"  - {i['start'].strftime('%H:%M')} → {i['end'].strftime('%H:%M')}" for i in intervals])
            result += f"{member.mention}:\n{lich}\n"
    await ctx.send("📅 **Lịch truy cập hiện tại:**\n" + result)

bot.run("MTQwMTk0OTQ5MDIzOTI0NjQzNw.GNf6RH.fYZ3M8Bw7q5vTfgp9FL9wL-z_fTYvy87DMVXMA")  # ← Thay bằng Token thực của bạn
