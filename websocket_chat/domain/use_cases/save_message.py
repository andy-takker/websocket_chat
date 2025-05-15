from websocket_chat.application.use_case import IUseCase
from websocket_chat.domain.entities.chat import Message, SaveMessageDTO


class SaveMessageUseCase(IUseCase[SaveMessageDTO, Message]):
    async def execute(self, input_dto: SaveMessageDTO) -> Message:
        raise NotImplementedError
