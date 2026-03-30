import unittest

from gesture_rules import classify_finger_states


def finger_states(thumb=False, index=False, middle=False, ring=False, pinky=False):
    return {
        "thumb": thumb,
        "index": index,
        "middle": middle,
        "ring": ring,
        "pinky": pinky,
    }


class GestureRulesTests(unittest.TestCase):
    def test_existing_gestures_still_match(self):
        self.assertEqual(
            classify_finger_states(
                finger_states(index=True, middle=True),
                thumb_direction="side",
                thumb_index_touch=False,
            ),
            "Peace ✌️",
        )
        self.assertEqual(
            classify_finger_states(
                finger_states(thumb=True, index=True, middle=True, ring=True, pinky=True),
                thumb_direction="side",
                thumb_index_touch=False,
            ),
            "Open Hand ✋",
        )

    def test_thumbs_down(self):
        self.assertEqual(
            classify_finger_states(
                finger_states(thumb=True),
                thumb_direction="down",
                thumb_index_touch=False,
            ),
            "Thumbs Down 👎",
        )

    def test_pointing_up(self):
        self.assertEqual(
            classify_finger_states(
                finger_states(index=True),
                thumb_direction="side",
                thumb_index_touch=False,
            ),
            "Pointing Up ☝️",
        )

    def test_call_me(self):
        self.assertEqual(
            classify_finger_states(
                finger_states(thumb=True, pinky=True),
                thumb_direction="side",
                thumb_index_touch=False,
            ),
            "Call Me 🤙",
        )

    def test_rock_on(self):
        self.assertEqual(
            classify_finger_states(
                finger_states(index=True, pinky=True),
                thumb_direction="side",
                thumb_index_touch=False,
            ),
            "Rock On 🤘",
        )

    def test_i_love_you_wins_over_similar_patterns(self):
        self.assertEqual(
            classify_finger_states(
                finger_states(thumb=True, index=True, pinky=True),
                thumb_direction="side",
                thumb_index_touch=False,
            ),
            "I Love You 🤟",
        )

    def test_three(self):
        self.assertEqual(
            classify_finger_states(
                finger_states(index=True, middle=True, ring=True),
                thumb_direction="side",
                thumb_index_touch=False,
            ),
            "Three 3️⃣",
        )

    def test_four(self):
        self.assertEqual(
            classify_finger_states(
                finger_states(index=True, middle=True, ring=True, pinky=True),
                thumb_direction="side",
                thumb_index_touch=False,
            ),
            "Four 4️⃣",
        )

    def test_ok_sign(self):
        self.assertEqual(
            classify_finger_states(
                finger_states(middle=True, ring=True, pinky=True),
                thumb_direction="side",
                thumb_index_touch=True,
            ),
            "OK 👌",
        )


if __name__ == "__main__":
    unittest.main()
