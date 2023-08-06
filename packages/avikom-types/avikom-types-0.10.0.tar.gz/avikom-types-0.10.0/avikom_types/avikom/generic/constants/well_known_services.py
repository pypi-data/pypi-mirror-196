class WellKnownServices:
    """ Well-known service topics. """

    SERVICE_SPEECH_RECOGNITION = "ServiceSpeechRecognition"
    """ Provides speech recognition input """

    SERVICE_OCR = "ServiceOcr"
    """ Provides character-/text-recognition """

    SERVICE_NUMBER_INPUT = "ServiceNumberInput"
    """ Offers number input to users; may be implemented via different methods (e.g. speech or keyboard) """

    SERVICE_TEXT_INPUT = "ServiceTextInput"
    """ Offers text input to users """

    SERVICE_LOCATION_EVENT = "ServiceLocationEvent"
    """ Triggers an event when a location has been reached (X)OR left """

