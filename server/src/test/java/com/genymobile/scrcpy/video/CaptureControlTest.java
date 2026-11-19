package com.genymobile.scrcpy.video;

import org.junit.Assert;
import org.junit.Test;

public class CaptureControlTest {
    @Test
    public void testFpsChanges() {
        CaptureControl control = new CaptureControl(59.94f);
        Assert.assertEquals(59.94f, control.getMaxFps(), 0f);
        control.reset(CaptureControl.RESET_REASON_DISPLAY_PROPERTIES_CHANGED);
        control.setMaxFps(90);
        Assert.assertEquals(CaptureControl.RESET_REASON_CLIENT_RESET | CaptureControl.RESET_REASON_DISPLAY_PROPERTIES_CHANGED, control.consumeReset());
        control.setMaxFps(90); // The same shortcut must not interrupt capture again.
        Assert.assertFalse(control.isResetRequested());
        control.setMaxFps(30);
        control.setMaxFps(0); // Last request wins, even before the encoder starts.
        Assert.assertEquals(0f, control.getMaxFps(), 0f);
        Assert.assertEquals(CaptureControl.RESET_REASON_CLIENT_RESET, control.consumeReset());
    }
}
