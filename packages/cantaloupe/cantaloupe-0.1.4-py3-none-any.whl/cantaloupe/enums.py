import enum


class Action(str, enum.Enum):
    """
    An enum containing all fields
    currently supported by the DSL.
    """

    GOTO = "goto"
    CODE = "code"
    TYPE = "type"
    CLEAR = "clear"
    PRESS = "press"
    FOCUS = "focus"
    CLICK = "click"
    HOVER = "hover"
    RELOAD = "reload"
    SELECT = "select"
    IMPORT = "import"
    GO_BACK = "go_back"
    GO_FORWARD = "go_forward"
    WAIT_FOR_URL = "wait_for_url"
    TAKE_SCREENSHOT = "take_screenshot"
    WAIT_FOR_ELEMENT = "wait_for_element"
    WAIT_FOR_NAVIGATION = "wait_for_navigation"


class Browser(str, enum.Enum):
    """Playwright supported browsers"""

    EDGE = "edge"
    CHROME = "chrome"
    SAFARI = "webkit"
    WEBKIT = "webkit"
    FIREFOX = "firefox"
    CHROMIUM = "chromium"


class TraceVideoOpts(str, enum.Enum):
    ON = "on"
    OFF = "off"
    FIRST_TRY = "on-first-retry"
    ON_FAILURE = "retain-on-failure"


class ScreenshotOpts(str, enum.Enum):
    ON = "on"
    OFF = "off"
    ON_FAILURE = "only-on-failure"
