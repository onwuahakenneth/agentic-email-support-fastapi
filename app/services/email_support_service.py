import uuid
import asyncio
from src.app.models import ChatRequest
from src.orchestrator.agent import AgentBuilder
from langchain_core.runnables import RunnableConfig


class EmailSupportService:
    """Email support agent with human-in-the-loop"""

    def __init__(self) -> None:
        self.builder = AgentBuilder()
        self.agent = self.builder.createAgent()
        self.config: RunnableConfig = {
            "configurable": {"thread_id": str(uuid.uuid4())}}

    async def process_chat(self, request_data: ChatRequest):
        """process user's chat message/query"""

        
        response = self.agent.invoke(
            {
                **request_data.model_dump(),
                "email_id": str(uuid.uuid4()),
                "messages": []
            }, # type: ignore
            config=self.config
        ) 

        response_content = response.get("draft_response", "Not draft yet...")

        return response_content


# single instance
email_support_service = EmailSupportService()


async def main():
    response = await email_support_service.process_chat(
        request_data=ChatRequest(
            email_content="How do I reset my password?",
            email_sender="example@customer.com",
        )
    )

    print(response)


if __name__ == "__main__":
    asyncio.run(main())
