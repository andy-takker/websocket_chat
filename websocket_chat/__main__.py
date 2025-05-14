import os

import uvicorn

from websocket_chat.presentors.web.app_factory import get_application

if __name__ == "__main__":
    port = int(os.getenv("APP_HTTP_PORT", 8080))
    uvicorn.run(
        get_application,
        host="0.0.0.0",
        port=port,
        forwarded_allow_ips="*",
        factory=True,
    )
