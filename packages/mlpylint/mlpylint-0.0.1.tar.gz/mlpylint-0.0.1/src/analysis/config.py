

class ColorConfig:
    _instance = None

    @staticmethod
    def get_instance(enable_color=False):
        if ColorConfig._instance is None:
            ColorConfig._instance = super(ColorConfig, ColorConfig).__new__(ColorConfig)
            ColorConfig._instance.enable_color = enable_color
        return ColorConfig._instance


