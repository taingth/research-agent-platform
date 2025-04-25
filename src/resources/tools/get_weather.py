from loguru import logger


def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city (e.g., "New York", "London", "Tokyo").

    Returns:
        dict: A dictionary containing the weather information.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'report' key with weather details.
              If 'error', includes an 'error_message' key.
    """

    logger.info(f"---- Tool calling: get_weather called for city {city} ----")
    city_normalized = city.lower().strip().replace(" ", "_")

    # Simulate a weather report

    ## Mock weather data for simplicity
    weather_data = {
        "new_york": {
            "status": "success",
            "report": "The weather in New York is sunny with a temperature of 25°C.",
        },
        "london": {
            "status": "success",
            "report": "Cloudy with a chance of rain in London.",
        },
        "tokyo": {"status": "success", "report": "Rainy in Tokyo."},
        "paris": {"status": "success", "report": "Sunny in Paris."},
    }

    return weather_data.get(
        city_normalized, {"status": "error", "error_message": f"City {city} not found."}
    )
