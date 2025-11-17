import json
import re
import hashlib
from config import CHUNK_WORD_LIMIT, CHUNK_OVERLAP


def load_postman(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def flatten_items(coll):
    """Recursively flatten Postman 'items'"""
    for it in coll.get("item", []):
        if "item" in it:
            yield from flatten_items(it)
        else:
            req = it.get("request", {}) or {}
            url = ""
            if isinstance(req.get("url", {}), dict):
                url = req.get("url", {}).get("raw", "")
            desc = req.get("description") or it.get("description", "")
            params = []
            if isinstance(req.get("url", {}), dict):
                params = req.get("url", {}).get("query", [])

            body = ""
            if req.get("body"):
                b = req["body"]
                body = b.get("raw", "") if isinstance(b, dict) else str(b)

            responses = it.get("response", []) or []

            yield {
                "name": it.get("name", ""),
                "method": req.get("method", ""),
                "url": url,
                "description": desc,
                "params": params,
                "body": body,
                "responses": responses,
            }


def _words(text):
    return re.findall(r"\S+", text)


def chunk_text(text, wlimit=CHUNK_WORD_LIMIT, overlap=CHUNK_OVERLAP):
    words = _words(text)
    if len(words) <= wlimit:
        return [text.strip()]

    chunks = []
    i = 0
    while i < len(words):
        end = min(i + wlimit, len(words))
        chunks.append(" ".join(words[i:end]))
        if end == len(words):
            break
        i = end - overlap
    return chunks


def build_chunks_from_collection(path):
    coll = load_postman(path)
    chunks = []

    for item in flatten_items(coll):
        parts = []

        parts.append(f"Name: {item['name']}")
        parts.append(f"Method: {item['method']}")
        parts.append(f"URL: {item['url']}")
        if item["description"]:
            parts.append(f"Description: {item['description']}")

        if item["params"]:
            params_str = ", ".join(
                f"{p.get('key')}={p.get('value')} ({p.get('description','')})"
                for p in item["params"]
            )
            parts.append(f"QueryParams: {params_str}")

        if item["body"]:
            parts.append("RequestBody: " + str(item["body"])[:1500])

        if item["responses"]:
            resps = []
            for r in item["responses"]:
                if r.get("body"):
                    resps.append(r["body"][:800])
            if resps:
                parts.append("Responses: " + " ".join(resps))

        full_text = "\n\n".join(parts)

        for idx, chunk in enumerate(chunk_text(full_text)):
            chunks.append(
                {
                    "text": chunk,
                    "meta": {
                        "name": item["name"],
                        "method": item["method"],
                        "url": item["url"],
                        "chunk_index": idx,
                        "id": hashlib.sha1(
                            (item["name"] + str(idx)).encode()
                        ).hexdigest(),
                    },
                }
            )

    return chunks
