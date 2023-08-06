import tensorflow as tf
import os

DEVICE = "GPU" if tf.config.list_physical_devices("GPU") else "CPU"

SECTIONS = {
    "full": [i for i in range(1, 6)],
    "header": [1],
    "disclaimer": [2],
    "greetings": [3],
    "body": [4],
    "signature": [5],
    "caution": [6],
}

FEATURE_REGEX = {
    "phone_number": "[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]",
    "url": "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$",
    "punctuation": "[!?]",
    "horizontal_separator": "[-=~]",
    "hashtag": "[#]",
    "pipe": "[|]",
    "email": "[-\\w\\.]+@([-\\w]+\\.)+[-\\w]{2,4}",
    "capitalized": "[A-Z][a-z]*",
    "full_caps": "[A-Z]{2,}",
}

PREPROCESSING = {
    "text_replacements": [
        {"pattern": "\\xa333", "replacement": ""},
        {"pattern": "\\u2019", "replacement": "'"},
        {"pattern": "\r\n\t\t", "replacement": ""},
        {"pattern": " B7; ", "replacement": ""},
        {"pattern": "\\xb4", "replacement": "'"},
        {"pattern": "&#43;", "replacement": "+"},
        {"pattern": "\\xa0", "replacement": " "},
        {"pattern": "\\xa0", "replacement": " "},
        {"pattern": "f\\xfcr", "replacement": "'s"},
        {"pattern": "\\xa", "replacement": " x"},
        {"pattern": "_x000D_", "replacement": ""},
        {"pattern": "x000D", "replacement": "\n"},
        {"pattern": ".à", "replacement": " a"},
        {"pattern": " ", "replacement": ""},
        {"pattern": "‎", "replacement": ""},
        {"pattern": "­", "replacement": ""},
        {"pattern": "﻿", "replacement": ""},
        {"pattern": "&nbsp;", "replacement": ""},
        {"pattern": "&#43;", "replacement": ""},
        {"pattern": "&lt;", "replacement": "<"},
        {"pattern": "&quot;", "replacement": "'"},
        {"pattern": "&gt;", "replacement": ">"},
        {"pattern": "ï»¿", "replacement": ""},
        {"pattern": "...", "replacement": "."},
        {"pattern": "..", "replacement": "."},
        {"pattern": " .", "replacement": ". "},
        {"pattern": "\r\n", "replacement": "\n"},
        {"pattern": "\\xa0", "replacement": " "},
        {"pattern": "：", "replacement": ": "},
        {"pattern": "\u200b", "replacement": ""},
        {"pattern": "\u2026", "replacement": "..."},
        {"pattern": "’", "replacement": "'"},
        {"pattern": "...", "replacement": "."},
        {"pattern": "..", "replacement": "."},
        {"pattern": ":\\s+", "replacement": ": "},
        {"pattern": " .", "replacement": ". "},
        {"pattern": ":\\s?\\.", "replacement": ":"},
    ],
    "regex_replacements": [
        {"pattern": "(<|\\[)https?:\/\/.*(\\.).*(>|\\])", "replacement": ""},
        {"pattern": "(?:[^\r\n\t\f\\v]*{[^{}]*})+", "replacement": ""},
        {"pattern": "[^\r\n\t\f\\v]*\\s*(\\}|\\{)\\s*|@import.*", "replacement": ""},
        {"pattern": "\/\\*[^*]*\\*+([^/*][^*]*\\*+)*\/", "replacement": ""},
        {"pattern": "^(\\s*\\|\\s+)+", "replacement": ""},
        {"pattern": "\\[cid:.*\\]", "replacement": ""},
        {"pattern": "^>+[ ]*", "replacement": ""},
    ],
}
