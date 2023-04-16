# Import the sentiment analysis library

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Define a function to get the sentiment of an inquiry

def get_sentiment(inquiry_text):

    analyzer = SentimentIntensityAnalyzer()

    sentiment = analyzer.polarity_scores(inquiry_text)

    return sentiment["compound"]

# Update the `handle_inquiry()` function to use the `get_sentiment()` function

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

    # Send the response to the customer

    send_message(customer_id, response["message"])

    # Log the inquiry

    logger.info("Inquiry handled: {}".format(inquiry_text))

# Update the `listen_for_inquiries()` function to use the `get_sentiment()` function

def listen_for_inquiries():

    # Get the list of channels

    channels = config["channels"]

    # Loop over the channels

    for channel in channels:

        # Get the channel U
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
