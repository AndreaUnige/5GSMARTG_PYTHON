class Const:

    X_AXIS = 'X_AXIS'
    Y_AXIS = 'Y_AXIS'
    Z_AXIS = 'Z_AXIS'

    SUBSCRIBE_TO_TOPIC_ALL = 0
    SUBSCRIBE_TO_TOPIC_HASH = 1
    SUBSCRIBE_TO_BOTH_TOPICS = 2

    # These will be overwritten by reading the file clients.txt
    broker = None
    root_topic_ALL = None
    root_topic_HASH = None
    username = None
    password = None
    clientIDs = None

    # Final list of topics to which subscribe.
    # This will be populated run-time based on the clientIDs in the 'clients.txt' file
    listOfTopicToSubscribeTo = []

    # Subscriber ID. Not so necessary, it could be put randomly
    subscriberID = '0x02'

    # ------------------ #
    # ---- ACC DATA ---- #
    # ------------------ #
    X_AXIS = "X_AXIS"
    Y_AXIS = "Y_AXIS"
    Z_AXIS = "Z_AXIS"

    SampleSeparator = ";"
    SingleValuesSeparator = ","

    # ---------------------------- #
    # --- WELCH PSD ESTIMATION --- #
    # ---------------------------- #
    WINDOW_LENGTH_IN_SEC = 5
    OVERLAP_PERCENTAGE = 85  # Percentage
    RUNNING_AVERAGE_IN_SAMPLES = 10

    # ----------------- #
    # --- PLOT DATA --- #
    # ----------------- #
    PLOT_PAUSE_SEC = 0.5
    SAMPLING_RATE = 100  # Hz
    MAX_SAMPLES_TO_VISUALIZE = 2 * WINDOW_LENGTH_IN_SEC * SAMPLING_RATE  # Show 2 windows

    # ----------------- #
    # ---- DEVICES ---- #
    # ----------------- #
    NODE_DSP = "DSP"
    NODE_LABJACK = "LJ"
