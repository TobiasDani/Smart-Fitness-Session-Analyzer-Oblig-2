class Observation:
    def __init__(self, timestamp, heart_rate, skin_response, temperature, activity_level, signal_quality):
        self.timestamp = timestamp
        self.heart_rate = heart_rate
        self.skin_response = skin_response
        self.temperature = temperature
        self.activity_level = activity_level
        self.signal_quality = signal_quality


    def is_valid(self):
        if not isinstance(self.timestamp, (int, float)) or self.timestamp < 0:
            return False
        if self.heart_rate is None or not isinstance(self.heart_rate, (int, float)) or not 35 <= self.heart_rate <= 205:
            return False
        if self.skin_response is None or not isinstance(self.skin_response, (int, float)) or self.skin_response < 0:
            return False
        if self.temperature is None or not isinstance(self.temperature, (int, float)) or not 25 <= self.temperature <= 42:
            return False
        if self.activity_level is None or not isinstance(self.activity_level, (int, float)) or not 0 <= self.activity_level <= 1:
            return False
        if self.signal_quality is None or not isinstance(self.signal_quality, (int, float)) or not 0 <= self.signal_quality <= 1:
            return False

        return True
    
