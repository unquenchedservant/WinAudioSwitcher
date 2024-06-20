import servicemanager
import socket
import sys
import win32event
import win32service
import win32serviceutil

from __future__ import print_function
import comtypes
from pycaw.pycaw import AudioUtilities, IMMDeviceEnumerator, EDataFlow, DEVICE_STATE
from pycaw.constants import CLSID_MMDeviceEnumerator



class AudioSwitcherService(win32serviceutil.ServiceFramework):
    _svc_name_ = "WinAudioSwitcher"
    _svc_display_name_ = "WinAudioSwitcher Service"
    _svc_description_ = "This service switches the audio output device on Windows, using user defined rules."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.is_alive = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_alive = False

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        while self.is_alive:
            # TODO: Add logic for listening for the hotkey and then switching the audio output device
            pass

    def get_default_audio_output_device():
    # Create a new IMMDeviceEnumerator instance
        deviceEnumerator = comtypes.CoCreateInstance(
            CLSID_MMDeviceEnumerator,
            IMMDeviceEnumerator,
            comtypes.CLSCTX_INPROC_SERVER)
        
        # Get the default audio output endpoint
        default_device = deviceEnumerator.GetDefaultAudioEndpoint(EDataFlow.eRender.value, DEVICE_STATE.ACTIVE.value)
        return AudioUtilities.CreateDevice(default_device)



if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(AudioSwitcherService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(AudioSwitcherService)