package com.genymobile.scrcpy.wrappers;

import com.genymobile.scrcpy.AndroidVersions;
import com.genymobile.scrcpy.FakeContext;

import android.annotation.TargetApi;
import android.content.ClipData;
import android.content.ClipDescription;
import android.content.Context;
import android.os.Build;
import android.os.PersistableBundle;

import java.util.UUID;

public final class ClipboardManager {
    // Clipboard notifications are asynchronous: they can arrive after a paste or restore completes.
    private static final String EXTRA_ORIGIN = "com.genymobile.scrcpy.clipOrigin";
    private final String typingOrigin = UUID.randomUUID().toString();
    private final String restoredOrigin = "restored:" + typingOrigin;
    private final android.content.ClipboardManager manager;

    static ClipboardManager create() {
        android.content.ClipboardManager manager = (android.content.ClipboardManager) FakeContext.get().getSystemService(Context.CLIPBOARD_SERVICE);
        if (manager == null) {
            // Some devices have no clipboard manager
            // <https://github.com/Genymobile/scrcpy/issues/1440>
            // <https://github.com/Genymobile/scrcpy/issues/1556>
            return null;
        }
        return new ClipboardManager(manager);
    }

    private ClipboardManager(android.content.ClipboardManager manager) {
        this.manager = manager;
    }

    public CharSequence getText(boolean forAutosync) {
        ClipData clipData = manager.getPrimaryClip();
        if (clipData == null || clipData.getItemCount() == 0) {
            return null;
        }
        if (forAutosync && Build.VERSION.SDK_INT >= AndroidVersions.API_24_ANDROID_7_0) {
            String origin = getOrigin(clipData.getDescription());
            if (typingOrigin.equals(origin) || restoredOrigin.equals(origin)) {
                return null;
            }
        }
        return clipData.getItemAt(0).getText();
    }

    @TargetApi(AndroidVersions.API_24_ANDROID_7_0)
    private static String getOrigin(ClipDescription description) {
        return description != null && description.getExtras() != null ? description.getExtras().getString(EXTRA_ORIGIN) : null;
    }

    @TargetApi(AndroidVersions.API_24_ANDROID_7_0)
    private static void markClip(ClipData clip, String origin, boolean sensitive) {
        ClipDescription description = clip.getDescription();
        PersistableBundle extras = description.getExtras() != null ? new PersistableBundle(description.getExtras()) : new PersistableBundle();
        extras.putString(EXTRA_ORIGIN, origin);
        if (sensitive) {
            extras.putBoolean(ClipDescription.EXTRA_IS_SENSITIVE, true);
        }
        description.setExtras(extras);
    }

    public interface PasteAction {
        boolean paste();
    }

    // Android 7+. Unlike an explicit clipboard transfer, typing must not replace the user's clipboard or sync a character to the host.
    @TargetApi(AndroidVersions.API_24_ANDROID_7_0)
    public boolean withTemporaryText(String text, PasteAction action) {
        ClipData previous = manager.getPrimaryClip();
        if (previous == null && manager.hasPrimaryClip()) {
            // An unreadable clip cannot be restored.
            return false;
        }
        ClipData typed = ClipData.newPlainText(null, text);
        markClip(typed, typingOrigin, true);
        manager.setPrimaryClip(typed);
        try {
            // Some devices silently reject clipboard writes. Never paste the old contents instead.
            return typingOrigin.equals(getOrigin(manager.getPrimaryClipDescription())) && action.paste();
        } finally {
            // Do not overwrite a new clip copied by the user or the receiving app during the paste.
            if (typingOrigin.equals(getOrigin(manager.getPrimaryClipDescription()))) {
                if (previous == null && Build.VERSION.SDK_INT >= AndroidVersions.API_28_ANDROID_9) {
                    manager.clearPrimaryClip();
                } else {
                    ClipData restore = previous != null ? previous : ClipData.newPlainText(null, "");
                    markClip(restore, restoredOrigin, false);
                    manager.setPrimaryClip(restore);
                }
            }
        }
    }

    public boolean setText(CharSequence text) {
        ClipData clipData = ClipData.newPlainText(null, text);
        manager.setPrimaryClip(clipData);
        return true;
    }

    public void addPrimaryClipChangedListener(android.content.ClipboardManager.OnPrimaryClipChangedListener listener) {
        manager.addPrimaryClipChangedListener(listener);
    }
}
