import os
from datetime import datetime
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions
import json
import logging
import openai


class _SupabaseClient:
    def __init__(self):
        url: str = os.environ.get(
            "INSTANCE_URL", default="https://qdgodxkfxzzmzwfliahh.supabase.co"
        )
        key: str = os.environ.get(
            "INSTANCE_ANON_KEY",
            default="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFkZ29keGtmeHp6bXp3ZmxpYWhoIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODg0OTc0NzcsImV4cCI6MjAwNDA3MzQ3N30.4bgCdg77wwOJ9w1hOtCD-z0gBVGv8X_kIxBCr5KDCuA",
        )

        # API key format is organization:api_key
        talc_api_key: str = os.environ.get("TALC_API_KEY", default=":")

        if talc_api_key == "":
            logging.warning(
                "TALC_API_KEY environment variable not set. Logging disabled."
            )
            self.__initialized = False
            return

        organization, api_key = talc_api_key.split(":")
        self.__organization: str = organization

        options = ClientOptions(headers={"talckey": api_key})
        self.supabase: Client = create_client(url, key, options=options)
        self.__initialized = True

    def createSession(self):
        if not self.__initialized:
            return None
        response = (
            self.supabase.table("sessions")
            .insert(
                {
                    "organization": self.__organization,
                }
            )
            .execute()
        )
        return response.data[0]["id"]

    def __createInput(self, sessionId, generationId, role, content, index):
        response = (
            self.supabase.table("inputs")
            .insert(
                {
                    "session": sessionId,
                    "generation": generationId,
                    "role": role,
                    "content": content,
                    "index": index,
                }
            )
            .execute()
        )
        return response.data[0]["id"]

    def __createGeneration(
        self,
        sessionId,
        content,
        function_calls,
        agent,
        generated_at,
        functions_available,
        parameters,
    ):
        response = (
            self.supabase.table("generations")
            .insert(
                {
                    "session": sessionId,
                    "content": content,
                    "functions_called": function_calls,
                    "agent": agent,
                    "generated_at": generated_at,
                    "functions_available": functions_available,
                    "parameters": parameters,
                }
            )
            .execute()
        )
        return response.data[0]["id"]

    def __historyArrayToInputs(self, history, generationId, sessionId):
        for index, chat in enumerate(history):
            self.__createInput(
                sessionId,
                generationId,
                chat["role"],
                chat["content"],
                # Index is reversed because we want the most recent message to have the lowest index
                len(history) - index,
            )

    def log(
        self,
        sessionId,
        history,
        text_content,
        function_calls,
        agent,
        functions_available,
        parameters,
    ):
        generated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        generationId = self.__createGeneration(
            sessionId,
            text_content,
            function_calls,
            agent,
            generated_at,
            functions_available,
            parameters,
        )
        self.__historyArrayToInputs(history, generationId, sessionId)


def createSession():
    response = client.createSession()
    return response


def init():
    global client
    client = _SupabaseClient()


class __alternateCompletion(openai.ChatCompletion):
    @classmethod
    def create(cls, *args, **kwargs):
        # Pop arguments that are not supported by the original create method
        agent = kwargs.pop("agent", "Default")
        session = kwargs.pop("session", None)
        stream = "stream" in kwargs and kwargs["stream"]

        functions_available, parameters = cls.__getFunctionsAndParameters(**kwargs)

        result = super().create(*args, **kwargs)

        text_content, function_calls = cls.__getContent(result.choices)

        # Handle case where we have received the full response at once.
        if not stream:
            try:
                if session and agent:
                    client.log(
                        session,
                        kwargs["messages"],
                        text_content,
                        function_calls,
                        agent,
                        functions_available,
                        parameters,
                    )
            except Exception as e:
                logging.warning("Error logging to talc: ", e)

            return result
        # Handle stream case
        else:
            logging.warning("Talc: Stream case not implemented yet.")

            agent = kwargs.pop("agent", "Default")
            session = kwargs.pop("session", None)

            return super().create(*args, **kwargs)

    @classmethod
    async def acreate(cls, *args, **kwargs):
        # Pop arguments that are not supported by the original create method
        agent = kwargs.pop("agent", None)
        session = kwargs.pop("session", None)

        result = await super().acreate(*args, **kwargs)

        return result

    @classmethod
    def __getContent(cls, choices):
        text_content = []
        function_calls = []

        for choice in choices:
            if "function_call" in choice.message:
                function_calls.append(choice.message.function_call)
            else:
                function_calls.append(None)

            if "content" in choice.message:
                text_content.append(choice.message.content)
            else:
                text_content.append(None)

        return text_content, function_calls

    @classmethod
    def __getFunctionsAndParameters(cls, **kwargs):
        functions = None
        if "functions" in kwargs:
            functions = kwargs["functions"]

        ignored_params = ["functions", "messages"]

        parameters = {
            key: val for (key, val) in kwargs.items() if key not in ignored_params
        }

        return json.dumps(functions), json.dumps(parameters)


openai.ChatCompletion = __alternateCompletion
