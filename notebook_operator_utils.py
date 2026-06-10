import csv
import os
from pathlib import Path


YES_VALUES = {"y", "yes", "true", "1", "all"}
NO_VALUES = {"n", "no", "false", "0"}


def _normalize_options(options):
    normalized = []
    for option in options:
        if isinstance(option, dict):
            value = str(option.get("value", option.get("label", "")))
            label = str(option.get("label", value))
            description = str(option.get("description", "") or "")
        elif isinstance(option, (tuple, list)) and len(option) >= 2:
            value = str(option[0])
            label = str(option[1])
            description = str(option[2]) if len(option) >= 3 and option[2] is not None else ""
        else:
            value = str(option)
            label = str(option)
            description = ""
        if not value:
            continue
        normalized.append({"value": value, "label": label, "description": description})
    if not normalized:
        raise ValueError("At least one option is required.")
    return normalized


def _resolve_default_value(normalized_options, default):
    if default is None:
        return normalized_options[0]["value"]
    default_text = str(default)
    for option in normalized_options:
        if option["value"].lower() == default_text.lower() or option["label"].lower() == default_text.lower():
            return option["value"]
    return normalized_options[0]["value"]


def _popup_enabled():
    return os.environ.get("NOTEBOOK_UI_DISABLE_POPUP", "").strip().lower() not in {"1", "true", "yes"}


def _try_tk_choice(prompt, normalized_options, default_value, title):
    if not _popup_enabled():
        return None

    try:
        import tkinter as tk
        from tkinter import ttk
    except Exception:
        return None

    root = None
    try:
        root = tk.Tk()
        root.withdraw()

        dialog = tk.Toplevel(root)
        dialog.title(title or "Select option")
        dialog.resizable(False, False)
        dialog.protocol("WM_DELETE_WINDOW", lambda: on_cancel())

        try:
            dialog.attributes("-topmost", True)
        except Exception:
            pass

        selected = tk.StringVar(value=default_value)
        result = {"value": None}

        frame = ttk.Frame(dialog, padding=16)
        frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame, text=prompt, wraplength=520, justify="left").grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )

        for row_index, option in enumerate(normalized_options, start=1):
            button_text = option["label"]
            if option["description"]:
                button_text = f"{button_text} - {option['description']}"
            ttk.Radiobutton(
                frame,
                text=button_text,
                value=option["value"],
                variable=selected,
            ).grid(row=row_index, column=0, sticky="w", pady=2)

        buttons = ttk.Frame(frame)
        buttons.grid(row=len(normalized_options) + 1, column=0, sticky="e", pady=(14, 0))

        def on_ok():
            result["value"] = selected.get()
            dialog.destroy()

        def on_cancel():
            result["value"] = default_value
            dialog.destroy()

        ttk.Button(buttons, text="OK", command=on_ok).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(buttons, text="Cancel", command=on_cancel).grid(row=0, column=1)

        dialog.update_idletasks()
        width = dialog.winfo_reqwidth()
        height = dialog.winfo_reqheight()
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 3)
        dialog.geometry(f"+{max(x, 0)}+{max(y, 0)}")

        dialog.grab_set()
        dialog.focus_force()
        root.wait_window(dialog)
        return result["value"]
    except Exception:
        return None
    finally:
        if root is not None:
            try:
                root.destroy()
            except Exception:
                pass


def _text_choice(prompt, normalized_options, default_value, aliases=None):
    aliases = {str(key).lower(): str(value) for key, value in (aliases or {}).items()}
    lookup = {}
    for index, option in enumerate(normalized_options, start=1):
        lookup[str(index)] = option["value"]
        lookup[option["value"].lower()] = option["value"]
        lookup[option["label"].lower()] = option["value"]

    print(prompt)
    for index, option in enumerate(normalized_options, start=1):
        detail = f" - {option['description']}" if option["description"] else ""
        marker = " [default]" if option["value"] == default_value else ""
        print(f"{index}. {option['label']}{detail}{marker}")

    while True:
        value = input("Select option: ").strip().lower()
        if value == "":
            return default_value
        value = aliases.get(value, value)
        selected = lookup.get(str(value).lower())
        if selected is not None:
            return selected
        print("Please choose one of the listed options.")


def choose_option(prompt, options, default=None, aliases=None, title="Notebook option"):
    normalized_options = _normalize_options(options)
    default_value = _resolve_default_value(normalized_options, default)
    selected = _try_tk_choice(prompt, normalized_options, default_value, title)
    if selected is not None:
        return selected
    return _text_choice(prompt, normalized_options, default_value, aliases=aliases)


def _resolve_default_values(normalized_options, default):
    option_values = {option["value"].lower(): option["value"] for option in normalized_options}
    option_labels = {option["label"].lower(): option["value"] for option in normalized_options}
    if default is None:
        return []
    if isinstance(default, str):
        raw_values = _parse_file_path_text(default)
    else:
        raw_values = list(default)

    selected = []
    seen = set()
    for value in raw_values:
        text = str(value).strip().lower()
        option_value = option_values.get(text) or option_labels.get(text)
        if option_value and option_value not in seen:
            seen.add(option_value)
            selected.append(option_value)
    return selected


def _try_tk_multi_choice(prompt, normalized_options, default_values, title):
    if not _popup_enabled():
        return None

    try:
        import tkinter as tk
        from tkinter import ttk
    except Exception:
        return None

    root = None
    try:
        root = tk.Tk()
        root.withdraw()

        dialog = tk.Toplevel(root)
        dialog.title(title or "Select options")
        dialog.resizable(False, False)
        dialog.protocol("WM_DELETE_WINDOW", lambda: on_cancel())

        try:
            dialog.attributes("-topmost", True)
        except Exception:
            pass

        result = {"values": None}
        selected = {
            option["value"]: tk.BooleanVar(value=option["value"] in default_values)
            for option in normalized_options
        }

        frame = ttk.Frame(dialog, padding=16)
        frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame, text=prompt, wraplength=560, justify="left").grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )

        for row_index, option in enumerate(normalized_options, start=1):
            button_text = option["label"]
            if option["description"]:
                button_text = f"{button_text} - {option['description']}"
            ttk.Checkbutton(
                frame,
                text=button_text,
                variable=selected[option["value"]],
            ).grid(row=row_index, column=0, sticky="w", pady=2)

        buttons = ttk.Frame(frame)
        buttons.grid(row=len(normalized_options) + 1, column=0, sticky="e", pady=(14, 0))

        def on_ok():
            result["values"] = [
                option["value"]
                for option in normalized_options
                if selected[option["value"]].get()
            ]
            dialog.destroy()

        def on_cancel():
            result["values"] = list(default_values)
            dialog.destroy()

        ttk.Button(buttons, text="OK", command=on_ok).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(buttons, text="Cancel", command=on_cancel).grid(row=0, column=1)

        dialog.update_idletasks()
        width = dialog.winfo_reqwidth()
        height = dialog.winfo_reqheight()
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 3)
        dialog.geometry(f"+{max(x, 0)}+{max(y, 0)}")

        dialog.grab_set()
        dialog.focus_force()
        root.wait_window(dialog)
        return result["values"]
    except Exception:
        return None
    finally:
        if root is not None:
            try:
                root.destroy()
            except Exception:
                pass


def _text_multi_choice(prompt, normalized_options, default_values, aliases=None):
    aliases = {str(key).lower(): str(value) for key, value in (aliases or {}).items()}
    lookup = {}
    for index, option in enumerate(normalized_options, start=1):
        lookup[str(index)] = option["value"]
        lookup[option["value"].lower()] = option["value"]
        lookup[option["label"].lower()] = option["value"]

    print(prompt)
    for index, option in enumerate(normalized_options, start=1):
        detail = f" - {option['description']}" if option["description"] else ""
        marker = " [default]" if option["value"] in default_values else ""
        print(f"{index}. {option['label']}{detail}{marker}")

    while True:
        value = input("Select one or more options (comma separated, all, none): ").strip()
        if value == "":
            return list(default_values)
        if value.lower() == "none":
            return []
        if value.lower() == "all":
            return [option["value"] for option in normalized_options]

        selected = []
        seen = set()
        for raw_value in value.replace(";", ",").split(","):
            key = raw_value.strip().lower()
            if not key:
                continue
            key = aliases.get(key, key)
            option_value = lookup.get(str(key).lower())
            if option_value and option_value not in seen:
                seen.add(option_value)
                selected.append(option_value)
        if selected:
            return selected
        print("Please choose one or more listed options.")


def choose_multiple_options(prompt, options, default=None, aliases=None, title="Notebook options"):
    normalized_options = _normalize_options(options)
    default_values = _resolve_default_values(normalized_options, default)
    selected = _try_tk_multi_choice(prompt, normalized_options, default_values, title)
    if selected is not None:
        return selected
    return _text_multi_choice(prompt, normalized_options, default_values, aliases=aliases)


def ask_yes_no(prompt, default=False, yes_aliases=None, no_aliases=None):
    aliases = {}
    for value in YES_VALUES | set(yes_aliases or ()):
        aliases[value] = "yes"
    for value in NO_VALUES | set(no_aliases or ()):
        aliases[value] = "no"
    choice = choose_option(
        prompt,
        [("yes", "Yes"), ("no", "No")],
        default="yes" if default else "no",
        aliases=aliases,
        title="Confirm",
    )
    return choice == "yes"


def _parse_file_path_text(raw_paths):
    raw_paths = str(raw_paths or "").strip()
    if not raw_paths:
        return []

    separators_present = any(separator in raw_paths for separator in (",", ";", "\n"))
    if not separators_present:
        return [raw_paths]

    normalized = raw_paths.replace(";", ",").replace("\n", ",")
    parsed_paths = []
    try:
        for row in csv.reader([normalized], skipinitialspace=True):
            parsed_paths.extend(row)
    except Exception:
        parsed_paths = normalized.split(",")
    return [path.strip().strip('"').strip("'") for path in parsed_paths if path.strip()]


def _try_tk_file_picker(prompt, default_dir=".", multiple=True, filetypes=None, title=None):
    if not _popup_enabled():
        return None

    try:
        import tkinter as tk
        from tkinter import filedialog
    except Exception:
        return None

    root = None
    try:
        root = tk.Tk()
        root.withdraw()
        try:
            root.attributes("-topmost", True)
        except Exception:
            pass
        root.update()
        initial_dir = Path(default_dir or ".").expanduser().resolve()
        picker_title = title or prompt or "Select file"
        picker_filetypes = filetypes or (("JSON files", "*.json"), ("All files", "*.*"))
        if multiple:
            selected = filedialog.askopenfilenames(
                parent=root,
                title=picker_title,
                initialdir=str(initial_dir),
                filetypes=picker_filetypes,
            )
            return [str(path) for path in selected]
        selected = filedialog.askopenfilename(
            parent=root,
            title=picker_title,
            initialdir=str(initial_dir),
            filetypes=picker_filetypes,
        )
        return [str(selected)] if selected else []
    except Exception:
        return None
    finally:
        if root is not None:
            try:
                root.destroy()
            except Exception:
                pass


def select_file_paths(prompt, default_dir=".", multiple=True, filetypes=None, title=None):
    selected_paths = _try_tk_file_picker(
        prompt,
        default_dir=default_dir,
        multiple=multiple,
        filetypes=filetypes,
        title=title,
    )
    if selected_paths is not None:
        if selected_paths:
            print("Selected file(s):")
            for path in selected_paths:
                print(f"- {path}")
        else:
            print("No file selected.")
        return selected_paths

    raw_paths = input(f"{prompt}: ").strip()
    return _parse_file_path_text(raw_paths)


def select_emirates_ids_for_section(section_name, emirates_ids, default_all=True):
    emirates_ids = [str(emirates_id) for emirates_id in emirates_ids]
    process_all = ask_yes_no(f"Process all Emirates IDs for {section_name}?", default=default_all)
    if process_all:
        print(f"Selected all configured Emirates IDs for {section_name}.")
        return emirates_ids

    selected = []
    for emirates_id in emirates_ids:
        if ask_yes_no(f"Process Emirates ID {emirates_id} for {section_name}?", default=True):
            selected.append(emirates_id)
        else:
            print(f"Skipped {section_name} for Emirates ID {emirates_id}.")
    return selected
