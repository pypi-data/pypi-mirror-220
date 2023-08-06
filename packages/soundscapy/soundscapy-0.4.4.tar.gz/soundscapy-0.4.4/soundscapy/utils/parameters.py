# Constants and Labels
PAQ_NAMES = [
    "pleasant",
    "vibrant",
    "eventful",
    "chaotic",
    "annoying",
    "monotonous",
    "uneventful",
    "calm",
]

PAQ_IDS = [
    "PAQ1",
    "PAQ2",
    "PAQ3",
    "PAQ4",
    "PAQ5",
    "PAQ6",
    "PAQ7",
    "PAQ8",
]

IGNORE_LIST = ["AllLondon", "AllyPally", "CoventGd1", "OxfordSt"]

CATEGORISED_VARS = {
    "indexing": [
        "GroupID",
        "SessionID",
        "LocationID",
        "Country",
        "record_id",
    ],  # Ways to index which survey it is
    "meta_info": [
        "recording",
        "start_time",
        "end_time",
        "longitude",
        "latitude",
    ],  # Info from when that survey was collected
    "sound_source_dominance": [
        "Traffic",
        "Other",
        "Human",
        "Natural",
    ],  # Sound sources
    "complex_PAQs": ["Pleasant", "Eventful"],  # Projected PAQ coordinates
    "raw_PAQs": [
        "pleasant",
        "chaotic",
        "vibrant",
        "uneventful",
        "calm",
        "annoying",
        "eventful",
        "monotonous",
    ],  # Raw 5-point PAQs
    "overall_soundscape": [
        "overall",
        "appropriateness",
        "loudness",
        "often",
        "visit_again",
    ],  # Questions about the overall soundscape
    "demographics": ["Age", "Gender", "Occupation", "Education", "Ethnicity", "Resid"],
    "misc": ["AnythingElse"],
}

ENGLISH_PAQS = {
    "PAQ1": {
        "name": "pleasant",
        "eq_angle": 0,
        "corr_angle": 0,
    },
    "PAQ2": {
        "name": "vibrant",
        "eq_angle": 45,
        "corr_angle": 46,
    },
    "PAQ3": {
        "name": "eventful",
        "eq_angle": 90,
        "corr_angle": 93,
    },
    "PAQ4": {
        "name": "chaotic",
        "eq_angle": 135,
        "corr_angle": 138,
    },
    "PAQ5": {
        "name": "annoying",
        "eq_angle": 180,
        "corr_angle": 178
    },
    "PAQ6": {
        "name": "monotonous",
        "eq_angle": 225,
        "corr_angle": 229,
    },
    "PAQ7": {
        "name": "uneventful",
        "eq_angle": 270,
        "corr_angle": 272
    },
    "PAQ8": {
        "name": "calm",
        "eq_angle": 325,
        "corr_angle": 340
    }
}
