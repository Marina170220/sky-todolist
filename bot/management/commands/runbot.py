import os
from enum import Enum, unique, auto
from typing import Optional

from django.core.management import BaseCommand
from marshmallow_dataclass import dataclass

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models import Goal, Category
from todolist import settings


@dataclass
class NewGoal:
    cat_id: Optional[int] = None
    goal_title: Optional[str] = None

    def complete(self) -> bool:
        return None not in {self.cat_id, self.goal_title}

@unique
class StateEnum(Enum):
    CREATE_CATEGORY_STATE = auto()
    CHOSEN_CATEGORY = auto()
    VIEW_GOALS_LIST = auto()


@dataclass
class FSMData:
    state: StateEnum
    goal: NewGoal


FSM_STATES: dict[int, FSMData] = dict()


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.BOT_TOKEN)

    @staticmethod
    def _generate_verification_code() -> str:
        return os.urandom(12).hex()

    def handle_user_without_verification(self, msg: Message, tg_user: TgUser):
        code: str = self._generate_verification_code()
        tg_user.verification_code = code
        tg_user.save(update_fields=['verification_code'])

        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f"[verification code] {code}"
        )

    def handle_goals_list(self, msg: Message, tg_user: TgUser):
        goals_list: list[str] = [f'#{goal.id} {goal.title}' for goal in Goal.objects.filter(user_id=tg_user.user_id)]
        self.tg_client.send_message(msg.chat.id, "\n".join(goals_list) or "[Goals list is empty]")

    def handle_categories_list(self, msg: Message, tg_user: TgUser):
        cats_list: list[str] = [f'#{cat.id} {cat.title}' for cat in Category.objects.filter(
            board__participants__user_id=tg_user.user_id,
            is_deleted=False)
                                ]
        if cats_list:
            self.tg_client.send_message(msg.chat.id, "Select category\n{}".format("\n".join(cats_list)))
        else:
            self.tg_client.send_message(msg.chat.id, "Categories not found")

    def handle_save_category(self, msg: Message, tg_user: TgUser):
        if msg.text.isdigit():
            cat_id = int(msg.text)
            if Category.objects.filter(board__participants__user_id=tg_user.user_id,
                                       is_deleted=False,
                                       id=cat_id).count():
                FSM_STATES[tg_user.chat_id].goal.cat_id = cat_id
                self.tg_client.send_message(msg.chat.id, "[Set title]")
                FSM_STATES[tg_user.chat_id].state = StateEnum.CHOSEN_CATEGORY
                return

        self.tg_client.send_message(msg.chat.id, "[Invalid category id]")

    def handle_save_new_goal(self, msg: Message, tg_user: TgUser):
        goal: NewGoal = FSM_STATES[tg_user.chat_id].goal
        goal.goal_title = msg.text
        if goal.complete():
            Goal.objects.create(
                title=goal.goal_title,
                category_id=goal.cat_id,
                user_id=tg_user.user_id
            )
            self.tg_client.send_message(msg.chat.id, "[New goal created]")
        else:
            self.tg_client.send_message(msg.chat.id, "[Something went wrong]")

        FSM_STATES.pop(tg_user.chat_id, None)

    def handle_verified_user(self, msg: Message, tg_user: TgUser):
        if not msg.text:
            return
        if "goals" in msg.text:
            self.handle_goals_list(msg=msg, tg_user=tg_user)
            FSM_STATES[tg_user.chat_id] = FSMData(state=StateEnum.VIEW_GOALS_LIST, goal=None)

        elif "create" in msg.text:
            self.handle_categories_list(msg=msg, tg_user=tg_user)
            FSM_STATES[tg_user.chat_id] = FSMData(state=StateEnum.CREATE_CATEGORY_STATE, goal=NewGoal())

        elif "cancel" in msg.text and tg_user.chat_id in FSM_STATES:
            FSM_STATES.pop(tg_user.chat_id)
            self.tg_client.send_message(msg.chat.id, "[Action cancelled]")

        elif tg_user.chat_id in FSM_STATES:
            state: StateEnum = FSM_STATES[tg_user.chat_id].state

            if state == StateEnum.CREATE_CATEGORY_STATE:
                self.handle_save_category(msg=msg, tg_user=tg_user)

            elif state == StateEnum.CHOSEN_CATEGORY:
                self.handle_save_new_goal(msg=msg, tg_user=tg_user)

        else:
            self.tg_client.send_message(msg.chat.id, "[Unknown command]")

        print(FSM_STATES)

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(
            chat_id=msg.chat.id,
            defaults={
                "username": msg.from_.username,
            },
        )
        if created:
            self.tg_client.send_message(msg.chat.id, "[Hello]")

        if tg_user.user:
            self.handle_verified_user(msg, tg_user)

        else:
            self.handle_user_without_verification(msg, tg_user)

    def handle(self, *args, **options):
        offset = 0

        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(msg=item.message)
