import json
import requests
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model import Response

# ChatPDF API Key (Replace with your actual key)
CHATPDF_API_KEY = "your_chatpdf_api_key"
CHATPDF_ENDPOINT = "https://api.chatpdf.com/v1/"  # Example endpoint

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speech_text = "Welcome to ChatPDF! You can ask me to summarize or analyze a PDF."
        return handler_input.response_builder.speak(speech_text).set_should_end_session(False).response

class SummarizePDFIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("SummarizePDFIntent")(handler_input)

    def handle(self, handler_input):
        pdf_id = "your_pdf_id"  # You need to retrieve this dynamically in a real scenario
        response = requests.post(
            f"{CHATPDF_ENDPOINT}/summarize",
            headers={"Authorization": f"Bearer {CHATPDF_API_KEY}"},
            json={"pdf_id": pdf_id}
        )
        
        if response.status_code == 200:
            summary = response.json().get("summary", "I couldn't fetch the summary.")
        else:
            summary = "There was an issue retrieving the PDF summary."
        
        return handler_input.response_builder.speak(summary).set_should_end_session(True).response

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "You can ask me to summarize a PDF or analyze its content. How can I help?"
        return handler_input.response_builder.speak(speech_text).set_should_end_session(False).response

class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.speak("Goodbye!").set_should_end_session(True).response

sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(SummarizePDFIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())

lambda_handler = sb.lambda_handler()
