from websocket_chat.application.use_case import IUseCase
from websocket_chat.domain.entities.chat import ReadMessageDTO, ReadMessageResultDTO


class ReadMessageUseCase(IUseCase[ReadMessageDTO, ReadMessageResultDTO]):
    async def execute(self, input_dto: ReadMessageDTO) -> ReadMessageResultDTO:
        raise NotImplementedError
