from asyncio import get_event_loop
from typing import TYPE_CHECKING, Any, Callable, Coroutine, TypeVar

from pytecord import utils
from pytecord.enums import InteractionCallbackType, InteractionType, Permissions
from pytecord.route import Route
from pytecord.ui import Modal


if TYPE_CHECKING:
    from pytecord.annotations import Strable, Subclass
    from aiohttp import ClientSession

__all__ = (
    'Context',
    'Modal',
)

class Command:
    def __init__(self, data: dict) -> None:
        self.data = data
    def __getitem__(self, key: str):
        return self.data.get(key, None)
    def eval(self) -> dict:
        return self.data

class ContextMenu:
    def __init__(self, data: dict) -> None:
        self.data = data
    def __getitem__(self, key: str):
        return self.data.get(key, None)
    def eval(self) -> dict:
        return self.data

CT = TypeVar('CT', Command, ContextMenu)
MT = TypeVar('MT', bound=Modal)

class AppClient:
    def __init__(self) -> None:
        self.commands = []
        self.callbacks = {1: {}, 2: {}, 3: {}}
        self.component_callbacks = {'modals': {}}

    def add_command(self, command: CT, callback: Callable[..., Coroutine[Any, Any, Any]]) -> CT:
        self.commands.append(command)
        self.callbacks[command['type']].setdefault(command['name'], callback)
        return command

    def add_modal(self, modal: MT) -> MT:
        self.component_callbacks['modals'].setdefault(modal.custom_id, modal.submit)
        return modal

    async def invoke_command(self, name: str, type: int, *args, **kwrgs):
        await self.callbacks[type][name](*args, **kwrgs)

    async def invoke_modal_submit(self, custom_id: str, *args, **kwargs):
        await self.component_callbacks['modals'][custom_id](*args, **kwargs)

class _Interaction:
    def __init__(self, data: dict, token: str, session: 'ClientSession') -> None:
        self.token = data.get('token')
        self.id = data.get('id')
        self.type = data.get('type')
        self.application_id = data.get('application_id')

        self._token = token
        self._session = session

    async def respond(self, payload: dict):
        route = Route(
            '/interactions/%s/%s/callback', self.id, self.token,
            method='POST',
            token=self._token,
            payload=payload
        )
        j, _ = await route.async_request(self._session, get_event_loop())
        return j


class Context:
    def __init__(self, data: dict, token: str, session: 'ClientSession', hook) -> None:
        self._token = token
        self.interaction = _Interaction(data, token, session)
        self._session = session
        self._hook = hook

        self.command = Command(data['data'])

    async def send_message(
            self,
            *strings: list['Strable'],
            sep: str = ' ',
            tts: bool = False,
            ephemeral: bool = False
        ):
        await self.interaction.respond({
            'type': InteractionCallbackType.channel_message_with_source,
            'data': utils.message_payload(
                *strings,
                sep=sep,
                ephemeral=ephemeral,
                tts=tts
            )
        })

    async def edit_message(
            self,
            *strings: list['Strable'],
            sep: str = ' ',
            tts: bool = False,
            ephemeral: bool = False
        ):
        await self.interaction.respond({
            'type': InteractionCallbackType.update_message,
            'data': utils.message_payload(
                *strings,
                sep=sep,
                ephemeral=ephemeral,
                tts=tts
            )
        })

    async def send_modal(self, modal: 'Subclass[Modal]'):
        if self.interaction.type in [
            InteractionType.ping,
            InteractionType.modal_submit
        ]:
            return # not available in discord API
        await self.interaction.respond({
            'type': InteractionCallbackType.modal,
            'data': modal.eval()
        })
        self._hook._app_client.add_modal(modal)

def describe(**options):
    def wrapper(func):
        try:
            return options, func[1], 'describe'
        except TypeError:
            return options, func, 'describe'
    return wrapper

def perms(**permissions: dict[str, bool]):
    def wrapper(func):
        result = 0
        
        # permission_dict = {
        #     'create_instant_invite': Permissions.create_instant_invite,
        #     'kick_members': Permissions.kick_members,
        #     'ban_members': Permissions.ban_members,
        #     'administrator': Permissions.administrator,
        #     'manage_channels': Permissions.manage_channels,
        #     'manage_guild': Permissions.manage_guild,
        #     'add_reactions': Permissions.add_reactions,
        #     'view_audit_log': Permissions.view_audit_log,
        #     'priority_speaker': Permissions.priority_speaker,
        #     'stream': Permissions.stream,
        #     'view_channel': Permissions.view_channel,
        #     'send_messages':
        #     'send_tts_messages':
        #     'manage_messages':
        #     'embed_links':
        #     'attach_files':
        #     'read_message_history':
        #     'mention_everyone':
        #     'use_external_emojis':
        #     'view_guild_insights':
        #     'connect':
        #     'speak':
        #     'mute_members':
        #     'deafen_members':
        #     'move_members':
        #     'use_vad':
        #     'change_nickname':
        #     'manage_nicknames':
        #     'manage_roles':
        #     'manage_webhooks':
        #     'manage_emojis_and_stickers':
        #     'use_application_commands':
        #     'request_to_speak':
        #     'manage_events':
        #     'manage_threads':
        #     'create_public_threads':
        #     'create_private_threads':
        #     'use_external_stickers':
        #     'send_messages_in_threads':
        #     'use_embedded_activities':
        #     'moderate_members':
        # }
        
        json_dict = {'default_member_permissions': result}
        try:
            return result, func[1], ''
        except TypeError:
            return result, func, ''
    return wrapper
