from datetime import datetime as dt


try:

    def get_current_year():
        return dt.now().year

except Exception as e:
    print(f"Error: {e}")

