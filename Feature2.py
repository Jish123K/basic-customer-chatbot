# Import the knowledge base library

from rasa.shared.nlu.training_data.schemas.kb import KnowledgeBase

# Define a function to get the knowledge base response for an inquiry

def get_knowledge_base_response(inquiry_text):

    kb = KnowledgeBase()

    response = kb.query(inquiry_text)

    return response

# Update the `handle_inquiry()` function to use the `get_knowledge_base_response()` function

def handle_inquiry(inquiry):

    # Get the customer ID

    customer_id = inquiry["customer_id"]

    # Get the inquiry text

    inquiry_text = inquiry["text"]

    # Classify the inquiry

    classification = model.predict(inquiry_text)[0]

    # Get the response for the inquiry

    response = get_response(

        config["responses"]["{}.json".format(classification)],

        method="GET",

    )

    # Get the sentiment of the inquiry

    sentiment = get_sentiment(inquiry_text)

    # If the sentiment is negative, escalate the issue to a human representative

    if sentiment < 0:

        send_message(customer_id, "Your inquiry has been escalated to a human representative.")

        return

    # Get the knowledge base response for the inquiry

    kb_response = get_knowledge_base_response(inquiry_text)

    # If the knowledge base response is not empty, use it

    if kb_response:

        send_message(customer_id, kb_response["message"])

        return

    # Send the response to the customer

    send_message(customer_id, response["message"])

    # Log the inquiry
    logger.info("Inquiry handled: {}".format(inquiry_text))

# Update the `listen_for_inquiries()` function to use the `get_knowledge_base_response()` function

def listen_for_inquiries():

    # Get the list of channels

    channels = config["channels"]

    # Loop over the channels

    for channel in channels:

        # Get the channel URL

        channel_url = config["channels"][channel]["url"]

        # Get the channel headers

        channel_headers = config["channels"][channel]["headers"]

        # Get the channel data

        channel_data = config["channels"][channel]["data"]

        # Listen for new inquiries on the channel

        while True:

            # Get the new inquiries

            new_inquiries = get_response(channel_url, method="GET", headers=channel_headers, data=channel_data)

            # Loop over the new inquiries

            for inquiry in new_inquiries:

                # Handle the inquiry

                handle_inquiry(inquiry)

            # Sleep for a few seconds

            time.sleep(config["sleep_interval"])

# Start listening for new inquiries

if __name__ == "__main__":

    # Start a new thread to listen for new inquiries

    thread = threading.Thread(target=listen_for_inquiries)

    thread.start()

    # Keep the main thread running

    while True:

        time.sleep(1)
