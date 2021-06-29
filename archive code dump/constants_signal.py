class Signal(Enum):
    AI_CONVERT_CLOCK = 12484  #: 
    TEN_M_HZ_REF_CLOCK = 12536  #: 
    TWENTY_M_HZ_TIMEBASE_CLOCK = 12486  #: 
    SAMPLE_CLOCK = 12487  #: Timed Loop executes on each active edge of the Sample Clock.
    ADVANCE_TRIGGER = 12488  #: 
    REFERENCE_TRIGGER = 12490  #: 
    START_TRIGGER = 12491  #: 
    ADV_CMPLT_EVENT = 12492  #: 
    AI_HOLD_CMPLT_EVENT = 12493  #: 
    COUNTER_OUTPUT_EVENT = 12494  #: Timed Loop executes each time the Counter Output Event occurs.
    CHANGE_DETECTION_EVENT = 12511  #: Timed Loop executes each time the Change Detection Event occurs.
    WATCHDOG_TIMER_EXPIRED_EVENT = 12512  #: 
    SAMPLE_COMPLETE = 12530  #: Timed Loop executes each time the Sample Complete Event occurs.


