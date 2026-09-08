import random
import asyncio
from highrise import BaseBot, ResponseError
from highrise.models import SessionMetadata, User, Position, Item

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.is_dancing = False
        # Track active dancing users: {user_id: asyncio.Task}
        self.user_dance_tasks = {}

        self.emote_dict = {
            "6": "dance-orangejuice",
            "18": "idle-attentive",
            "19": "emote-fairytwirl",
            "25": "emote-kissing-bound",
            "62": "emote-astronaut",
            "72": "emote-strike",
            "77": "idle-floattwirl",
            "84": "idle-space",
            "86": "emote-collapse",
            "90": "emote-flirtywave",
            "98": "idle-floating",
            "124": "emote-proposing",
            "125": "dance-aerobics",
            "127": "emote-smooch",
            "150": "emote-handstand",
            "158": "idle-relaxing",
            "159": "emote-uwu",
            "161": "dance-sheephop",
            "164": "emote-cute",
            "168": "emote-howl",
            "170": "dance-saunter",
            "173": "emote-yoga",
            "176": "emote-shy2",
            "179": "emote-launch",
            "183": "dance-griddy",
            "184": "emote-blowkisses",
            "186": "dance-fruity",
            "190": "dance-karma",
            "194": "dance-icecream",
            "196": "emote-curtsy",
            "201": "emote-roll",
            "204": "emote-knock",
            "221": "dance-kawaiigo",
            "226": "emote-charging",
            "229": "dance-secrethandshake",
            "235": "emote-surf",
            "237": "emote-stunned",
            "239": "dance-karate",
            "247": "emote-attention",
            "258": "dance-shuffle",
            "262": "emote-teleporting",
            "272": "emote-gravity",
            "281": "emote-cartwheel",
            "287": "dance-dontloveyou",
            "292": "emote-shrink",
            "295": "dance-russian",
            "296": "emote-howl2",
            "302": "emote-armcannon",
            "303": "dance-twerk",
            "304": "dance-yap",
            "306": "dance-freshstep"
        }

    async def loop_user_emote(self, user_id: str, emote_id: str):
        try:
            while True:
                # Sleep first since the initial emote is triggered in on_chat
                await asyncio.sleep(9)
                await self.highrise.send_emote(emote_id, user_id)
        except asyncio.CancelledError:
            pass
        except ResponseError:
            pass

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print("Bot is alive and in the room!")
        stand_spot = Position(x=15.5, y=0.0, z=5.5100002288818, facing='FrontRight')
        try:
            await self.highrise.teleport(session_metadata.user_id, stand_spot)
        except Exception:
            pass

    async def on_user_join(self, user: User, position: Position) -> None:
        await self.highrise.chat(f"Welcome, {user.username} to Cheap Diamond Grabs and Chat! Feel free to look around and send tips. 🥰✨! Check bio for commands.")

    async def on_user_leave(self, user: User) -> None:
        if user.id in self.user_dance_tasks:
            self.user_dance_tasks[user.id].cancel()
            del self.user_dance_tasks[user.id]

    async def on_chat(self, user: User, message: str) -> None:
        text = message.lower().strip()

        # 1. Stop command for the player
        if text == "stop":
            if user.id in self.user_dance_tasks:
                self.user_dance_tasks[user.id].cancel()
                del self.user_dance_tasks[user.id]
                await self.highrise.chat(f"Stopped dancing for @{user.username}!")
            return

        # 2. Player types a number to dance continuously
        if text in self.emote_dict:
            emote_id = self.emote_dict[text]
            
            # Test it first to catch errors and send the chat message
            try:
                await self.highrise.send_emote(emote_id, user.id)
            except ResponseError:
                await self.highrise.chat(f"Sorry @{user.username}, that emote cannot be played right now!")
                return
                
            # If successful, cancel old loop and start a new one
            if user.id in self.user_dance_tasks:
                self.user_dance_tasks[user.id].cancel()
            
            task = asyncio.create_task(self.loop_user_emote(user.id, emote_id))
            self.user_dance_tasks[user.id] = task
            return

        # 3. Player types "bot <number>" to make the bot dance
        if text.startswith("bot ") and text.replace("bot ", "").strip() in self.emote_dict:
            num = text.replace("bot ", "").strip()
            emote_id = self.emote_dict[num]
            try:
                await self.highrise.send_emote(emote_id)
            except ResponseError:
                await self.highrise.chat("I can't perform that emote!")
            return

        # 4. Bot continuous dancing loop
        if text == "!party":
            if self.is_dancing:
                await self.highrise.chat("I'm already dancing!")
                return
            self.is_dancing = True
            await self.highrise.chat("Let's dance!")
            while self.is_dancing:
                random_emote = random.choice(list(self.emote_dict.values()))
                try:
                    await self.highrise.send_emote(random_emote)
                except ResponseError:
                    pass
                await asyncio.sleep(10)

        elif text == "!stopbot":
            self.is_dancing = False
            await self.highrise.chat("Taking a break!")

        # 5. Outfit setter
        elif text == "!dressup":
            new_outfit = [
                Item(type='clothing', amount=1, id='body-flesh', account_bound=False, active_palette=28),
                Item(type='clothing', amount=1, id='nose-n_01_b', account_bound=False, active_palette=0),
                Item(type='clothing', amount=1, id='earrings-n_room12019goldhoops', account_bound=False, active_palette=0),
                Item(type='clothing', amount=1, id='shirt-n_registrationavatars2023furryshirt', account_bound=False, active_palette=0),
                Item(type='clothing', amount=1, id='skirt-n_septskypass2021skort', account_bound=False, active_palette=0),
                Item(type='clothing', amount=1, id='shoes-n_registrationavatars2023gothgirlshoes', account_bound=False, active_palette=0),
                Item(type='clothing', amount=1, id='hair_front-n_basic2018coilysidepart', account_bound=False, active_palette=17),
                Item(type='clothing', amount=1, id='eye-n_salonshop2018instagrameyes', account_bound=False, active_palette=24),
                Item(type='clothing', amount=1, id='eyebrow-n_basic2018newbrows16', account_bound=False, active_palette=0),
                Item(type='clothing', amount=1, id='mouth-n_registrationavatars2023pinkmouth', account_bound=False, active_palette=18),
                Item(type='clothing', amount=1, id='freckle-n_basic2018freckle22', account_bound=False, active_palette=0),
                Item(type='clothing', amount=1, id='freckle-n_basic2018freckle32', account_bound=False, active_palette=0),
                Item(type='clothing', amount=1, id='freckle-n_registrationavatars2023contour', account_bound=False, active_palette=0),
                Item(type='clothing', amount=1, id='freckle-n_freckle01', account_bound=False, active_palette=0),
                Item(type='clothing', amount=1, id='freckle-n_friendlymonstersmarchskypass2022friendlyblush', account_bound=False, active_palette=0),
                Item(type='clothing', amount=1, id='freckle-n_basic2018freckle39', account_bound=False, active_palette=0),
                Item(type='clothing', amount=1, id='glasses-n_room32019smallshades', account_bound=False, active_palette=0),
                Item(type='clothing', amount=1, id='hair_back-n_basic2018loosecoilymedium', account_bound=False, active_palette=17),
            ]
            try:
                await self.highrise.set_outfit(new_outfit)
                await self.highrise.chat("Outfit updated!")
            except ResponseError:
                await self.highrise.chat("I don't own all those items!")

        # 6. Check outfit code
        elif text == "!checkoutfit":
            user_outfit = await self.highrise.get_user_outfit(user.id)
            print("\n--- COPY THE CODE BELOW ---")
            for item in user_outfit.outfit:
                print(f"Item(type='{item.type}', amount=1, id='{item.id}', account_bound=False, active_palette={item.active_palette}),")
            print("---------------------------\n")
            await self.highrise.chat("Check your VS Code terminal for the outfit code!")

        # 7. Check floor coordinates
        elif text == "!pos":
            room_users = await self.highrise.get_room_users()
            for r_user, r_pos in room_users.content:
                if r_user.id == user.id and isinstance(r_pos, Position):
                    print(f"\nPosition(x={r_pos.x}, y={r_pos.y}, z={r_pos.z}, facing='{r_pos.facing}')\n")
                    await self.highrise.chat(f"Coords: x={r_pos.x:.1f}, y={r_pos.y:.1f}, z={r_pos.z:.1f}")
        # 8. Send emote list
        elif text == "!emotelist":
            await self.highrise.chat("Emotes 1/3: 18 (Attentive), 25 (Kiss), 62 (Astronaut), 98 (Float), 124 (Propose), 125 (Aerobics), 150 (Handstand)")
            await self.highrise.chat("Emotes 2/3: 164 (Cute), 168 (Howl), 176 (Shy), 179 (Launch), 186 (Fruity), 194 (Icecream), 196 (Curtsy), 201 (Roll)")
            await self.highrise.chat("Emotes 3/3: 226 (Charge), 247 (Attention), 262 (Teleport), 272 (Gravity), 292 (Shrink), 295 (Russian)")