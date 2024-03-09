class StringConverter:
    @staticmethod
    def string_to_bool(input: str) -> bool:
        if input in ('True', 'true', 'TRUE'):
            return True
        return False
 