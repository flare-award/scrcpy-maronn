#include "common.h"

#include <assert.h>
#include <stdlib.h>
#include <string.h>

#include "keyboard_sdk.h"

// Capture the message in place of the controller thread (including ownership).
static struct sc_control_msg pending;
static bool has_message;

bool
sc_controller_push_msg(struct sc_controller *controller,
                       const struct sc_control_msg *msg) {
    (void) controller;
    assert(!has_message);
    pending = *msg;
    has_message = true;
    return true;
}

static void
expect_key(enum android_keycode keycode, enum android_keyevent_action action) {
    assert(has_message && pending.type == SC_CONTROL_MSG_TYPE_INJECT_KEYCODE);
    assert(pending.inject_keycode.keycode == keycode);
    assert(pending.inject_keycode.action == action);
    has_message = false;
}

static void
expect_text(enum sc_control_msg_type type, const char *text) {
    assert(has_message && pending.type == type);
    assert(!strcmp(pending.inject_text.text, text));
    free(pending.inject_text.text);
    has_message = false;
}

static void
type_text(struct sc_keyboard_sdk *kb, const char *text) {
    struct sc_text_event event = {.text = text};
    kb->key_processor.ops->process_text(&kb->key_processor, &event);
}

static void
key(struct sc_keyboard_sdk *kb, enum sc_action action,
    enum sc_keycode layout_keycode, uint16_t mods) {
    struct sc_key_event event = {
        .action = action,
        .keycode = SC_KEYCODE_a, // SDL's event keycode, even on a Russian layout
        .layout_keycode = layout_keycode,
        .scancode = SC_SCANCODE_A,
        .mods_state = mods,
    };
    kb->key_processor.ops->process_key(&kb->key_processor, &event, 0);
}

int
main(void) {
    struct sc_keyboard_sdk kb;
    sc_keyboard_sdk_init(&kb, NULL, SC_KEY_INJECT_MODE_MIXED, true, true);

    key(&kb, SC_ACTION_DOWN, SC_KEYCODE_a, 0);
    expect_key(AKEYCODE_A, AKEY_EVENT_ACTION_DOWN);
    type_text(&kb, "a");
    assert(!has_message);
    key(&kb, SC_ACTION_UP, SC_KEYCODE_a, 0);
    expect_key(AKEYCODE_A, AKEY_EVENT_ACTION_UP);

    // EN -> RU: do not send a spurious A before the actual Cyrillic text.
    enum sc_keycode cyrillic_ef = 0x0444;
    key(&kb, SC_ACTION_DOWN, cyrillic_ef, SC_MOD_LSHIFT);
    assert(!has_message);
    type_text(&kb, "Ф");
    expect_text(SC_CONTROL_MSG_TYPE_PASTE_TEXT, "Ф");
    key(&kb, SC_ACTION_UP, cyrillic_ef, SC_MOD_LSHIFT);
    assert(!has_message);
    type_text(&kb, "A Ёж №1, её"); // one multi-character SDL commit
    expect_text(SC_CONTROL_MSG_TYPE_PASTE_TEXT, "A Ёж №1, её");
    key(&kb, SC_ACTION_DOWN, cyrillic_ef, SC_MOD_LCTRL);
    expect_key(AKEYCODE_A, AKEY_EVENT_ACTION_DOWN);
    key(&kb, SC_ACTION_UP, cyrillic_ef, SC_MOD_LCTRL);
    expect_key(AKEYCODE_A, AKEY_EVENT_ACTION_UP);

    // RU -> EN: raw Latin keys and ordinary SDK text injection still work.
    key(&kb, SC_ACTION_DOWN, SC_KEYCODE_a, 0);
    expect_key(AKEYCODE_A, AKEY_EVENT_ACTION_DOWN);
    key(&kb, SC_ACTION_UP, SC_KEYCODE_a, 0);
    expect_key(AKEYCODE_A, AKEY_EVENT_ACTION_UP);
    type_text(&kb, "é");
    expect_text(SC_CONTROL_MSG_TYPE_INJECT_TEXT, "é");

    sc_keyboard_sdk_init(&kb, NULL, SC_KEY_INJECT_MODE_TEXT, true, true);
    type_text(&kb, "A");
    expect_text(SC_CONTROL_MSG_TYPE_INJECT_TEXT, "A");
    type_text(&kb, "ё");
    expect_text(SC_CONTROL_MSG_TYPE_PASTE_TEXT, "ё");
    sc_keyboard_sdk_init(&kb, NULL, SC_KEY_INJECT_MODE_TEXT, true, false);
    type_text(&kb, "ё");
    expect_text(SC_CONTROL_MSG_TYPE_INJECT_TEXT, "ё"); // no clipboard fallback

    sc_keyboard_sdk_init(&kb, NULL, SC_KEY_INJECT_MODE_RAW, true, true);
    key(&kb, SC_ACTION_DOWN, cyrillic_ef, 0);
    expect_key(AKEYCODE_A, AKEY_EVENT_ACTION_DOWN);
    type_text(&kb, "ф");
    assert(!has_message);
    return 0;
}
