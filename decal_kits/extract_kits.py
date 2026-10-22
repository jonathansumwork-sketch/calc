#!/usr/bin/env python3
"""Scan a folder tree for decal repair-kit PDFs and extract them into a review set.

Usage:
    python3 extract_kits.py ROOT OUT_DIR [--deep]

ROOT is only ever read. Writes to OUT_DIR:
    kits.csv         one row per PDF - review this before any Jotform is created
    parts.csv        one row per part code per PDF
    kits.json        the same data in full, for the form-building stage
    skipped_pdfs.txt PDFs under ROOT that were not treated as repair kits
    part_sheets/     PNG of each kit's part-sheet page

By default a PDF counts as a repair kit when its file name contains "repair kit".
--deep also opens every other PDF and checks for a "PARTS PRICELIST" page.

Requires: pip install pdfplumber pypdfium2
"""
import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pdfplumber

MAKES = [
    "ALFA ROMEO", "AUDI", "BMW", "BYD", "CHERY", "CITROEN", "CUPRA", "FIAT", "FORD",
    "FUSO", "GWM", "HAVAL", "HINO", "HOLDEN", "HONDA", "HYUNDAI", "ISUZU", "IVECO",
    "JEEP", "KIA", "LAND ROVER", "LDV", "LEXUS", "MAZDA", "MERCEDES-BENZ", "MERCEDES",
    "MG", "MITSUBISHI", "NISSAN", "PEUGEOT", "POLESTAR", "RENAULT", "SKODA",
    "SSANGYONG", "SUBARU", "SUZUKI", "TESLA", "TOYOTA", "VOLKSWAGEN", "VOLVO",
]
MAKE_RE = re.compile(
    r"(?<![A-Z0-9])("
    + "|".join(sorted(map(re.escape, MAKES), key=len, reverse=True))
    + r")(?![A-Z0-9])",
    re.I,
)
KEEP_UPPER = {"BMW", "BYD", "GWM", "LDV", "MG", "EV", "SUV"}
SMALL_WORDS = {"of", "and", "the", "for", "to", "in", "on"}

MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December",
]
MONTH_RE = re.compile(
    r"\b(JAN(?:UARY)?|FEB(?:RUARY)?|MAR(?:CH)?|APR(?:IL)?|MAY|JUNE?|JULY?|AUG(?:UST)?"
    r"|SEP(?:T(?:EMBER)?)?|OCT(?:OBER)?|NOV(?:EMBER)?|DEC(?:EMBER)?)\.?\s*,?\s*(20\d\d)\b",
    re.I,
)

KIT_NAME_RE = re.compile(r"repair[\s_\-]*kit", re.I)
CODE_RE = re.compile(r"^\s*([A-Z]{1,2}\d{1,2})(?=\s|$)\s*(.*)$")
LABEL_LINE_RE = re.compile(r"^\s*(?:[A-Z]{1,2}\d{1,2}\s*)+$")
PRICE_RE = re.compile(r"\$\s*([\d,]+(?:\.\d+)?)(?:\s*\+\s*GST)?", re.I)
STOP_RE = re.compile(r"ADDITIONAL\s+COST|CALL\s*OUT|Please send|Project Manager|Email:", re.I)


def smart_title(text):
    out = []
    for i, word in enumerate(text.split()):
        w = word.upper()
        if w in KEEP_UPPER or re.search(r"\d", w) or (len(w) <= 2 and w.isalpha() and (i == 0 or w.lower() not in SMALL_WORDS)):
            out.append(w)
        elif i and w.lower() in SMALL_WORDS:
            out.append(w.lower())
        else:
            out.append("-".join(p.capitalize() for p in w.split("-")))
    return " ".join(out)


def find_date(text):
    m = MONTH_RE.search(text)
    if not m:
        return None
    idx = [n[:3].upper() for n in MONTH_NAMES].index(m.group(1)[:3].upper())
    return f"{MONTH_NAMES[idx]} {m.group(2)}", f"{m.group(2)}-{idx + 1:02d}"


def lines_before(text, pattern):
    out = []
    for line in text.splitlines():
        if re.search(pattern, line, re.I):
            break
        if line.strip():
            out.append(re.sub(r"\s+", " ", line.strip()))
    return " ".join(out)


def parse_filename(stem):
    segs = [s.strip() for s in re.split(r"\s+-\s+", stem.replace("_", " ")) if s.strip()]
    job = segs.pop(0) if segs and re.fullmatch(r"\d{4,}", segs[0]) else ""
    kit_idx = next((i for i, s in enumerate(segs) if KIT_NAME_RE.search(s)), None)
    middle = segs[1:kit_idx] if kit_idx is not None else segs[1:]
    return {
        "job": job,
        "client": segs[0] if segs else "",
        "vehicle": middle[-1] if middle else "",
        "date": find_date(" ".join(segs[kit_idx:]) if kit_idx is not None else stem),
    }


def split_title(title):
    client, rest = title.split(" - ", 1) if " - " in title else ("", title)
    matches = list(MAKE_RE.finditer(rest))
    return {
        "client": client.strip(),
        "program": (rest[: matches[0].start()] if matches else rest).strip(" -"),
        "makes": {m.group(1).upper() for m in matches},
        "rest": rest,
        "matches": matches,
    }


def model_after(parsed, make):
    last = [m for m in parsed["matches"] if m.group(1).upper() == make]
    return parsed["rest"][last[-1].end():].strip(" -") if last else ""


def parse_pricelist(text, flags):
    lines = [ln.rstrip() for ln in text.splitlines()]
    header = next((i for i, ln in enumerate(lines) if re.search(r"Part\s+Number", ln, re.I)), None)
    if header is None:
        flags.append("no_price_table_header")
        return [], None, []
    desc_col = lines[header].find("Position")
    parts, unparsed = [], []
    for ln in lines[header + 1:]:
        if not ln.strip():
            continue
        if STOP_RE.search(ln):
            break
        m = CODE_RE.match(ln)
        if m:
            rest = m.group(2)
            prices = [p.replace(",", "") for p in PRICE_RE.findall(rest)]
            desc = re.sub(r"\s{2,}", " ", PRICE_RE.sub("", rest)).strip()
            if len(prices) != 2 or not desc:
                flags.append(f"part_{m.group(1)}_incomplete")
            parts.append({
                "code": m.group(1),
                "description": desc,
                "supply_only_ex_gst": prices[0] if prices else "",
                "supply_install_ex_gst": prices[1] if len(prices) > 1 else "",
            })
        elif parts and len(ln) - len(ln.lstrip()) >= max(desc_col - 4, 20):
            parts[-1]["description"] += " " + re.sub(r"\s+", " ", ln.strip())
        else:
            unparsed.append(ln.strip())
    if unparsed:
        flags.append("unparsed_pricelist_lines")
    return parts, desc_col, unparsed


def parse_callout_and_contact(text):
    callout = re.search(r"ADDITIONAL\s+COST\s+\$\s*([\d,.]+)", text, re.I)
    contact = re.search(r"Please send orders[^\n]*\n(.*?)Email:\s*(\S+@\S+)", text, re.S | re.I)
    name = role = ""
    if contact:
        got = [re.sub(r"\s+", " ", ln.strip()) for ln in contact.group(1).splitlines() if ln.strip()]
        name, role = (got + ["", ""])[:2]
    return {
        "callout_fee_ex_gst": callout.group(1).replace(",", "") if callout else "",
        "contact_name": name,
        "contact_role": role,
        "contact_email": contact.group(2).strip(".,;") if contact else "",
    }


def pick_make(sources, flags):
    votes = Counter(m for makes in sources.values() for m in makes)
    if not votes:
        flags.append("make_not_found")
        return ""
    top = votes.most_common()
    make = top[0][0]
    if len(top) > 1 and top[0][1] == top[1][1]:
        flags.append("make_ambiguous:" + "/".join(m for m, _ in top))
        sheet = sources.get("part_sheet_title") or set()
        make = next((m for m, _ in top if m in sheet), make)
    for src, makes in sources.items():
        if makes and makes != {make}:
            flags.append(f"make_disagrees:{src}={'/'.join(sorted(makes))}")
    return make


def pick_model(title_model, file_model, flags):
    if title_model and file_model:
        a, b = title_model.upper(), file_model.upper()
        if a in b:
            return file_model
        if b in a:
            return title_model
        flags.append(f"model_disagrees:title={title_model}|file={file_model}")
        return title_model
    return title_model or file_model


def slugify(text):
    return re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_")


def extract_kit(path, png_dir):
    flags = []
    raw = path.read_bytes()
    sha = hashlib.sha1(raw).hexdigest()
    fname = parse_filename(path.stem)
    with pdfplumber.open(path) as pdf:
        pages = [p.extract_text(layout=True) or "" for p in pdf.pages]
        price_i = next((i for i, t in enumerate(pages) if re.search(r"PARTS\s+PRICELIST", t, re.I)), None)
        sheet_i = next((i for i, t in enumerate(pages) if re.search(r"PART\s+SHEET", t, re.I)), None)
        if price_i is None:
            flags.append("no_pricelist_page")
        if sheet_i is None:
            flags.append("no_part_sheet_page")
        sheet_title = lines_before(pages[sheet_i], r"PART\s+SHEET") if sheet_i is not None else ""
        price_title = lines_before(pages[price_i], r"PARTS\s+PRICELIST") if price_i is not None else ""
        sheet_png = None
        if sheet_i is not None:
            sheet_png = (png_dir / f"{sha[:10]}.png")
            pdf.pages[sheet_i].to_image(resolution=150).save(str(sheet_png), format="PNG")

    price = split_title(price_title)
    sheet = split_title(sheet_title)
    client = price["client"] or sheet["client"] or fname["client"]
    if not (price["client"] or sheet["client"]):
        flags.append("client_taken_from_filename")
    program = price["program"] or sheet["program"]
    if price["program"] and sheet["program"] and price["program"].upper() != sheet["program"].upper():
        flags.append("program_differs_between_pages")

    file_makes = {m.group(1).upper() for m in MAKE_RE.finditer(fname["vehicle"])}
    make = pick_make(
        {"pricelist_title": price["makes"], "part_sheet_title": sheet["makes"], "filename": file_makes}, flags
    )
    file_model = re.sub(r"\s+", " ", MAKE_RE.sub("", fname["vehicle"])).strip(" -")
    model = pick_model(model_after(price, make) or model_after(sheet, make), file_model, flags)
    if not model:
        flags.append("model_not_found")

    parts, _, unparsed = parse_pricelist(pages[price_i], flags) if price_i is not None else ([], None, [])
    if not parts:
        flags.append("no_parts_found")
    codes = [p["code"] for p in parts]
    if len(set(codes)) != len(codes):
        flags.append("duplicate_part_codes")
    if sheet_i is not None and parts:
        on_sheet = {c for ln in pages[sheet_i].splitlines() if LABEL_LINE_RE.match(ln) for c in ln.split()}
        only_table, only_sheet = sorted(set(codes) - on_sheet), sorted(on_sheet - set(codes))
        if only_table or only_sheet:
            flags.append(f"part_sheet_labels_differ:table_only={','.join(only_table)}|sheet_only={','.join(only_sheet)}")

    date = find_date("\n".join(pages)) or fname["date"]
    if not date:
        flags.append("date_not_found")
    elif fname["date"] and fname["date"][1] != date[1]:
        flags.append(f"date_differs_from_filename:pdf={date[1]}|filename={fname['date'][1]}")

    extra = parse_callout_and_contact(pages[price_i]) if price_i is not None else {}
    if not extra.get("contact_email"):
        flags.append("no_orders_email")

    client_t, program_t, make_t, model_t = smart_title(client), smart_title(program), smart_title(make), smart_title(model)
    vehicle = " ".join(x for x in (make_t, model_t) if x)
    form_name = " - ".join(x for x in (client_t, program_t, f"{vehicle} Repair Kit") if x)

    return {
        "source_pdf": str(path),
        "sha1": sha,
        "job_number": fname["job"],
        "client": client_t,
        "program": program_t,
        "make": make_t,
        "model": model_t,
        "form_name": form_name,
        "pricelist_date": date[0] if date else "",
        "pricelist_date_iso": date[1] if date else "",
        "parts": parts,
        "part_sheet_png": str(sheet_png) if sheet_png else "",
        "unparsed_pricelist_lines": unparsed,
        "flags": flags,
        **extra,
    }


def mark_versions(kits):
    groups = defaultdict(list)
    for k in kits:
        if k["extract_status"] != "error":
            groups[(k["client"].lower(), k["program"].lower(), k["make"].lower(), k["model"].lower())].append(k)
    for group in groups.values():
        group.sort(key=lambda k: k["source_pdf"])
        group.sort(key=lambda k: k["pricelist_date_iso"], reverse=True)  # stable: newest first, then path order
        keeper = group[0]
        for other in group[1:]:
            if other["sha1"] == keeper["sha1"]:
                other["extract_status"], other["superseded_by"] = "exact_duplicate", keeper["source_pdf"]
            elif other["pricelist_date_iso"] == keeper["pricelist_date_iso"]:
                other["extract_status"], other["superseded_by"] = "same_date_conflict", keeper["source_pdf"]
                keeper["flags"].append("same_date_conflict_with:" + other["source_pdf"])
                if keeper["extract_status"] == "ready":
                    keeper["extract_status"] = "needs_review"
            else:
                other["extract_status"], other["superseded_by"] = "superseded", keeper["source_pdf"]


def is_kit_pdf(path, deep):
    if KIT_NAME_RE.search(path.name):
        return True
    if not deep:
        return False
    try:
        with pdfplumber.open(path) as pdf:
            return any(re.search(r"PARTS\s+PRICELIST", p.extract_text() or "", re.I) for p in pdf.pages[:4])
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--deep", action="store_true")
    args = ap.parse_args()

    out = args.out.resolve()
    png_dir = out / "part_sheets"
    png_dir.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(p for p in args.root.rglob("*") if p.suffix.lower() == ".pdf" and p.is_file() and out not in p.resolve().parents)
    kits, skipped = [], []
    for n, path in enumerate(pdfs, 1):
        if not is_kit_pdf(path, args.deep):
            skipped.append(str(path))
            continue
        print(f"[{n}/{len(pdfs)}] {path.name}", file=sys.stderr)
        try:
            kit = extract_kit(path, png_dir)
            kit["extract_status"] = "needs_review" if kit["flags"] else "ready"
        except Exception as exc:  # one bad PDF must not stop the run
            kit = {"source_pdf": str(path), "flags": [f"error:{type(exc).__name__}:{exc}"], "extract_status": "error",
                   "parts": [], "client": "", "program": "", "make": "", "model": "", "form_name": "",
                   "pricelist_date": "", "pricelist_date_iso": "", "sha1": "", "job_number": "",
                   "part_sheet_png": "", "unparsed_pricelist_lines": []}
        kit.setdefault("superseded_by", "")
        kits.append(kit)
    mark_versions(kits)

    # Rename PNGs to something readable now that make/model/date are known.
    for k in kits:
        if k["part_sheet_png"]:
            old = Path(k["part_sheet_png"])
            new = png_dir / f"{slugify(' '.join([k['client'], k['make'], k['model'], k['pricelist_date_iso']]))}_{k['sha1'][:6]}.png"
            if old.exists():
                old.replace(new)
            k["part_sheet_png"] = str(new)

    (out / "kits.json").write_text(json.dumps(kits, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "skipped_pdfs.txt").write_text("\n".join(skipped), encoding="utf-8")

    with open(out / "kits.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["Client", "Vehicle Make", "Vehicle Model", "Form Name", "Pricelist Date", "Extract Status",
                    "Flags", "Part Codes", "Orders Email", "Job Number", "Source PDF", "Part Sheet PNG", "Superseded By"])
        for k in sorted(kits, key=lambda k: (k["client"], k["make"], k["model"], k["pricelist_date_iso"])):
            w.writerow([k["client"], k["make"], k["model"], k["form_name"], k["pricelist_date"], k["extract_status"],
                        "; ".join(k["flags"]), " ".join(p["code"] for p in k["parts"]), k.get("contact_email", ""),
                        k["job_number"], k["source_pdf"], k["part_sheet_png"], k["superseded_by"]])
    with open(out / "parts.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["Source PDF", "Part Code", "Description", "Supply Only ex GST", "Supply & Install ex GST"])
        for k in kits:
            for p in k["parts"]:
                w.writerow([k["source_pdf"], p["code"], p["description"], p["supply_only_ex_gst"], p["supply_install_ex_gst"]])

    counts = Counter(k["extract_status"] for k in kits)
    print(f"\n{len(kits)} repair-kit PDFs found, {len(skipped)} other PDFs skipped", file=sys.stderr)
    for status, n in sorted(counts.items()):
        print(f"  {status}: {n}", file=sys.stderr)
    print(f"Review: {out / 'kits.csv'}", file=sys.stderr)


if __name__ == "__main__":
    main()
