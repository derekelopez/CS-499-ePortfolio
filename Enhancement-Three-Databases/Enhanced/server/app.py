"""
Flask API for the enhanced smart thermostat.

This module receives telemetry from the Raspberry Pi thermostat.
"""

from datetime import datetime

from flask import Flask, jsonify, request

from .database import ThermostatDatabase

from .validation import validate_reading

app = Flask(__name__)

database = ThermostatDatabase()


@app.get("/api/health")
def health_check():
    """
    Return the API health status.
    """

    return jsonify(
        {
            "status": "ok",
            "service": "smart-thermostat-api",
        }
    )


@app.post("/api/readings")
def receive_reading():
    """
    Receive one thermostat telemetry reading.
    """

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Request body must contain valid JSON."}), 400

    errors = validate_reading(data)

    if errors:
        return (
            jsonify(
                {
                    "error": "Telemetry validation failed.",
                    "details": errors,
                }
            ),
            400,
        )

    reading_id = database.insert_reading(data)

    if reading_id is None:
        return jsonify({"error": "Unable to store telemetry reading."}), 503

    return (
        jsonify(
            {
                "message": "Telemetry stored successfully.",
                "id": reading_id,
            }
        ),
        201,
    )


@app.get("/api/readings/recent")
def get_recent_readings():
    """
    Return the most recent thermostat readings.
    """

    try:
        limit = int(request.args.get("limit", 20))

    except ValueError:
        return jsonify({"error": "limit must be an integer."}), 400

    if limit < 1 or limit > 100:
        return jsonify({"error": "limit must be between 1 and 100."}), 400

    readings = database.get_recent_readings(limit)

    if readings is None:
        return jsonify({"error": "Unable to retrieve thermostat readings."}), 503

    return (
        jsonify(
            {
                "count": len(readings),
                "readings": readings,
            }
        ),
        200,
    )


@app.get("/api/readings/range")
def get_readings_by_date_range():
    """
    Return thermostat readings within a requested timestamp range.
    """

    start_time = request.args.get("start")
    end_time = request.args.get("end")

    if not start_time or not end_time:
        return jsonify({"error": "Both start and end timestamps are required."}), 400

    try:
        start_datetime = datetime.fromisoformat(start_time)
        end_datetime = datetime.fromisoformat(end_time)

    except ValueError:
        return jsonify({"error": "start and end must be valid ISO timestamps."}), 400

    if start_datetime > end_datetime:
        return jsonify({"error": "start timestamp must be before end timestamp."}), 400

    readings = database.get_readings_by_date_range(
        start_time,
        end_time,
    )

    if readings is None:
        return jsonify({"error": "Unable to retrieve thermostat readings."}), 503

    return (
        jsonify(
            {
                "count": len(readings),
                "readings": readings,
            }
        ),
        200,
    )


@app.get("/api/readings/statistics")
def get_reading_statistics():
    """
    Return aggregate statistics for stored thermostat readings.

    Optional start and end timestamps limit the statistics
    to a specific date range.
    """

    start_time = request.args.get("start")
    end_time = request.args.get("end")

    if (start_time and not end_time) or (end_time and not start_time):
        return jsonify({"error": "Both start and end timestamps are required."}), 400

    if start_time and end_time:
        try:
            start_datetime = datetime.fromisoformat(start_time)
            end_datetime = datetime.fromisoformat(end_time)

        except ValueError:
            return (
                jsonify({"error": "start and end must be valid ISO timestamps."}),
                400,
            )

        if start_datetime > end_datetime:
            return (
                jsonify({"error": "start timestamp must be before end timestamp."}),
                400,
            )

    statistics = database.get_statistics(
        start_time,
        end_time,
    )

    if statistics is None:
        return jsonify({"error": "Unable to calculate thermostat statistics."}), 503

    return jsonify(statistics), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
