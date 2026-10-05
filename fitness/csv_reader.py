import csv
import re
from pathlib import Path

from .exceptions import InvalidIdentifierError, InvalidRecordError
from .observation import Observation
from .participant import Participant
from .session import Session


def validate_participant_id(participant_id):
    if not re.fullmatch(r"P\d{3}", participant_id):
        raise InvalidIdentifierError(
            f"Invalid participant ID: {participant_id}"
        )


def validate_session_id(session_id):
    if not re.fullmatch(r"FIT-\d{4}-\d{3}", session_id):
        raise InvalidIdentifierError(
            f"Invalid session ID: {session_id}"
        )


def load_participants(file_path):
    file_path = Path(file_path)

    participants = {}
    rejected = []

    try:
        with open(file_path, "r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            for row_number, row in enumerate(reader, start=2):
                field = "row"

                try:
                    # Detect rows with too few or too many columns
                    if None in row or any(value is None for value in row.values()):
                        raise InvalidRecordError("Unexpected number of columns")

                    # Detect empty required fields
                    for name, value in row.items():
                        field = name
                        if value.strip() == "":
                            raise InvalidRecordError("Missing required field")

                    field = "participant_id"
                    participant_id = row["participant_id"]
                    validate_participant_id(participant_id)

                    field = "baseline_heart_rate"
                    heart_rate = int(row["baseline_heart_rate"])

                    field = "baseline_skin_response"
                    skin_response = float(row["baseline_skin_response"])

                    field = "baseline_temperature"
                    temperature = float(row["baseline_temperature"])

                    if not Participant.is_valid_baseline(
                        heart_rate,
                        skin_response,
                        temperature,
                    ):
                        raise InvalidRecordError("Invalid baseline values")

                    participant = Participant(
                        participant_id,
                        heart_rate,
                        skin_response,
                        temperature,
                        name=row["name"],
                    )

                    participants[participant_id] = participant

                except (
                    InvalidIdentifierError,
                    InvalidRecordError,
                    ValueError,
                    KeyError,
                ) as error:
                    rejected.append(
                        {
                            "filename": str(file_path),
                            "row_number": row_number,
                            "field": field,
                            "reason": str(error),
                        }
                    )

    except FileNotFoundError:
        rejected.append(
            {
                "filename": str(file_path),
                "row_number": None,
                "field": "file",
                "reason": "File not found",
            }
        )

    except PermissionError:
        rejected.append(
            {
                "filename": str(file_path),
                "row_number": None,
                "field": "file",
                "reason": "Permission denied",
            }
        )

    except csv.Error as error:
        rejected.append(
            {
                "filename": str(file_path),
                "row_number": None,
                "field": "file",
                "reason": f"CSV error: {error}",
            }
        )

    return participants, rejected


def load_sessions(file_path, participants):
    file_path = Path(file_path)

    sessions = {}
    rejected = []

    try:
        with open(file_path, "r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            for row_number, row in enumerate(reader, start=2):
                field = "row"

                try:
                    # Detect rows with too few or too many columns
                    if None in row or any(value is None for value in row.values()):
                        raise InvalidRecordError("Unexpected number of columns")

                    # Detect empty required fields
                    for name, value in row.items():
                        field = name
                        if value.strip() == "":
                            raise InvalidRecordError("Missing required field")

                    field = "session_id"
                    session_id = row["session_id"]
                    validate_session_id(session_id)

                    field = "participant_id"
                    participant_id = row["participant_id"]
                    validate_participant_id(participant_id)

                    if participant_id not in participants:
                        raise InvalidRecordError(
                            f"Unknown participant ID: {participant_id}"
                        )

                    field = "timestamp"
                    timestamp = int(row["timestamp"])
                    if timestamp < 0:
                        raise InvalidRecordError(
                            "Timestamp cannot be negative"
                        )

                    field = "heart_rate"
                    heart_rate = int(row["heart_rate"])
                    if not 35 <= heart_rate <= 205:
                        raise InvalidRecordError(
                            "Heart rate is outside accepted range"
                        )

                    field = "skin_response"
                    skin_response = float(row["skin_response"])
                    if skin_response < 0:
                        raise InvalidRecordError(
                            "Skin response cannot be negative"
                        )

                    field = "temperature"
                    temperature = float(row["temperature"])
                    if not 25 <= temperature <= 42:
                        raise InvalidRecordError(
                            "Temperature is outside accepted range"
                        )

                    field = "activity_level"
                    activity_level = float(row["activity_level"])
                    if not 0 <= activity_level <= 1:
                        raise InvalidRecordError(
                            "Activity level must be between 0 and 1"
                        )

                    field = "signal_quality"
                    signal_quality = float(row["signal_quality"])
                    if not 0 <= signal_quality <= 1:
                        raise InvalidRecordError(
                            "Signal quality must be between 0 and 1"
                        )

                    observation = Observation(
                        timestamp,
                        heart_rate,
                        skin_response,
                        temperature,
                        activity_level,
                        signal_quality,
                    )

                    if session_id not in sessions:
                        sessions[session_id] = Session(
                            participants[participant_id],
                            session_id,
                        )

                    sessions[session_id].add_single_observation(
                        observation
                    )

                except (
                    InvalidIdentifierError,
                    InvalidRecordError,
                    ValueError,
                    KeyError,
                ) as error:
                    rejected.append(
                        {
                            "filename": str(file_path),
                            "row_number": row_number,
                            "field": field,
                            "reason": str(error),
                        }
                    )

    except FileNotFoundError:
        rejected.append(
            {
                "filename": str(file_path),
                "row_number": None,
                "field": "file",
                "reason": "File not found",
            }
        )

    except PermissionError:
        rejected.append(
            {
                "filename": str(file_path),
                "row_number": None,
                "field": "file",
                "reason": "Permission denied",
            }
        )

    except csv.Error as error:
        rejected.append(
            {
                "filename": str(file_path),
                "row_number": None,
                "field": "file",
                "reason": f"CSV error: {error}",
            }
        )

    return sessions, rejected