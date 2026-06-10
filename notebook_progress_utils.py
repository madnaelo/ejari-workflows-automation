import csv
import json
import re
from datetime import datetime
from pathlib import Path


def count_progress_success_records(progress):
    count = 0
    if not isinstance(progress, dict):
        return count
    for emirates_data in progress.values():
        if not isinstance(emirates_data, dict):
            continue
        successes = emirates_data.get("ejari_creation_success")
        if isinstance(successes, dict):
            count += len(successes)
    return count


def infer_emirates_id_from_success_file(progress_path, record):
    for key in ("emirates_id", "owner_emirates_id", "OwnerEmiratesId", "OwnerEmiratesID", "EID"):
        value = record.get(key) if isinstance(record, dict) else None
        if value:
            return str(value)
    filename = Path(progress_path).name if progress_path is not None else ""
    match = re.search(r"(?:^|_)(\d{15})(?:_|$)", filename)
    if match:
        return match.group(1)
    return None


def looks_like_success_detail_record(data):
    if not isinstance(data, dict):
        return False
    status = str(data.get("status") or data.get("Status") or "").strip().lower()
    has_success_status = status == "success"
    has_property_identity = bool(data.get("property_id") or data.get("PropertyId") or data.get("property_row_value") or data.get("PropertyRowValue"))
    has_create_response = bool(data.get("api5_response") or data.get("create_response") or data.get("contract_number") or data.get("ContractNumber"))
    return has_success_status and has_property_identity and has_create_response


def wrap_success_detail_as_progress(data, progress_path):
    emirates_id = infer_emirates_id_from_success_file(progress_path, data)
    if not emirates_id:
        raise ValueError(
            "Single success JSON file does not contain an Emirates ID and it could not be inferred from the filename. "
            "Expected a filename like success_<emirates_id>_<property_id>_....json."
        )
    property_key = (
        data.get("property_row_value")
        or data.get("PropertyRowValue")
        or data.get("property_id")
        or data.get("PropertyId")
        or Path(progress_path).stem
    )
    return {
        str(emirates_id): {
            "ejari_creation_success": {
                str(property_key): data,
            },
            "ejari_creation_failure": {},
            "ejari_creation_curl_only": {},
        }
    }


def parse_progress_timestamp(value):
    if not value:
        return datetime.min
    text = str(value).strip().replace("T", " ")
    for date_format in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y%m%d_%H%M%S"):
        try:
            candidate = text[:26] if "%f" in date_format else text[:19]
            return datetime.strptime(candidate, date_format)
        except Exception:
            continue
    return datetime.min


def normalize_progress_path(path_text):
    text = str(path_text or "").strip().strip('"').strip("'")
    if not text:
        return None
    progress_path = Path(text).expanduser()
    if progress_path.is_dir():
        progress_path = progress_path / "progress.json"
    return progress_path


def parse_progress_file_paths(raw_paths):
    if isinstance(raw_paths, (list, tuple, set)):
        cleaned_paths = []
        seen = set()
        for path_text in raw_paths:
            progress_path = normalize_progress_path(path_text)
            if progress_path is None:
                continue
            marker = str(progress_path)
            if marker not in seen:
                seen.add(marker)
                cleaned_paths.append(progress_path)
        return cleaned_paths

    raw_paths = str(raw_paths or "").strip()
    if not raw_paths:
        return []

    separators_present = any(separator in raw_paths for separator in (",", ";", "\n"))
    if not separators_present:
        progress_path = normalize_progress_path(raw_paths)
        return [progress_path] if progress_path else []

    normalized = raw_paths.replace(";", ",").replace("\n", ",")
    parsed_paths = []
    try:
        for row in csv.reader([normalized], skipinitialspace=True):
            parsed_paths.extend(row)
    except Exception:
        parsed_paths = normalized.split(",")

    cleaned_paths = []
    seen = set()
    for path_text in parsed_paths:
        progress_path = normalize_progress_path(path_text)
        if progress_path is None:
            continue
        marker = str(progress_path)
        if marker not in seen:
            seen.add(marker)
            cleaned_paths.append(progress_path)
    return cleaned_paths


def load_progress_file(progress_path):
    progress_path = normalize_progress_path(progress_path)
    if progress_path is None:
        raise ValueError("No progress file path was provided.")
    if not progress_path.exists():
        raise FileNotFoundError(f"Progress file does not exist: {progress_path}")
    with progress_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("Progress file root must be a JSON object keyed by Emirates ID.")
    if count_progress_success_records(data) == 0 and looks_like_success_detail_record(data):
        data = wrap_success_detail_as_progress(data, progress_path)
    if count_progress_success_records(data) == 0:
        raise ValueError(
            "The selected file has no ejari_creation_success records and is not a recognizable success_*.json detail file. "
            "Select an Ejari creation progress.json file or a success_*.json file."
        )
    return data


def validate_progress_files(progress_paths):
    valid_files = []
    invalid_files = []
    for progress_path in progress_paths:
        normalized_path = normalize_progress_path(progress_path)
        try:
            progress = load_progress_file(normalized_path)
            valid_files.append(
                {
                    "path": normalized_path,
                    "progress": progress,
                    "success_count": count_progress_success_records(progress),
                }
            )
        except Exception as exc:
            invalid_files.append(
                {
                    "path": normalized_path or progress_path,
                    "error": str(exc),
                }
            )
    return valid_files, invalid_files


def iter_progress_success_records(progress, progress_path=None):
    if not isinstance(progress, dict):
        return
    for emirates_id, emirates_data in progress.items():
        if not isinstance(emirates_data, dict):
            continue
        successes = emirates_data.get("ejari_creation_success") or {}
        if not isinstance(successes, dict):
            continue
        for property_key, record in successes.items():
            if not isinstance(record, dict):
                continue
            yield {
                "emirates_id": str(emirates_id),
                "property_key": str(property_key),
                "record": record,
                "progress_path": str(progress_path) if progress_path else "",
            }


def progress_record_merge_key(emirates_id, property_key, record):
    property_row_value = record.get("property_row_value") or record.get("PropertyRowValue") or property_key
    property_id = record.get("property_id") or record.get("PropertyId")
    if property_row_value:
        return str(emirates_id), "property_row_value", str(property_row_value)
    if property_id:
        return str(emirates_id), "property_id", str(property_id)
    return str(emirates_id), "property_key", str(property_key)


def merge_success_progress_files(valid_files, output_prefix="uploaded_success_progress_merge"):
    if not valid_files:
        raise ValueError("No valid progress files were provided.")
    if len(valid_files) == 1:
        return valid_files[0]["path"], valid_files[0]["success_count"], None

    merged_records = {}
    merged = {}
    summary_rows = []
    for file_info in valid_files:
        source_path = file_info["path"]
        progress = file_info["progress"]
        for emirates_id, emirates_data in progress.items():
            if not isinstance(emirates_data, dict):
                continue
            successes = emirates_data.get("ejari_creation_success") or {}
            if not isinstance(successes, dict):
                continue
            merged.setdefault(
                str(emirates_id),
                {
                    "ejari_creation_success": {},
                    "ejari_creation_failure": {},
                    "ejari_creation_curl_only": {},
                },
            )
            if isinstance(emirates_data.get("property_counts"), dict) and "property_counts" not in merged[str(emirates_id)]:
                merged[str(emirates_id)]["property_counts"] = emirates_data["property_counts"]

            for property_key, record in successes.items():
                if not isinstance(record, dict):
                    continue
                merge_key = progress_record_merge_key(emirates_id, property_key, record)
                timestamp = parse_progress_timestamp(record.get("timestamp"))
                previous = merged_records.get(merge_key)
                if previous is not None and timestamp <= previous["timestamp"]:
                    continue
                merged_records[merge_key] = {
                    "timestamp": timestamp,
                    "source_path": source_path,
                    "emirates_id": str(emirates_id),
                    "property_key": str(record.get("property_row_value") or property_key),
                    "record": record,
                }

    for merged_item in merged_records.values():
        emirates_id = merged_item["emirates_id"]
        property_key = merged_item["property_key"]
        record = merged_item["record"]
        merged.setdefault(
            emirates_id,
            {
                "ejari_creation_success": {},
                "ejari_creation_failure": {},
                "ejari_creation_curl_only": {},
            },
        )
        merged[emirates_id]["ejari_creation_success"][property_key] = record
        summary_rows.append(
            {
                "source_progress_file": str(merged_item["source_path"]),
                "emirates_id": emirates_id,
                "property_id": record.get("property_id"),
                "property_row_value": record.get("property_row_value") or property_key,
                "title": record.get("title"),
                "contract_number": record.get("contract_number"),
                "timestamp": record.get("timestamp"),
            }
        )

    merge_dir = Path("runs") / f"{output_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    merge_dir.mkdir(parents=True, exist_ok=True)
    merged_progress_path = merge_dir / "progress.json"
    merged_progress_path.write_text(json.dumps(merged, ensure_ascii=False, indent=2, default=str), encoding="utf-8")

    with (merge_dir / "merge_summary.csv").open("w", newline="", encoding="utf-8-sig") as f:
        fieldnames = [
            "source_progress_file",
            "emirates_id",
            "property_id",
            "property_row_value",
            "title",
            "contract_number",
            "timestamp",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(summary_rows)
    (merge_dir / "merge_summary.json").write_text(
        json.dumps(summary_rows, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )

    success_count = count_progress_success_records(merged)
    print(f"Merged {len(valid_files)} progress files into: {merged_progress_path}")
    print(f"Merged success records: {success_count}")
    return merged_progress_path, success_count, merge_dir


def resolve_uploaded_success_progress_paths(
    raw_paths,
    *,
    confirm_callback=input,
    merge_output_prefix="uploaded_success_progress_merge",
):
    progress_paths = parse_progress_file_paths(raw_paths)
    if not progress_paths:
        raise ValueError("No progress file paths were provided.")

    valid_files, invalid_files = validate_progress_files(progress_paths)
    if invalid_files:
        print("Invalid progress file(s):")
        for item in invalid_files:
            print(f"- {item['path']}: {item['error']}")

    if invalid_files and len(progress_paths) == 1:
        raise ValueError("The uploaded/provided progress file is invalid; audit cannot continue.")

    if not valid_files:
        raise ValueError("No valid progress files were provided; audit cannot continue.")

    print("Valid progress file(s):")
    for item in valid_files:
        print(f"- {item['path']} ({item['success_count']} successes)")

    if invalid_files:
        try:
            response = confirm_callback("Continue with valid files only?", default=False)
        except TypeError:
            response = confirm_callback("Continue with valid files only? (yes/no) [no]: ")

        if isinstance(response, bool):
            continue_with_valid_files = response
        else:
            continue_with_valid_files = str(response or "").strip().lower() in {"y", "yes"}

        if not continue_with_valid_files:
            raise RuntimeError("User chose not to continue with partial valid progress files.")

    progress_path, success_count, merge_dir = merge_success_progress_files(valid_files, output_prefix=merge_output_prefix)
    return progress_path, success_count, merge_dir, valid_files, invalid_files


def find_latest_ejari_creation_success_progress(runs_glob="ejari_creation_*/progress.json"):
    candidates = []
    for progress_path in Path("runs").glob(runs_glob):
        try:
            progress = load_progress_file(progress_path)
        except Exception:
            continue
        success_count = count_progress_success_records(progress)
        if success_count:
            candidates.append((progress_path.stat().st_mtime, progress_path, success_count))
    if not candidates:
        raise FileNotFoundError("No runs/ejari_creation_*/progress.json file with successes was found.")
    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates[0][1], candidates[0][2]
